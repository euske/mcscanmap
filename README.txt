Minecraft Pigmap Scanner
by Yusuke Shinyama <yusuke at cs dot nyu dot edu>

What is it?
This program scans the pigmap output of a Minecraft server and
generate an activity map overlay. It maintains a Berkeley dbm 
file to keep the md5 hash of each image data to detect the changes.
The scanning (crawling) is performed in an efficient manner so 
only about 1-2% of the entire map data is needed.

Prerequisites:
  1. Python 2.6 or newer (Python 3 is *not* supported.)
  2. Berkeley DB 3 (http://pypi.python.org/pypi/bsddb3/)
  2. Requests (http://pypi.python.org/pypi/requests/)
  3. Python Imageing Library 1.1.6 (http://pypi.python.org/pypi/PIL)

How to use:
  $ python scanmap.py map.db http://minecraft.example.com/map/ > map.out
  $ python render.py ./out/ map.out

Terms and Conditions:
This program is in public domain and comes with ABSOLUTELY NO WARRANTY.
There's no need to ask permission of doing anything with this program.
