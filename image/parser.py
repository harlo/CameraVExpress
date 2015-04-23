import os, re, json
from subprocess import Popen, PIPE
from cStringIO import StringIO

def parse_image(img, out_dir=None):
	print "parsing image %s" % img

	out_file = "%s.j3m" % img

	if out_dir is not None:
		out_file = os.path.join(out_dir, out_file.split("/")[-1])
	
	j3m_data = StringIO()
	obscura_marker_found = False

	cmd = [os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib", "j3mparser.out"), img]

	p = Popen(cmd, stdout=PIPE, close_fds=True)
	data = p.stdout.readline()

	while data:
		data = data.strip()
		print data

		if re.match(r'^file: .*', data):
			pass
		elif re.match(r'^Generic APPn .*', data):
			pass
		elif re.match(r'^Component.*', data):
			pass
		elif re.match(r'^Didn\'t find .*', data):
			pass
		elif re.match(r'^Got obscura marker.*', data):
			obscura_marker_found = True
		else:
			if obscura_marker_found:
				j3m_data.write(data)

		data = p.stdout.readline()

	p.stdout.close()


	try:
		j3m_data = j3m_data.getvalue()

		with open(out_file, 'wb+') as OUT:
			OUT.write(j3m_data)

		return True, out_file
	except Exception as e:
		print e, type(e)

	return False