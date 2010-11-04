#!/usr/bin/python

import sys
import re
from time import gmtime, strftime

def stime(timestamp):
    return strftime("%d %b %Y %H:%M:%S", gmtime(timestamp))

cseq_re = re.compile("CSeq:\s*([0-9]+)", re.I)
def parse_cseq(message):
    m = cseq_re.search(message)
    if m:
        return int(m.group(1))
    return 0

def get_trace(cid):
    result = []
    for line in sys.stdin:
        fields = line.split('|')
        if len(fields) != 10:
            print "input error"
            break
        callid = fields[1]
        if cid not in callid:
            continue
        message = fields[0].replace('\\x0D\\x0A', '\n')
        cseq = parse_cseq(message)
        is_reply = int(bool(fields[3]))
        from_host = fields[4]
        to_host = fields[5]
        timestamp = int(fields[6])
        direction = fields[7]
        weight = cseq * 2 + is_reply
        msg = "%s %s -> %s (%s):\n%s" % (stime(timestamp), from_host, to_host, direction, message)
        result.append((timestamp, weight, msg))
    return sorted(result)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: %s CALLID" % sys.argv[0])
        sys.exit(1)
    trace = get_trace(sys.argv[1])
    if trace:
        print("\n\n".join(x[2] for x in trace))
