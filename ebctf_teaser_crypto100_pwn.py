
# pwn for "crypto100" ebctf 2013 teaser
# jiva

import hashlib

def xor(d, k): return ''.join([chr(ord(d[i]) ^ ord(k[i % len(k)])) for i in xrange(len(d))])

def h(x):
    x = hashlib.sha256(x).digest()
    x = xor(x[:16], x[16:])
    return x

def crypt(msg, initial_key):
    k = initial_key

    out = ''
    for i in xrange(0, len(msg), 16):
        out += xor(msg[i:i+16], k)
        k = h(k + str(len(msg)))

    return out

msg2 = open('msg002.enc').read().decode('base64')

k = xor(msg2[:16], 'From: Vlugge Jap')

print crypt(msg2,k)

'''
From: Vlugge Japie <vl.japie@yahoo.com>
To: Baron van Neemweggen <b.neemweggen@zmail.com>
Subj: Found it!

Boss,

I found some strange code on one of the documents.
Is this what you're looking for?

ebCTF{21bbc4f404fa2057cde2adbf864b5481}

Vlugge Japie
'''
