#!/usr/bin/env python

# solver for compression challenge - pctf 2013
# jiva

import socket
import struct
import string
import math

HOST = '54.234.224.216'
PORT = 4433

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

nonce = s.recv(8)

flag = ''

for _ in xrange(20):
  avg_len = 0
	lengths = {}
	for c in string.lowercase + '_':
		send_data = (flag+c)*10
		s.send(struct.pack('I', len(send_data)) + send_data)
		ciphertext_length = s.recv(4)
		ciphertext_length = struct.unpack('I', ciphertext_length)[0]
		ciphertext = s.recv(ciphertext_length)
		lengths[c] = ciphertext_length

	avg_len = math.ceil(float(sum(lengths.values())) / len(lengths))
	for char,length in lengths.items():
		if _ == 11: # GHETTO IM SO SORRY ABOUT THIS
				flag += 'i'
				print 'FLAG SO FAR:', flag
				break
		if lengths[char] < avg_len:
			if _ == 1 and char == 'c': continue # GHETTO IM SO SORRY ABOUT THIS
			if _ == 10 and char == '_': continue # GHETTO IM SO SORRY ABOUT THIS	
			if _ == 14 and char == '_': continue # GHETTO IM SO SORRY ABOUT THIS	
			flag += char 
			print 'FLAG SO FAR:', flag
			break

s.close()

'''
PROBLEM_KEY is 20 bytes

ccccXXXXXXXXXXXXXXXX XXXX


'''
