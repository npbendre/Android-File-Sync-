#!/usr/bin/env python

from socket import *
import sys
import time
from file_sync import *

TIMEOUT = 1

#
# Function to transfer file to host
#
def to_host(sock, filename):
	fil = open(filename, "rb")
	data = fil.read()
	
	print "[Sending]", filename
	sock.sendall(data)
	print "[Done]\n"
	
	fil.close()

#
# Function to receive file from host
#
def from_host(sock, filename):
	fil = open(filename, "wb")
	once = 1
	while True:
		try:
			data = sock.recv(1024)
			if once == 1:
				print "[Receiving]", filename
				sock.settimeout(TIMEOUT)
				once = 0

			fil.write(data)
			if len(data) < 1024:
				print "[Done]\n"
				break
		except timeout:
			break

	sock.setblocking(1)
	fil.close()


def get_file_transfer_msg(sock):
	string = ""
	while True:
		data = sock.recv(1024)
		string += data
		if len(data) < 1024:
			break
	
	return string


def get_transfer_map(msg):
	msg = msg.splitlines()
	final = {}
	
	for i in msg:
		res = i.split("|")
		final[res.pop(0)] = res
	
	return final

def start_transfer(sock, final):
	for mode in ["UP", "DOWN"]:
		if mode in final and final[mode] != []:	# get files from host
			for fil in final[mode]:
				if fil != "":
					sock.sendall(mode + "|" + fil)
					time.sleep(TIMEOUT+1)
					if mode == "UP":
						from_host(sock, fil)
					else:
						to_host(sock, fil)
						time.sleep(TIMEOUT+1)
	sock.sendall("DONE")

#
# main routine
#
def main():
	path = "/sdcard/sync"
	os.chdir(path)

	host = "10.0.2.2"
	port = int(sys.argv[1])
	sock = socket(AF_INET, SOCK_STREAM)
	sock.connect((host, port))

	# get device file_stats
	file_stats = get_sync_files_stat(get_sync_files(path), get_saved_file_stats())
	string = file_stats_to_string(file_stats)
	
	# send file_stats to host
	sock.sendall(string)

	msg = get_file_transfer_msg(sock)
	if msg != "":
		final = get_transfer_map(msg)
		start_transfer(sock, final)
		# get new file_stats
		file_stats = get_sync_files_stat(get_sync_files(path), get_saved_file_stats())

	print "[Sync'd]"
	write_file_stats(file_stats)
	sock.close()
	return 0


if __name__ == "__main__":
	sys.exit(main())
