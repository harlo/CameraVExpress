import os, re, json, base64
from subprocess import Popen, PIPE
from cStringIO import StringIO

def b64decode(content):
	try:
		return base64.b64decode(content)
	except TypeError as e:
		print e
		print "...so trying to decode again (brute-force padding)"
			
		try:
			return base64.b64decode(content + ("=" * ((4 - len(content) % 4) % 4)))
		except TypeError as e:
			print "could not unB64 this content: %s"  % e
	
	return None

def parse_video(vid, out_file):
	print "parsing video %s" % vid

	j3m_data = StringIO()

	cmd = ["ffmpeg", "-y", "-dump_attachment:t", vid, "-i"]
	print " ".join(cmd)

	p = Popen(cmd, stdout=PIPE, close_fds=True)
	data = p.stdout.readline()

	while data:
		data = data.strip()
		
		print data

		j3m_data.write(data)
		data = p.stdout.readline()

	p.stdout.close()

	try:
		j3m_data = b64decode(j3m_data.getvalue())
		print j3m_data

		if out_file is not None:
			with open(out_file, 'wb+') as OUT:
				OUT.write(j3m_data)

		return True
	except Exception as e:
		print e, type(e)

	return False