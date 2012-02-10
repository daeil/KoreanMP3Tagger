#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from mutagen.easyid3 import EasyID3
from mutagen import id3

TAGS = 'title','artist','album','performer'
RETAGS = 'album','performer'

def help():
	print 'Usage: %s [OPTION]... [FILE]' % sys.argv[0]
	print 'MP3 tag update about the FILEs (the current directory by default).'
	print 'FILE may be a name of mp3 file or directory'


def euckr2utf8(euckr):
	try:
		euckr = euckr.encode('iso8859-1').decode('euc-kr')
	except:
		pass
	return euckr


def toUnicode(uc):
	if type(uc) is not unicode:
		return uc.decode('utf-8')
	return euckr2utf8(uc)

def addDummyTag(filename, tag):
	t = id3.ID3()
	f = id3.Frames['TXXX'](encoding=3, text=u'Dummy')
	t.loaded_frame(f)
	t.save(filename)



def getValue(filename, tag):
	try:
		mp3 = EasyID3(filename)
	except id3.ID3NoHeaderError:
		addDummyTag(filename, tag)

	try:
		value = mp3[tag][0]
		if value == 'Unknown' and tag in RETAGS:
			value = mp3['artist'][0]
	except:
		print '!!!', filename, tag
		if tag in RETAGS:
			return mp3['artist'][0]
		value = raw_input('please input [%s] value: ' % tag)
	return value


def putValue(filename, tag, value):
	mp3 = EasyID3(filename)
	mp3[tag] = value
	mp3.save()

def changeName(filename):
	artist = getValue(filename, 'artist').encode('utf-8')
	title = getValue(filename, 'title').encode('utf-8')
	newname = ('%s-%s.mp3' % (artist, title)).translate(None, '/\\?%*:|"<>')
	name = os.path.basename(filename)
	newfile = os.path.realpath(filename).replace(name, newname)
	os.rename(filename, newfile)
	print 'move: %s -> %s' % (filename, newfile)


def updateTag(filename):
	print filename
	if not filename.endswith(('.mp3', 'MP3')):
		return
	for tag in TAGS:
		if not tag:
			continue
		t = getValue(filename, tag)
		s = toUnicode(t)
		putValue(filename, tag, s)
	#changeName(filename)

def dirupdate(name):
	for f in os.listdir(name):
		t = os.path.join(name, f)
		if os.path.isdir(t):
			dirupdate(t)
		else:
			updateTag(t)


def main(name):
	if os.path.isdir(name):
		dirupdate(name)
	else:
		updateTag(name)


if __name__ == "__main__":
	if len(sys.argv) == 2:
		main(sys.argv[1])
	else:
		help()

