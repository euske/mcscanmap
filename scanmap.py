#!/usr/bin/env python
import sys
import md5
import urlparse
import requests
import bsddb3


##  MapScanner
##
class MapScanner(object):

    def __init__(self, dbpath, basehref, minlevel, maxlevel):
        print >>sys.stderr, 'opening: %r' % dbpath
        self.db = bsddb3.hashopen(dbpath)
        self.basehref = basehref
        self.minlevel = minlevel
        self.maxlevel = maxlevel
        self.session = requests.session()
        return

    def close(self):
        self.session.close()
        self.db.close()
        return

    def fetch(self, k):
        k = '/'.join(k)
        url = urlparse.urljoin(self.basehref, k)+'.png'
        print >>sys.stderr, 'fetching: %r' % url
        resp = self.session.get(url)
        if resp.status_code != 200: return None
        return resp.content

    def run(self, k0=''):
        if self.maxlevel <= len(k0): return
        print >>sys.stderr, 'scanning: %r' % k0
        for c in '0123':
            k1 = k0+c
            v1 = self.fetch(k1)
            if v1 is None: continue
            if self.minlevel <= len(k1):
                buf = md5.md5()
                buf.update(v1)
                h1 = buf.digest()
                h0 = self.db.get('h'+k1)
                if h0 == h1: continue
                self.db['h'+k1] = h1
                #self.db['v'+k1] = v1
                if (self.maxlevel == len(k1) and
                    h0 is not None):
                    print k1
            self.run(k1)
        return

# main
def main(argv):
    import getopt
    def usage():
        print 'usage: %s [-n minlevel] [-m maxlevel] dbpath basehref' % argv[0]
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'n:m:')
    except getopt.GetoptError:
        return usage()
    minlevel = 4
    maxlevel = 8
    for (k,v) in opts:
        if k == '-n':
            minlevel = int(v)
        elif k == '-m':
            maxlevel = int(v)
    if len(args) < 2: return usage()
    dbpath = args.pop(0)
    basehref =args.pop(0)
    scanner = MapScanner(dbpath, basehref, minlevel, maxlevel)
    scanner.run()
    scanner.close()
    return

if __name__ == '__main__': sys.exit(main(sys.argv))
