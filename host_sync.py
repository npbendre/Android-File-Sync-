#!/usr/bin/env python

from socket import *
import sys
import time
from file_sync import *

TIMEOUT = 1

#
# Function to transfer file to android device
#
def to_android(conn, filename):
	fil = open(filename, "rb")
	data = fil.read()

	print "[Sending]", filename
	conn.sendall(data)
	print "[Done]\n"

	fil.close()

#
# Function to receive file from android device
#
def from_android(conn, filename):
	fil = open(filename, "wb")
	once = 1
	while True:
		try:
			data = conn.recv(1024)
			if once == 1:
				print "[Receiving]", filename
				conn.settimeout(TIMEOUT)
				once = 0

			fil.write(data)
			if len(data) < 1024:
				print "[Done]\n"
				break
		except timeout:
			break

	conn.setblocking(1)
	fil.close()

#
# Function to receive file_stats from android device
#
def wait_for_file_stats(conn):
	string = ""
	while True:
		data = conn.recv(1024)
		string += data
		if len(data) < 1024:
			break
	
	return string

#
# Function to get message to be sent to android device
#
def get_file_transfer_string(final):
	string = ""
	
	for key in ["UP", "DOWN"]:
		if final[key] != []:
			string += key + "|"
			for i in final[key]:
				string += i + "|"
			string += "\n"

	return string

#
# Function to start file transfer
#
def start_transfer(conn):
	while True:
		msg = conn.recv(1024)

		if "DONE" in msg:
			break

		mode, filename = msg.split("|")
	
		if mode == "UP":
			to_android(conn, filename)
			time.sleep(TIMEOUT+1)
		elif mode == "DOWN":
			from_android(conn, filename)

#
# main routine
#
def main():
	path = "/home/kernel/py"
	os.chdir(path)

	host = ""
	port = int(sys.argv[1])

	sock = socket(AF_INET, SOCK_STREAM)
	sock.bind((host, port))
	sock.listen(1)
	conn, addr = sock.accept()
	
	# host file stats
	file_stats = get_sync_files_stat(get_sync_files(path), get_saved_file_stats())
	
	# get android file stats
	recv_string = wait_for_file_stats(conn)
	recv_stats = string_to_file_stats(recv_string)

	# list of files to be uploaded and downloaded
	final = compare_stats(file_stats, recv_stats)
	string = get_file_transfer_string(final)

	# send file transfer string
	conn.sendall(string)
	if string != "":
		start_transfer(conn)
		# store new file_stats
		file_stats = get_sync_files_stat(get_sync_files(path), get_saved_file_stats())

	print "[Sync'd]"
	write_file_stats(file_stats)
	conn.close()
	sock.close()
	return 0

if __name__ == "__main__":
	sys.exit(main())
