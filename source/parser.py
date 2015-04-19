import os, re
from subprocess import Popen, PIPE

BASH_CMD = {
	'LIST_ARCHIVE' : "unzip -l %s",
	'UNZIP' : "unzip -o %s -d %s",
	'MKDIR' : "mkdir %s"
}

def parse_source(source, out_dir=None):
	print "parsing source %s" % source
	

	cmd = (BASH_CMD['LIST_ARCHIVE'] % source).split(" ")
	print " ".join(cmd)

	p = Popen(cmd, stdout=PIPE, close_fds=True)
	if p.wait() != 0:
		return False

	for a in p.stdout.read().split('\n'):
		if len(re.findall(r'\d+\s+\d+-\d+-\d+\s+\d+:\d+\s+(.*)', a.strip())) == 1:
			if not re.match(r'.*\s+(?:baseImage_\d|publicKey|credentials)', a.strip()):
				print "Invalid zip: unknown file in archive."
				return False

	if out_dir is None:
		out_dir = source.replace(".zip", "")
	else:
		out_dir = os.path.join(out_dir, source.split("/")[-1])
	
	cmd = (BASH_CMD['MKDIR'] % out_dir).split(" ")
	p = Popen(cmd, stdout=PIPE, close_fds=True)
	if p.wait() != 0:
		return False

	cmd = (BASH_CMD['UNZIP'] % (source, out_dir)).split(" ")
	p = Popen(cmd, stdout=PIPE, close_fds=True)
	if p.wait() == 0:
		return True, out_dir


	return False