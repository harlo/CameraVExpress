import os, re, csv
from sys import argv, exit

def camerav_parser(file_description, out_dir=None):
	try:
		file_path, mime_type = parse_file_description(file_description)
	except Exception as e:
		print e, type(e)
		return False

	if not os.path.exists(file_path):
		print "bad input file"
		return False

	print file_path, mime_type

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
			print "Unpacking assets..."
			
			for idx, d in enumerate(output['data']):
				asset_mime_type = re.findall(r'.+\.(jpg|mkv)$', d)
				
				if len(asset_mime_type) == 1:
					print asset_mime_type
					if asset_mime_type[0] == "jpg":
						from image.parser import parse_image as parse_sub_media
					elif asset_mime_type[0] == "mkv":
						from video.parser import parse_video as parse_sub_media
					else:
						continue

					try:
						res, sub_output = parse_sub_media(os.path.abspath(d), out_dir=out_dir)
						if res:
							output['data'][idx] = sub_output
					except Exception as e:
						print e, type(e)

		return res, output
		
	except Exception as e:
		print "Could not parse media:"
		print e, type(e)

	return False

def parse_file_description(file_description):
	mime_type = get_mime_type(file_description)
	
	if mime_type is not None:
		fd = file_description.split(": ")
		if len(fd) == 2:
			return fd[0], mime_type

	return None

def get_mime_type(file_description):
	if re.match(r'.*JPEG image data(:?, EXIF standard)$', file_description):
		return "image"
	elif re.match(r'.*\.mkv: data$', file_description):
		return "video"
	elif re.match(r'.*\sZip archive data$', file_description):
		return "source"
	elif re.match(r'.*PGP message', file_description) or re.match(r'.*ASCII text', file_description):
		return "j3mlog"

	return None

def convert_to_csv(json_files):
	from json import loads
	print "***\n\nConverting J3M data to CSV format...\n\n***"

	if type(json_files) in [str, unicode]:
		json_files = [json_files]

	try:

		csv_files = []
		for json_file in json_files:
			with open(json_file, 'rb') as J:
				try:
					data = loads(J.read())
				except Exception as e:
					print e, type(e)
					continue

			if len(data.keys()) == 2 and ('j3m' in data.keys() and 'signature' in data.keys()):
				data = data['j3m']

			if 'sensorCapture' not in data['data'].keys() or 'userAppendedData' not in data['data'].keys():
				print "%s contains for real data for CSV" % json_file
				continue

			csv_file = "%s.csv" % json_file

			with open(csv_file, 'wb+') as C:
				csv_ = csv.writer(C, delimiter=',')
				csv_.writerow(['timestamp', 'sensor_type', 'sensor_value'])

				if 'sensorCapture' in data['data'].keys():
					for reading in data['data']['sensorCapture']:
						if 'sensorPlayback' in reading.keys() and 'timestamp' in reading.keys():
							for r in reading['sensorPlayback'].keys():
								csv_.writerow([reading['timestamp'], r, reading['sensorPlayback'][r]])

				if 'userAppendedData' in data['data'].keys():
					for uad in data['data']['userAppendedData']:
						if 'timestamp' in uad.keys() and 'associatedForms' in uad.keys():
							for a in [a['answerData'] for a in uad['associatedForms']]:
								for ad in a.keys():
									csv_.writerow([uad['timestamp'], ad, a[ad]])

			csv_files.append(csv_file)

		if len(csv_files) != 0:
			return True, csv_files

	except Exception as e:
		print e, type(e)

	return False

if __name__ == "__main__":
	if len(argv) not in [2, 3]:
		print "usage: camerav_express [media file] [mime_type] (--with-csv)"
		exit(-1)

	print argv
	res = False

	try:
		res, output = camerav_parser(argv[1])
		print_out = [
			"Mime Type : %(mime_type)s",
			"Original file : %(original_file)s",
			"Output data : %(data)s"
		]

		if len(argv) == 3 and argv[2] == "--with-csv":
			try:
				cres, csv_files = convert_to_csv(output['data'])

				if cres:
					print_out.append("Generated CSV files: %s" % csv_files)

			except Exception as e:
				print "Could not generate csv files."
				print e, type(e)

		print "***\n\n%s\n\n***" % ("\n".join([p % output for p in print_out]))
	except Exception as e:
		print e, type(e)

	exit(-1 if not res else 0)