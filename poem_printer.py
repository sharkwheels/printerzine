#!/usr/bin/python3

######################
# Simple Poem Printer to play around with form
# Nadine Lessio
# June2019
# scp poem_printer.py pi@172.25.1.3:/home/pi/Projects/poems/
######################

from __future__ import print_function
import random
import textwrap
import time
import glob
from random import choice
from threading import Thread
from PIL import Image
from datetime import datetime
from thermalprinter import *

from hux_poems import huxPoems
from ren_poems import renPoems




## PRINTER DECLARATION ######################
try:
	printer = ThermalPrinter(port="/dev/cu.usbserial-A4016WUR", baudrate=9600, timeout=5, heat_time=200, heat_interval=5, most_heated_point=200)
except:
	print("no printer")
	print("")
	print("")

## Appendix and Images ######################
appendix_array = [
	("WTF is Kylux?",
"""Kylux is the pairing of Kylo Ren and General Hux from the Star Wars Sequel Trilogy, and is a popular "trash ship" in the star wars fandom. While Kylux has grown to include a wide variety of content (trashy, funny, fluffy or otherwise) it can still be problematic and there's a lot of discussion around it both in and outside of fandom. If you're curious about Kylux here are some starting points:\n
	SGG - Overview + Discourse: 
	intro (2016)
	youtu.be/4hxIbYtimls
	update (2018)
	youtu.be/2b6zeibK8rI\n
	Polygon - SW Ships:
	tinyurl.com/polygonkylux\n
	Rogues Portal - Trashcans:
	tinyurl.com/rogueskylux\n
	Newcomer's Guide to Kylux:
	tinyurl.com/kyluxnewbies\n
	Vox-Shipping Tropes:
	tinyurl.com/voxshipmeme\n
	Stats By Toast:
	tinyurl.com/toaststats
	"""),
	("How Are These Made?",
		"""These tiny fics were made using GPT2's base conditional sample generation mode with some very strict variables. Some fic structures came back almost complete, some I edited for readability. This was less about trying to generate long form convincing fanfic, and more about exploring "undesirable results" (looping and repetition), and how that can reflect on a source material."""),
	("Source Material?",
		"""The bulk of these were generated using passages hand picked out from the fanfic Finitum. Its mostly angsty, and doomed. You can read it here: tinyurl.com/finitum.\n
		A few were also based on this chapter of short one shots: 
		tinyurl.com/30daysbitter"""),
	("Will You Do More?", """Yes! I'm for sure going to do a set for Stormpilot. After that we'll see."""),
	("Contact","""twitter: @_nadine""")
	]

def getImages():
	img_list = []
	for filename in glob.glob('images/*.png'): 
		im = Image.open(filename)
		#im.thumbnail((95,95))
		img_list.append(im)
	return img_list

image_list = getImages()
#print(image_list)


############### ON SCREEN TESTING #######################	

def printOnScreen(text):
	title = text[0]
	poem = text[1].split('\n')
	poem = [x for x in poem if x.strip()]
	tp = "{0}{1}{2}".format("_.__++ ",title," ++_.__")
	print("{:^32}".format(tp))
	print("")
	for i in poem:
		d = textwrap.dedent(i).strip()
		w = textwrap.fill(d,width=32)
		print("{0}{1}".format(w,"\n"))
	print("")
	print("")
	
def printPrimerOnScreen(text):
	title = text[0]
	body = text[1].replace('\t','').split('\n')
	tp = "{0}{1}{2}".format("++ ",title," ++")
	print("{:^32}".format(tp))
	print("")
	for i in body:
		w = textwrap.fill(i,width=32)
		print("{0}".format(w))
	print("")
	print("")
	

def onScreenMake(h,r,x):
	""" Make the Zine for On Screen """
	random.seed(datetime.now())
	random.shuffle(h)
	random.shuffle(r)
	t = "+++ FIXATIONS [0.{0}] +++".format(x)
	## zine title 
	print("{:^32}".format("-"*20))
	print("")
	print("{:^32}".format(t))
	print("{:^32}".format("A Generated Kylux Tinyfic Zine"))
	print("")

	## zine contents ########
	print("«« Hux »»")
	print("")
	for c, value in enumerate(h, 1):
		print("{0} {1}".format(c,value[0]))
	print("")
	print("«« Ren »»")
	print("")
	for c, value in enumerate(r, 1):
		print("{0} {1}".format(c,value[0]))
	print("")
	print("{:^32}".format("Explanations and links can be found in the Appendix at the end."))
	print("")
	print("{:^32}".format("-"*20))
	print("")
	print("")

	## Hux ########	
	print("{:^32}".format("+++ "+"HUX"+" +++"))
	print("")
	print("")
	for i in h:
		printOnScreen(i)

	## Ren ########	
	print("{:^32}".format("+++ "+"REN"+" +++"))
	print("")
	print("")
	for i in r:
		printOnScreen(i)
	
	print("{:^32}".format("-"*20))
	print("")
	
	## appendix #######
	print("{:^32}".format("+++ "+"APPENDIX"+" +++"))
	print("")
	print("")
	for i in appendix_array:
		printPrimerOnScreen(i)
	print("{:^32}".format("-"*20))
	print("")
	
############### PRINTER #######################	

def printOne(text):
	title = text[0]
	poem = text[1].split('\n')
	poem = [x for x in poem if x.strip()]
	tp = "{0}{1}{2}".format("_.__++ ",title," ++_.__")
	printer.out("{:^32}".format(tp),bold=True)
	printer.feed(1)
	for i in poem:
		d = textwrap.dedent(i).strip()
		w = textwrap.fill(d,width=32)
		printer.out("{0}{1}".format(w,"\n"))
	printer.feed(1)

def printAppenix(text):
	title = text[0]
	body = text[1].replace('\t','').split('\n')
	tp = "{0}{1}{2}".format("++ ",title," ++")
	printer.out("{:^32}".format(tp))
	printer.feed(1)
	for i in body:
		w = textwrap.fill(i,width=32)
		printer.out("{0}".format(w))
	printer.feed(1)

def printZine(h,r,x):
	""" Print The Zine """
	random.seed(datetime.now())
	random.shuffle(h)
	random.shuffle(r)
	
	## zine title 
	title = "+++ FIXATIONS [0.{0}] +++".format(x)
	printer.out("{:^32}".format("-"*20),bold=True)
	printer.feed(1)
	printer.out("{:^32}".format(title),bold=True)
	printer.out("{:^32}".format("A Generated Kylux Tinyfic Zine"))
	printer.feed(1)

	## zine contents ########
	printer.out("{:^32}".format("«««« Hux »»»»"))
	printer.feed(1)
	for c, value in enumerate(h, 1):
		t = "{0} {1}".format(c,value[0])
		printer.out("{0} {1}".format(c,value[0]),justify='C')
	printer.feed(1)
	printer.out("{:^32}".format("«««« Ren »»»»"))
	printer.feed(1)
	for c, value in enumerate(r, 1):
		t = "{0} {1}".format(c,value[0])
		printer.out("{0} {1}".format(c,value[0]),justify='C')
	printer.feed(1)
	printer.out("{:^32}".format("-"*20),bold=True)
	printer.feed(1)
	
	## hux #######
	printer.out("{:^32}".format("+++ "+"HUX"+" +++"),bold=True)
	printer.feed(1)
	for i in h:
		printOne(i)
		time.sleep(2)
	
	time.sleep(5)
	printer.image(random.choice(image_list))
	#printer.image(image_list[1]) #snake
	printer.feed(1)

	## ren #######
	printer.out("{:^32}".format("+++ "+"REN"+" +++"), bold=True)
	printer.feed(1)
	for i in r:
		printOne(i)
		time.sleep(2)

	printer.out("{:^32}".format("-"*20))
	printer.feed(1)
	time.sleep(2)

	## appendix #######
	printer.out("{:^32}".format("+++ "+"APPENDIX"+" +++"),bold=True)
	printer.feed(1)
	for i in appendix_array:
		printAppenix(i)
	printer.out("{:^32}".format("-"*20),bold=True)
	printer.feed(2)


############### RUN IT #######################

printOne(renPoems[1])
	
#onScreenMake(huxPoems[:4],renPoems[:4],1)
#onScreenMake(huxPoems[4:8], renPoems[4:8],2)
#

#print(len(image_list))
#printZine(huxPoems[:4], renPoems[:4],1)
#printZine(huxPoems[4:8], renPoems[4:8],2)

#printer.image(random.choice(image_list))
"""
for i in image_list:
	printer.image(i)
	time.sleep(2)
"""