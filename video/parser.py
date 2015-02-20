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

def parse_video(vid):
	print "parsing video %s" % vid
	out_file = "%s.json" % vid

	cmd = ["ffmpeg", "-y", "-dump_attachment:t", out_file, "-i", vid]
	print " ".join(cmd)

	p = Popen(cmd, stdout=PIPE, close_fds=True)
	p.wait()

	if os.path.exists("%s.json" % vid):
		return True

	return False