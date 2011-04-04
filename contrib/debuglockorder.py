#!/usr/bin/env python

#
# Parse debug.log files to look for potential deadlock problems
# Run bitcoin with the -debug flag; this looks for lines in debug.log
# of that look like:
# W:cs_foo:function
# L:cs_foo:function
# U:cs_foo:function
# ... which mean 'Waiting/Locked/Unlocked'
#

import os.path
import sys
import re
from collections import defaultdict

def determine_db_dir():
  import platform
  if platform.system() == "Darwin":
    return os.path.expanduser("~/Library/Application Support/Bitcoin/")
  elif platform.system() == "Windows":
    return os.path.join(os.environ['APPDATA'], "Bitcoin")
  return os.path.expanduser("~/.bitcoin")

def main():
  import optparse
  parser = optparse.OptionParser(usage="%prog [options]")
  parser.add_option("--datadir", dest="datadir", default=determine_db_dir(),
                    help="Look for debug.log here (defaults to bitcoin default)")
  parser.add_option("--testnet", action="store_true", dest="testnet", default=False,
                    help="Find the -testnet debug.log")

  (options, args) = parser.parse_args()

  import pdb
  pdb.set_trace()

  if options.testnet:
    debuglog = os.path.join(options.datadir, "testnet", "debug.log")
  else:
    debuglog = os.path.join(options.datadir, "debug.log")

  chains = defaultdict(set)
  pairs = set()
  chain = defaultdict(list)
  callstack = defaultdict(list)
  callstacks = defaultdict(set)
  waiting = defaultdict(lambda: defaultdict(int))
  locked = defaultdict(lambda: defaultdict(int))

  fp = open(debuglog)
  for (line_number, line) in enumerate(fp):
    if line[0:2] == 'W:':
      (cs,thread,func) = (line[2:]).strip().split(":")
      waiting[thread][cs] += 1
    elif line[0:2] == 'L:':
      (cs,thread,func) = (line[2:]).strip().split(":")
      waiting[thread][cs] -= 1
      locked[thread][cs] += 1
      chain[thread].append(cs)
      callstack[thread].append(func)
      p = (chain[thread][0], cs)
      if p not in pairs:
        pairs.add(p)
        callstacks[p].add(str(callstack[thread]))
    elif line[0:2] == 'U:':
      (cs,thread,func) = (line[2:]).strip().split(":")
      if locked[thread][cs] == 0 or len(chain[thread]) == 0 or len(callstack[thread]) == 0:
        print("Unlock missing lock? line %d (%s)"%(line_number, line))
        continue
      locked[thread][cs] -= 1
      chains[thread].add(str(chain[thread]))
      chain[thread].pop()
      callstack[thread].pop()
    else:
      continue

  already_reported = set()
  for p in sorted(pairs):
    if p[0] == p[1] or p in already_reported: continue
    p_inverse = (p[1], p[0])
    if p_inverse in pairs:
      already_reported.add(p)
      already_reported.add(p_inverse)
      print("INCONSISTENT LOCK ORDER: "+str(p))
      print(" Call stacks for order %s:\n  %s"%(str(p), str(callstacks[p])))
      print(" Call stacks for order %s:\n  %s"%(str(p_inverse), str(callstacks[p_inverse])))
  for (thread, d) in waiting.iteritems():
    for (cs, count) in d.iteritems():
      if count > 0: print("bitcoin exited waiting on: "+cs)

if __name__ == '__main__':
    main()
