import os, re, csv
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
	elif mime_type == "j3mlog":
		from log.parser import parse_j3mlog as parse_media

	try:
		res, output = parse_media(os.path.abspath(file_path), out_dir=out_dir)
		output = {
			'mime_type' : mime_type,
			'data' : output,
			'original_file' : file_path
		}

		if mime_type == "j3mlog" and type(output['data']) is list:
			unpacked_data = []
			for idx, d in enumerate(output['data']):
				asset_mime_type = re.match(r'.+\.(jpg|mkv)$', data)
				
				if asset_mime_type:
					try:
						output['data'][idx] = camerav_parser("image" if asset_mime_type == "jpg" else "mkv")
					except Exception as e:
						print e, type(e)

		return res, output
		
	except Exception as e:
		print e, type(e)

	return False

def get_mime_type(file_description):
	if re.match(r'.*JPEG image data$', file_description):
		return "image"
	elif re.match(r'.*\.mkv: data$', file_description):
		return "video"
	elif re.match(r'.*\sZip archive data$', file_description):
		return "source"
	elif re.match(r'.*PGP message', file_description) or re.match(r'.*ASCII text', file_description):
		return "j3mlog"

	return None

def convert_to_csv(json_files):
	if type(json_files) in [str, unicode]:
		json_files = [json_files]

	try:

		for json_file in json_files:
			with open(json_file, 'rb') as J:
				try:
					data = loads(J.read())
				except Exception as e:
					print e, type(e)
					continue

			with open("%s.csv" % json_file, 'wb+') as C:
				csv_ = csv.writer(C, delimiter=',')
				csv_.writerow(['timestamp', 'sensor_type', 'sensor_value'])

				for reading in data['data']['sensorCapture']:
					if 'sensorPlayback' in reading.keys() and 'timestamp' in reading.keys():
						for r in reading['sensorPlayback'].keys():
							csv_.writerow([reading['timestamp'], r, reading['sensorPlayback'[r]]])

				if 'userAppendedData' not in data['data'].keys():
					continue

				for uad in data['data']['userAppendedData']:
					if 'timestamp' in uad.keys() and 'associatedForms' in uad.keys():
						for a in [a['answerData'] for a in uad['associatedForms']]:
							for ad in a.keys():
								csv_.writerow([uad['timestamp'], ad, a[ad]])

			return True

	except Exception as e:
		print e, type(e)

	return False

if __name__ == "__main__":
	if len(argv) not in [3, 4]:
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

		if len(argv) == 4 and argv[3] == "--with-csv":
			convert_to_csv(output['data'])

		print "***\n\n%s\n\n***" % ("\n".join([p % output for p in print_out]))
	except Exception as e:
		print e, type(e)

	exit(-1 if not res else 0)