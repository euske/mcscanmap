#!/usr/bin/env python
import sys, os
import os.path
import Image


##  Renderer
##
class Renderer(object):

    COLORS = [(0,255,255), (0,255,128), (0,255,0), (128,255,0),
              (224,224,0), (255,128,0), (255,0,0), (255,0,128)]
    
    def __init__(self, basedir, maxlevel, size=256):
        try:
            os.makedirs(basedir)
        except OSError:
            pass
        self.basedir = basedir
        self.maxlevel = maxlevel
        self.size = size
        self.format = 'm%s.png'
        return
    
    def render(self, tree, name='', level=0):
        img0 = Image.new('RGBA', (self.size, self.size))
        path = os.path.join(self.basedir, self.format % name)
        if level == self.maxlevel:
            assert isinstance(tree, int)
            assert name
            v = min(tree, len(self.COLORS)-1)
            img0.paste(self.COLORS[v], None)
        else:
            img0.paste((0,0,0,0), None)
            for (k,(dx,dy)) in (('0',(0,0)), ('1',(1,0)),
                                ('2',(0,1)), ('3',(1,1))):
                if k not in tree: continue
                src = self.render(tree[k], name+k, level=level+1)
                img1 = Image.open(src)
                img1 = img1.resize((self.size/2, self.size/2))
                img0.paste(img1, (dx*self.size/2, dy*self.size/2))
        img0.save(path)
        print path
        return path

# main
def main(argv):
    import getopt
    import fileinput
    def usage():
        print 'usage: %s [-m maxlevel] [-s size] outdir ...' % argv[0]
        return 100
    try:
        (opts, args) = getopt.getopt(argv[1:], 'm:s:')
    except getopt.GetoptError:
        return usage()
    if not args: return usage()
    outdir = args.pop(0)
    maxlevel = 8
    size = 256
    for (k, v) in opts:
        if k == '-m': maxlevel = int(v)
        elif k == '-s': size = int(v)
    renderer = Renderer(outdir, maxlevel, size=size)
    tree = {}
    for line in fileinput.input(args):
        line = line.strip()
        if len(line) != maxlevel: continue
        t = tree
        for c in line[:-1]:
            if c not in t: t[c] = {}
            t = t[c]
        c = line[-1]
        if c not in t: t[c] = 0
        t[c] += 1
    renderer.render(tree)
    return

if __name__ == '__main__': sys.exit(main(sys.argv))
