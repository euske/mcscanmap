#!/usr/bin/env python
import sys
import bsddb3

def main(argv):
    import getopt
    def usage():
        print 'usage: %s [-k|-v] path ...' % argv[0]
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'kv')
    except getopt.GetoptError:
        return usage()
    def dispitem(k,v):
        print '+%d,%d:%s->%s' % (len(k), len(v), k, v)
        return
    def dispkey(k,v):
        print '+%d:%s' % (len(k), k)
        return
    def dispvalue(k,v):
        print '+%d:%s' % (len(v), v)
        return
    func = dispitem
    for (k,v) in opts:
        if k == '-k':
            func = dispkey
        elif k == '-v':
            func = diskvalue
    if not args: return usage()
    for path in args:
        db = bsddb3.hashopen(path, 'r')
        for (k,v) in db.iteritems():
            func(k, v)
        db.close()
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv))
