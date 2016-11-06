import sys
import collections
import pandas as pd


def rm_dup(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

d = pd.read_csv(sys.argv[1], header=None)
#d = d[~d[0].str.contains("")]
d[0] = pd.to_numeric(d[0], downcast='unsigned')
jclk0 = d[0][0]
d[0] = d[0] - jclk0
d['tmp'] = d[0].shift()
d['diff'] = d[0] - d.tmp

#sample = d['diff'].sample(10000)
sample = d['diff']
counter = collections.Counter(sample)
diffs = sorted(d['diff'], reverse=True)
diffs = rm_dup(diffs)
for diff in diffs:
    print diff, counter[diff]
