#!/usr/bin/env python
import argparse
import numpy as np
import h5py
import json
from keras.models import model_from_json


# ***** main loop *****
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Path viewer')
  parser.add_argument('model', type=str, help='Path to model definition json. Model weights should be on the same path.')
  parser.add_argument('--dataset', type=str, default="2016-11-16--07-51-06", help='Dataset/video clip name')
  args = parser.parse_args()

  with open(args.model, 'r') as jfile:
    model = model_from_json(json.load(jfile))

  model.compile("sgd", "mse")
  weights_file = args.model.replace('json', 'keras')
  model.load_weights(weights_file)

  # default dataset is the validation data on the highway
  dataset = args.dataset

  log = h5py.File("dataset/log/"+dataset+".h5", "r")
  cam = h5py.File("dataset/camera/"+dataset+".h5", "r")

  print cam.keys()
  print log.keys()

  # skip to highway
  for i in xrange(cam['images'].shape[0]):
    if i%30 == 0:
      print "%.2f seconds elapsed" % (i/30.0)
    img = cam['images'][i]
    predicted_steers = model.predict(img[None, :, :, :])[0][0] - 100
    print predicted_steers, log['steering'][i][0]
