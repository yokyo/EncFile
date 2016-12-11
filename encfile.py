#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import hashlib
import base64
import mmap
import argparse
from contextlib import closing


"""
Simple file(s) encoder. a decoder included.
"""
ENC_FLAG= 'FBJ'			# encoded file flag, in header field. This flag must bind to ENC_VER
ENC_VER= "001"			# encoder/decoder version
ENC_EXT= ".ixb"			# encoded file extension. could be change.


# before encode, generate new file header
def _make_header(filename):
	name= os.path.basename(filename)
	_, ext= os.path.splitext(name)
	b64name= base64.b64encode(name)
	header_len=6+ 8+ len(b64name)
	return '%s%s%03d%02d%03d%s' % (ENC_FLAG,ENC_VER,header_len,len(ext),len(b64name),b64name)

# after encode, rename it for secret
def _enc_rename(src):
	d= os.path.dirname(src)
	name= os.path.basename(src)
	new_name= hashlib.md5(name).hexdigest()+ ENC_EXT
	dest= os.path.join(d,new_name)
	os.rename(src,dest)

## encode a file
## file size is 513 at least.
## new header-format:  'enc','001',header_len(3),ext_len(2),name_len(3),source_name(n)
def enc(filename):
	done=False
	with open(filename,"a+b") as f:
		size=os.path.getsize(filename)

		if size < 512:
			print 'File too short to encode[%d], quit' % size
			return False

		header= _make_header(filename)
		header_len= len(header)

		oheader= f.read(header_len)

		with closing(mmap.mmap(f.fileno(),header_len)) as m:
			m[0:]= header

		f.seek(os.SEEK_END)
		f.write(oheader)
		done = True

	if done:
		_enc_rename(filename)
		return True


## decode a file which encoded by function enc
##
def dec(filename):
	d = os.path.dirname(filename)
	name= os.path.basename(filename)
	size= os.path.getsize(filename)
	done=False
	with open(filename,"a+b") as f:
		h= f.read(14)
		if h[0:3] != ENC_FLAG:
			print "%s is not a encoded file." % name
			return False
		ver= h[3:6]
		header_len= int(h[6:9])
		ext_len= int(h[9:11])
		name_len= int(h[11:])
		name= f.read(name_len)

		f.seek(-header_len,os.SEEK_END)
		ohead= f.read()

		with closing(mmap.mmap(f.fileno(),header_len)) as m:
			m[0:]= ohead

		f.truncate(size-header_len)
		done=True;
	if done:
		sname= base64.b64decode(name)
		fullname= os.path.join(d,sname)
		os.rename(filename,fullname)

## process user input parameters, handler properly.
def handle_args(args):
	support_oper = ['enc', 'dec']  # Better make it global var

	if args.oper not in support_oper:
		print "not supported operation:"+ args.oper
		return

	proper= os.path.isdir if args.recursive else os.path.isfile
	if not proper(args.fd):
		print "parameter error."
		return

	if args.recursive:
		for r,d,f in os.walk(args.fd):
			for ff in f:
				fn= os.path.join(r,ff)
				eval(args.oper)(fn)
	else:
		eval(args.oper)(args.fd)

# main
if __name__ == '__main__':

	# xxx dec/enc [-R dir | file]
	parser= argparse.ArgumentParser(description="Encode/Decode binary file(s).")
	parser.add_argument("oper",help="dec/enc")
	parser.add_argument("fd",help="file or directory(with -R)")
	parser.add_argument("-R","--recursive",help="with this flag,one can encode/decode a directory recursively.",action="store_true")
	args= parser.parse_args()

	handle_args(args)

