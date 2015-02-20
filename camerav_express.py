import os, re
from sys import argv, exit

if __name__ == "__main__":
	if len(argv) != 3:
		print "usage: camerav_express [mime_type] [media file]"
		exit(-1)

	if not os.path.exists(argv[2]):
		print "bad input file"
		exit(-1)

	res = False

	print argv[1]

	if re.match(r'.*JPEG image data', argv[1]):
		from image.parser import parse_image as parse_media
	elif re.match(r'.*\.mkv: data', argv[1]):
		from video.parser import parse_video as parse_media

	try:
		res = parse_media(os.path.abspath(argv[2]))
	except Exception as e:
		print e, type(e)

	exit(-1 if not res else 0)