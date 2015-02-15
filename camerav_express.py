import os
from sys import argv, exit

if __name__ == "__main__":
	if len(argv) not in [3, 4]:
		print "usage: camerav_express [mime_type] [media file] [output file]"
		exit(-1)

	if not os.path.exists(argv[2]):
		print "bad input file"
		exit(-1)

	res = False
	if argv[1] == "image":
		from image.parser import parse_image as parse_media

	try:
		res = parse_media(os.path.abspath(argv[2]), None if len(argv) is 3 else os.path.abspath(argv[3]))
	except Exception as e:
		print e, type(e)

	exit(-1 if not res else 0)


