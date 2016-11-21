"""
This file is named after `dask` for historical reasons. We first tried to
use dask to coordinate the hdf5 buckets but it was slow and we wrote our own
stuff.
"""
import numpy as np
import h5py
import time
import logging
import traceback

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def concatenate(camera_names, time_len):
  logs_names = [x.replace('camera', 'log') for x in camera_names]

  steering = []  # steering steering of the car
  throttle = []  # steering steering of the car
  hdf5_camera = []  # the camera hdf5 files need to continue open
  c5x = []
  filters = []
  lastidx = 0

  for cword, tword in zip(camera_names, logs_names):
    try:
      with h5py.File(tword, "r") as t5:
        c5 = h5py.File(cword, "r")
        hdf5_camera.append(c5)
        x = c5["images"]
        c5x.append((lastidx, lastidx+x.shape[0], x))

        throttle_value = t5["throttle"][:]
        steering_steering = t5["steering"][:]
        idxs = np.linspace(0, steering_steering.shape[0]-1, x.shape[0]).astype("int")  # approximate alignment
        steering.append(steering_steering[idxs])
        throttle.append(throttle_value[idxs])

        goods = np.abs(steering[-1]) <= 600

        filters.append(np.argwhere(goods)[time_len-1:] + (lastidx+time_len-1))
        lastidx += goods.shape[0]
        # check for mismatched length bug
        print("x {} | t {} | f {}".format(x.shape[0], steering_steering.shape[0], goods.shape[0]))
        if x.shape[0] != steering[-1].shape[0] or x.shape[0] != goods.shape[0]:
          raise Exception("bad shape")

    except IOError:
      import traceback
      traceback.print_exc()
      print "failed to open", tword

  steering = np.concatenate(steering, axis=0)
  throttle = np.concatenate(throttle, axis=0)
  filters = np.concatenate(filters, axis=0).ravel()
  print "training on %d/%d examples" % (filters.shape[0], steering.shape[0])
  return c5x, steering, throttle, filters, hdf5_camera


first = True


def datagen(filter_files, time_len=1, batch_size=256, ignore_goods=False):
  """
  Parameters:
  -----------
  leads : bool, should we use all x, y and speed radar leads? default is false, uses only x
  """
  global first
  assert time_len > 0
  filter_names = sorted(filter_files)

  logger.info("Loading {} hdf5 buckets.".format(len(filter_names)))

  c5x, steering, throttle, filters, hdf5_camera = concatenate(filter_names, time_len=time_len)
  filters_set = set(filters)

  logger.info("camera files {}".format(len(c5x)))

  X_batch = np.zeros((batch_size, time_len, 160, 320, 3), dtype='uint8')
  steering_batch = np.zeros((batch_size, time_len, 1), dtype='float32')
  throttle_batch = np.zeros((batch_size, time_len, 1), dtype='float32')

  while True:
    try:
      t = time.time()

      count = 0
      start = time.time()
      while count < batch_size:
        if not ignore_goods:
          i = np.random.choice(filters)
          # check the time history for goods
          good = True
          for j in (i-time_len+1, i+1):
            if j not in filters_set:
              good = False
          if not good:
            continue

        else:
          i = np.random.randint(time_len+1, len(steering), 1)

        # GET X_BATCH
        # low quality loop
        for es, ee, x in c5x:
          if i >= es and i < ee:
            X_batch[count] = x[i-es-time_len+1:i-es+1]
            break

        steering_batch[count] = np.copy(steering[i-time_len+1:i+1])[:, None]
        throttle_batch[count] = np.copy(throttle[i-time_len+1:i+1])[:, None]

        count += 1

      # sanity check
      assert X_batch.shape == (batch_size, time_len, 160, 320, 3)

      logging.debug("load image : {}s".format(time.time()-t))
      print("%5.2f ms" % ((time.time()-start)*1000.0))

      if first:
        print "X", X_batch.shape
        print "steering", steering_batch.shape
        print "throttle", throttle_batch.shape
        first = False

      yield (X_batch, steering_batch, throttle_batch)

    except KeyboardInterrupt:
      raise
    except:
      traceback.print_exc()
      pass
