#!/usr/bin/env python

import os
import sys
from stat import *

#
# Fucntion to get files from a given path
#
def get_sync_files(path):
	sync_files = []

	for filename in os.listdir(path):
		if filename[0] != "." and filename[-1] != "~":
			sync_files.append(filename)

	return sync_files


#
# Function that returns saved stats from file
#
def get_saved_file_stats():
	saved_stats = {}
	if not os.path.exists(".file_stats"):
		return {}

	fil = open(".file_stats")
	
	for lin in fil.readlines():
		if lin == "":
			break
		res = lin.split("|")
		saved_stats[res[0]] = float(res[-1])
	
	fil.close()
	return saved_stats


#
# Function that returns the stats of sync_files
#
def get_sync_files_stat(sync_files, saved_stats):
	file_stats = {}
	
	if sync_files == []:
		return {}

	for entry in sync_files:
		statval = os.lstat(entry)
		if S_ISREG(statval[ST_MODE]):					# regular file
			if entry in saved_stats:				# entry exists in saved_stats
				file_stats[entry] = (float(statval.st_mtime), saved_stats[entry])	# get the (mod, last_mod)
			else:							
				file_stats[entry] = (float(statval.st_mtime), float(statval.st_ctime))	# get the (mod, create)

	return file_stats

#
# store list of files with mod timestamps
#
def write_file_stats(file_stats):
	fil = open(".file_stats", "w")
	for fstat in file_stats:
		fil.write(fstat + "|" + str(file_stats[fstat][0]) + "\n")

	fil.close()

#
# create a stat map from string
#
def string_to_file_stats(string):
	if string == "":
		return {}
	
	string = string.splitlines()
	file_stats = {}

	for i in string:
		res = i.split("|")
		file_stats[res[0]] = (float(res[-2]), float(res[-1]))

	return file_stats

#
# get list of files to be received
#
def compare_stats(file_stats, recv_stats):
	final = { "DOWN" : [], "UP" : [] }
	
	for f in file_stats:
		if f in recv_stats:
			if f not in final["UP"] and f not in final["DOWN"]:
				loc_diff = file_stats[f][0]-file_stats[f][1]
				recv_diff = recv_stats[f][0]-recv_stats[f][1]
				if (loc_diff - recv_diff) > 5:
					final["UP"].append(f)
				elif (loc_diff - recv_diff) < -5:
					final["DOWN"].append(f)
		else:
			final["UP"].append(f)

	for f in recv_stats:
		if f in file_stats:
			if f not in final["UP"] and f not in final["DOWN"]:
				loc_diff = file_stats[f][0]-file_stats[f][1]
				recv_diff = recv_stats[f][0]-recv_stats[f][1]
				if (loc_diff - recv_diff) > 5:
					final["UP"].append(f)
				elif (loc_diff - recv_diff) < -5:
					final["DOWN"].append(f)
		else:
			final["DOWN"].append(f)

	return final

#
# create string from file_stats
#
def file_stats_to_string(file_stats):
	string = ""
	for fstat in file_stats:
		string += fstat + "|" + str(file_stats[fstat][0]) + "|" + str(file_stats[fstat][1]) + "\n"
	
	return string
