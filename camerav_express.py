import os, re
from sys import argv, exit

def camerav_parser(file_description, file_path, out_dir=None):
	if not os.path.exists(file_path):
		print "bad input file"
		return False

	mime_type = get_mime_type(file_description)

	if mime_type == "image":
		from image.parser import parse_image as parse_media
	elif mime_type == "video":
		from video.parser import parse_video as parse_media
	elif mime_type == "source":
		from source.parser import parse_source as parse_media

	try:
		res, output = parse_media(os.path.abspath(file_path), out_dir=out_dir)
		output = {
			'mime_type' : mime_type,
			'data' : output,
			'original_file' : file_path
		}

		return res, output
		
	except Exception as e:
		print e, type(e)

	return False

def get_mime_type(file_description):
	if re.match(r'.*JPEG image data', file_description):
		return "image"
	elif re.match(r'.*\.mkv: data', file_description):
		return "video"
	elif re.match(r'.*\sZip archive data', file_description):
		return "source"

	return None

if __name__ == "__main__":
	if len(argv) != 3:
		print "usage: camerav_express [mime_type] [media file]"
		exit(-1)

	res = False

	try:
		res, output = camerav_parser(argv[1], argv[2])
		print_out = [
			"Mime Type : %(mime_type)s",
			"Original file : %(original_file)s",
			"Output data : %(data)s"
		]

		print "***\n\n%s\n\n***" % ("\n".join([p % output for p in print_out]))
	except Exception as e:
		print e, type(e)

	exit(-1 if not res else 0)