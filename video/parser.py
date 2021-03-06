import os, re, json, base64
from subprocess import Popen, PIPE
from cStringIO import StringIO

from utils.gpg import decrypt_file, gpg_sentinel

BASH_CMD = {
	'DUMP_ATTACHMENT' : "ffmpeg -y -dump_attachment:t %s -i %s"
}

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

def parse_video(vid, out_dir=None):
	print "parsing video %s" % vid
	out_file = "%s.j3m" % vid

	if out_dir is not None:
		out_file = os.path.join(out_dir, out_file.split("/")[-1])

	cmd = (BASH_CMD['DUMP_ATTACHMENT'] % (out_file, vid)).split(" ")

	p = Popen(cmd, stdout=PIPE, close_fds=True)
	p.wait()

	if not os.path.exists(out_file):
		return False

	with open(out_file, 'rb') as J:
		j3m_data = J.read()

	if j3m_data.split('\n')[:2] == gpg_sentinel:
		print "Now decrypting..."

		j3m_asc = "%s.asc" % out_file
		with open(j3m_asc, 'wb+') as OUT:
			OUT.write(j3m_data)

		decrypt_file(j3m_asc, out_file)
		
	return True, out_file

