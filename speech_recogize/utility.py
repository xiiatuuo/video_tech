#!/usr/bin/python2.6
#coding=utf8
import os
import sys
import datetime
import time
import ConfigParser
import traceback
#import pycurl
import urllib2
import cStringIO
import random
import socket
import struct
import fcntl
import re

FILE_ROOT = os.path.abspath(os.path.dirname(__file__))
LOG_FILE = os.path.join(FILE_ROOT, "./log_file")

ISOTIMEFORMAT = "%Y-%m-%d %H:%M:%S"
ISOTIMEFORMAT_1 = "%Y%m%d"
ISOTIMEFORMAT_Y_M_D_H = "%Y%m%d%H%M"
LOG_LEVEL_ERROR = "ERROR"
LOG_LEVEL_WARNING = "WARNING"
LOG_LEVEL_DEBUG = "DEBUG"
LOG_LEVEL_INFO = "INFO"

req = 0

#class for parsing ini file
class SearchConf():
	def __init__(self, search_conf_file):
		self.conffile = search_conf_file
		self.config = ConfigParser.ConfigParser()
		self.config.read(search_conf_file)

	def readConfig(self, section, option):
		return self.config.get(section, option)

	def writeConfig(self, section, option, value):
		self.config.set(section, option, value)
		self.config.write(open(self.conffile, 'w'))

	def sections(self):
		return self.config.sections()

	def items(self, section_name):
		return self.config.items(section_name)

#log file on today
g_log_buffer = ""
MAX_BUFFER = 102400
def log_file(exception_str, log_level = LOG_LEVEL_ERROR, flush_flag = 0, log_file_name = LOG_FILE):
	try:
		global g_log_buffer
		section_list = []
		section_list.append(str(get_current_time()))
		section_list.append(":")
		section_list.append(str(log_level))
		try:
			section_list.append(os.path.basename(sys._getframe().f_back.f_code.co_filename))
			section_list.append("p"+str(sys._getframe(1).f_lineno))
			section_list.append(sys._getframe().f_back.f_code.co_name)
		except Exception, data:
			pass
		section_list.append(str(exception_str))
		section_list.append(traceback.format_exc())
		sys.exc_clear()
		section_list.append("\n")
		content_str = ""
		content_str = "\t".join(section_list)

		g_log_buffer = g_log_buffer + content_str

		if len(g_log_buffer) > MAX_BUFFER:
			flush_flag = 1

		if flush_flag == 1:
			current_time = get_current_time(ISOTIMEFORMAT_1)
			log_file_name = log_file_name + "_" + current_time + ".txt"
			try:
				f = open(log_file_name, "a")
			except Exception, data:
				print Exception, data
				log_file_name = "log_file" + "_" + current_time + ".txt"
				try:
					f = open(log_file_name, "a")
				except Exception, data:
					print Exception, data
					g_log_buffer = ""
					return

			try:
				f.write(g_log_buffer)
				f.close()
			except Exception, data:
				print str(data)
			g_log_buffer = ""
			return
	except Exception, data:
		return

#get currentTime
def get_current_time(ios_time_format = ISOTIMEFORMAT):
	t_now_time = datetime.datetime.now()
	str_time = datetime.datetime.strftime(t_now_time, ios_time_format)[:]
	return str_time

#deal with date to timestamp
def deal_with_datestr(date_str, time_format = ISOTIMEFORMAT_Y_M_D_H):
	timestamp = int(time.mktime(time.strptime(date_str, time_format)))
	return timestamp


def get_src_val(ini_info_list,src_from):
	src_from = urllib2.unquote(src_from)
	if len(ini_info_list) == 0:
		return 0

	for item in ini_info_list:
		if len(item) != 3:
			continue
		## find
		flag = 0
		if item[0] == 0:
			for temp in item[1:-1]:
				if src_from.find(temp) != -1 :
					flag += 1
			if flag == len(item) - 2:
				return item[-1]
		if item[0] == 1:
			res = re.search(item[1], src_from)
			if res != None:
				return item[-1]
		
	return 0


#read interface
def read_url_port_pycurl_old(interface_url, connect_time_out = 0.1, read_time_out = 0.2):
	buf = cStringIO.StringIO()
	c = pycurl.Curl()
	result = ""
	try:
		c.setopt(c.URL, interface_url)
		c.setopt(c.WRITEFUNCTION, buf.write)
		c.setopt(c.CONNECTTIMEOUT, connect_time_out)
		c.setopt(c.TIMEOUT, read_time_out)
		c.setopt(c.FAILONERROR, True)

		c.perform()
		result = buf.getvalue()
	except Exception, data:
		log_file(str(data))

	c.close()
	buf.close()
	return result

def read_url_port_pycurl(interface_url, connect_time_out = 0.1, read_time_out = 0.2):
	result = ""
	try:
		socket.setdefaulttimeout(connect_time_out)
		headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
		req = urllib2.Request(url = interface_url, headers = headers)
		result = urllib2.urlopen(interface_url, timeout=100).read()
	except urllib2.URLError, e:
		log_file("http error\t" + interface_url + "\n")
	except Exception, data:
		log_file(str(data) + "\n" + interface_url + "\n")
	return result

def read_url_port_pycurl_with_auth(interface_url, user, passwd, connect_time_out = 0.2, read_time_out = 0.25):
	result = ""
	from base64 import encodestring
	try:
		socket.setdefaulttimeout(connect_time_out)
		req = urllib2.Request(interface_url)
		b64str = encodestring('%s:%s' % (user, passwd))[:-1]
		req.add_header("Authorization", "Basic %s" % b64str)
		result = urllib2.urlopen(req, timeout=100).read()
	except urllib2.URLError, e:
		log_file("http error\t" + interface_url + "\n")
	except urllib2.HTTPError, e:
		print "http error\t" + interface_url + "\n"
		log_file("http error\t" + interface_url + "\n")
	except Exception, data:
		log_file("http error\t" + interface_url + "\n")
	return result

def parse_ini_write(ini_file_path, conf_dict):
	try:
		gfilepath = ini_file_path.split("../conf/")[0]
		lastfname = ini_file_path.split('/')[-1][:-4]
		pyini_file_path = gfilepath +"./config_tmp/" + lastfname + ".py"
		dname = lastfname + "_ini"
		#file w
		if os.path.exists(pyini_file_path) == True:
			log_file(lastfname + ":write-hasfile")
			return 1
		f = open(pyini_file_path, 'w')
		f.write("conf_d = {}\nconf_d[\"" + dname + "\"] = " + repr(conf_dict) + "\n")
		log_file(lastfname + ":write")
		f.close()
		return 1
	except Exception, data:
		log_file(lastfname + ":write Exception")
	return 0

def parse_ini_read(ini_file_path, conf_dict):
	try:
		gfilepath = ini_file_path.split("../conf/")[0]
		importname = ini_file_path.split('/')[-1][:-4]
		#pyini_file_path = gfilepath +"./config_tmp/" + lastfname + ".py"
		#if os.path.exists(pyini_file_path) != True:
		#	log_file(pyini_file_path + " parse_ini_read false\n")
		#	return 0

		dname = importname + "_ini"
		try:
			mod = __import__(importname)
		except ImportError:
			log_file(importname + " import error")
			return 0
		conf_dict_tmp = mod.conf_d[dname]
		for i in conf_dict_tmp:
			conf_dict[i] = conf_dict_tmp[i]

		return 1
	except Exception, data:
		log_file(importname + " parse_ini_read false\n")
	return 0

def parse_ini_load(ini_file_path, section_name_list, dict_key_list, conf_dict):
	search_conf = SearchConf(ini_file_path)
	for section_name in section_name_list:
		section_conf_dict = {}
		for each in dict_key_list:
			try:
				ini_value = search_conf.readConfig(section_name, each)
				section_conf_dict[each] = ini_value
			except Exception, data:
				log_file(str(data))
				pass

		conf_dict[section_name] = section_conf_dict

def parse_ini_all_load(ini_file_path, conf_dict):
	search_conf = SearchConf(ini_file_path)
	for section_name in search_conf.sections():
		section_conf_dict = {}
		try:
			key_value_pair_list = search_conf.items(section_name)
			for (key, value) in key_value_pair_list:
				section_conf_dict[key] = value
		except Exception, data:
			log_file(str(data))
			pass
		conf_dict[section_name] = section_conf_dict

#parse ini
def parse_ini(ini_file_path, section_name_list, dict_key_list, conf_dict):
	if parse_ini_read(ini_file_path, conf_dict) == 0:
		parse_ini_load(ini_file_path, section_name_list, dict_key_list, conf_dict)
		if req == 0:
			parse_ini_write(ini_file_path, conf_dict)

#parse all ini
def parse_ini_all(ini_file_path, conf_dict):
	if parse_ini_read(ini_file_path, conf_dict) == 0:
		parse_ini_all_load(ini_file_path, conf_dict)
		if req == 0:
			parse_ini_write(ini_file_path, conf_dict)

#get random address
def get_random_address(address_list, ip_type):
	list_len_n = len(address_list)
	try:
		int_n = random.randint(0, list_len_n - 1)
		address_str = address_list[int_n][ip_type]
	except Exception, data:
		address_str = address_list[0][ip_type]

	return address_str

#get double random addresses
def get_random_address_double(address_list, ip_type, r_w_flag):
	address_str = None
	address_str_bak = None
	try:
		if r_w_flag == 1:
			address_str = get_random_address(address_list, ip_type)
			log_file("ADDRESS"+str(address_list))
			address_str_bak = get_random_address(address_list, 1 - ip_type)
		else:
			address_list_len = len(address_list)
			if address_list_len == 1:
				address_str_list = random.sample(address_list, 1)
				address_str = address_str_list[0][ip_type]
				address_str_bak = address_str_list[0][ip_type]
			elif address_list_len > 1:
				address_str_list = random.sample(address_list, 2)
				address_str = address_str_list[0][ip_type]
				address_str_bak = address_str_list[1][ip_type]
	except Exception, data:
		log_file(str(data))
		
	return address_str, address_str_bak

# get data from mapdb
def req_bin_server(host, port, req_str, log_id = 20130306 , timeout_usecs = 100000000) :
	#req_str = '{"keywords": [{"value": 202, "keyword": "二套房"}, {"value": 186, "keyword": "自有住房"}, {"value": 170, "keyword": "减免所得税"}, {"value": 113, "keyword": "首付"}, {"value": 108, "keyword": "二线"}, {"value": 107, "keyword": "换房"}, {"value": 98, "keyword": "所得税"}, {"value": 86, "keyword": "利率"}, {"value": 86, "keyword": "细则"}], "cate_info": [8404992, 0.51920299999999997, 0.84456299999999995], "num": 30}'
	print req_str
	address = (host, port)
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try :
		s.settimeout(timeout_usecs / 1000000.0)
		s.connect(address)
		head = struct.pack('IIII', len(req_str), log_id, 0, 0)
		ret = s.send(head)
		if ret != len(head) :
			s.close()
			return False
		send_num = 0
		while send_num < len(req_str) :
			ret = s.send(req_str[send_num:])
			if ret <= 0 :
				s.close()
				return False
			send_num += ret

		head = s.recv(16)
		body_len, log_id, tmp1, tmp2 = struct.unpack('IIII', head)
		if body_len == 0:
			data = ''
		else :
			recved_data = []
			recved_len = 0
			while recved_len < body_len:
				data = s.recv(body_len - recved_len)
				if len(data) <= 0:
					s.close()
					return False
				recved_data.append(data)
				recved_len += len(data)
			data = ''.join(recved_data)
		s.close()
		return data
	except Exception, e:
		log_file(str(e) + ":" + req_str + ":" + host + ":" + str(port))
		print "\n"
		print str(e) + ":" + req_str + ":" + host + ":" + str(port)
		pass

	s.close()
	return False

def transfer_split_char(split_char):
	if split_char.find("|") == -1:
		new_split_char = split_char
		if split_char == "0001":
			new_split_char = '\001'
		elif split_char == "0t":
			new_split_char = '\t'
		elif split_char == "0n":
			new_split_char = '\n'
		elif split_char == "0":
			new_split_char = ' '

		return new_split_char
	elif split_char == "|":
		return split_char
	else:
		split_list = split_char.split("|")

		new_all_split_char = ""
		for each in split_list:
			new_split_char = each
			if each == "0001":
				new_split_char = '\001'
			elif each == "0t":
				new_split_char = '\t'
			elif each == "0n":
				new_split_char = '\n'
			elif each == "0":
				new_split_char = ' '
			if new_all_split_char == "":
				new_all_split_char = new_split_char
			else:
				new_all_split_char = new_all_split_char + "|" + new_split_char

		return new_all_split_char

def spend_time(function, before_time, first_flag = False):
	cur_time = time.time()
	if first_flag:
		log_file(function + ":first_time!")
	else:
		log_file(function + ":" + str(cur_time - before_time))
		
	return cur_time
