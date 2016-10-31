import sys
import collections
import pandas as pd


def rm_dup(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

d = pd.read_csv(sys.argv[1])
#d = d[~d.aclk.str.contains("")]
d.aclk = pd.to_numeric(d.aclk, downcast='unsigned')
aclk0 = d.aclk[0]
d.aclk = d.aclk - aclk0
d['tmp'] = d.aclk.shift()
d['diff'] = d.aclk - d.tmp

#sample = d['diff'].sample(10000)
sample = d['diff']
counter = collections.Counter(sample)
diffs = sorted(d['diff'], reverse=True)
diffs = rm_dup(diffs)
for diff in diffs:
    print diff, counter[diff]
