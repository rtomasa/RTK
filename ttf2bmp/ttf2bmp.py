#!/usr/bin/python

import os, sys, getopt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
try:
	import pygame
	from pygame.locals import *
except Exception as error:
	print(error,'\nPlease install the same to use this tool')
	sys.exit()

def main(argv):
	pygame.init()

	'''CLI arguments'''

	font_name = 'quarlow' # quarlow
	font_size = 16 # quarlow = 16
	font_color = 'fff1e8' # fff1e8 = (255,241,232)
	extra_w = 0 # makes the resulting char tiles wider
	extra_h = 0 # makes the resulting char tiles taller
	img_size = '320x240' # '320x240'
	bg_color = '00e436' # 00e436 = (0,228,54)
	charset_file = 'charset.txt'

	try:
		opts, args = getopt.getopt(argv,"?n:s:c:w:h:i:b:f:",["help","fntname=","fntsize=","fntcolor=","extraw=","extrah=","imgsize=","bgcolor=","charfile="])
	except getopt.GetoptError:
		print('ttf2bmp.py [options]\nExample: ttf2bmp.py -n quarlow -s 16 -c ff004d -w 2 -h 2 -i 256x256 -b 1d2b53\n-n, --fntname\tfont name i.e: quarlow\n-s, --fntsize\tfont size\n-c, --fntcolor\thex font color i.e: fff1e8\
			\n-w, --extraw\textra width\n-h, --extrah\textra heigh\n-i, --imgsize\timage size i.e: 320x240\
			\n-b, --bgcolor\thex background color i.e: 00e436\n-f, --charfile\tchar file, i.e: charset.txt\n-?, --help\tdisplay this help')
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-?", "--help"):
			print('ttf2bmp.py [options]\nExample: ttf2bmp.py -n quarlow -s 16 -c ff004d -w 2 -h 2 -i 256x256 -b 1d2b53\n-n, --fntname\tfont name i.e: quarlow\n-s, --fntsize\tfont size\n-c, --fntcolor\thex font color i.e: fff1e8\
			\n-w, --extraw\textra width\n-h, --extrah\textra heigh\n-i, --imgsize\timage size i.e: 320x240\
			\n-b, --bgcolor\thex background color i.e: 00e436\n-f, --charfile\tchar file, i.e: charset.txt\n-?, --help\tdisplay this help')
			sys.exit()
		elif opt in ("-n", "--fntname"):
			font_name = arg
		elif opt in ("-s", "--fntsize"):
			font_size = int(arg)
		elif opt in ("-c", "--fntcolor"):
			font_color = arg
		elif opt in ("-w", "--extraw"):
			extra_w = int(arg)
		elif opt in ("-h", "--extrah"):
			extra_h = int(arg)
		elif opt in ("-i", "--imgsize"):
			img_size = arg
		elif opt in ("-b", "--bgcolor"):
			bg_color = arg
		elif opt in ("-f", "--charfile"):
			charset_file = arg

	'''Font parameters'''

	img_w = int(img_size.split('x')[0])
	img_h = int(img_size.split('x')[1])
	font_color = tuple(int(font_color[i:i+2], 16) for i in (0, 2, 4))
	bg_color = tuple(int(bg_color[i:i+2], 16) for i in (0, 2, 4))
	font_file = font_name + '.ttf'
	out_dir = './output/'
	image_file = out_dir + font_name + ".bmp"
	font_data_file = out_dir + font_name + ".dat"

	'''Image parameters'''

	x = 0 + extra_w
	y = 0
	linemax = 0
	antialias = False
	
	'''Read all chars to be exported into the sprite sheet image'''

	chars = []
	charset_file = open(charset_file,"r")
	text = charset_file.read()
	for c in text:
		if c not in chars and c != '\n':
			chars.append(c)
	charset_file.close()
	chars.sort()
	chars = ''.join(chars)

	'''Generate sprite sheet image'''

	print("Try 'ttf2bmp -?' for more information.\n\nGenerating sprite sheet image...\n\n" + chars)
	sprite_sheet = pygame.surface.Surface((img_w, img_h))
	sprite_sheet.fill(bg_color)
	font = pygame.font.Font(font_file, font_size)
	fout = open(font_data_file,"w")
	for c in chars:
		charsurf = font.render(c, antialias, font_color)
		charsize = charsurf.get_size()
		char_w = charsize[0] + extra_w
		char_h = charsize[1] + extra_h
		if char_h > linemax:
			linemax = char_h
		if x + char_w > img_w:
			x = 0 + extra_w
			y += linemax
			linemax = 0
		sprite_sheet.blit(charsurf,(x, y))
		fout.write(c + "," + str(x-extra_w) + "," + str(y) + "," + str(char_w) + "," + str(char_h) + "\n")
		x += char_w
	pygame.image.save(sprite_sheet, image_file)
	fout.close
	print('\nDone!')

if __name__ == "__main__":
	main(sys.argv[1:])
