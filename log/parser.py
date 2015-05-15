import re, os
from base64 import b64encode
from subprocess import Popen, PIPE

def get_log_data(from_file):
	log_data = None

	try:
		with open(from_file, 'rb') as L:
			log_data = L.read()
			return log_data
	except Exception as e:
		print e, type(e)

	return None

def parse_j3mlog(log, out_dir=None):
	print "parsing j3m log %s" % log

	log_data = get_log_data(log)

	log_alias = log
	last_state = log

	out_file = "%s.unzipped" % log

	if out_dir is not None:
		out_file = os.path.join(out_dir, log.split("/")[-1])
	else:
		out_dir = os.path.dirname(log)

	# is it b64'd? (i.e. starts with LS0tblahblah)
	gpg_sentenel = ["-----BEGIN PGP MESSAGE-----", "Version: BCPG v@RELEASE_NAME@"]
	
	if log_data.split('\n')[0] == b64encode('\n'.join(gpg_sentenel)):
		print "Now un-b64ing..."

		log_alias = "%s.unb64ed" % log_alias

		# if so, un-b64
		cmd = ["base64", "-D", "-i", last_state, "-o", os.path.join(out_dir, log_alias)]

		p = Popen(cmd, stdout=PIPE, close_fds=True)
		data = p.stdout.readline()

		while data:
			data = data.strip()
			data = p.stdout.readline()
		p.stdout.close()

		last_state = log_alias
		log_data = get_log_data(last_state)

	# is it pgp? (i.e. starts with BEGIN PGP MESSAGE)
	if log_data.split('\n')[:2] == gpg_sentenel:
		print "Now decrypting..."

		log_alias = "%s.decrypted" % log_alias

		# if so, prompt user to decrypt
		cmd = ["gpg", "--yes", "--output", os.path.join(out_dir, log_alias), \
			"--decrypt", last_state]

		p = Popen(cmd, stdout=PIPE, close_fds=True)
		data = p.stdout.readline()

		while data:
			data = data.strip()
			data = p.stdout.readline()
		p.stdout.close()

		last_state = log_alias
		log_data = get_log_data(last_state)

	# finally, unzip
	try:
		print "Now unzipping..."
		cmd = ["unzip", "-o", last_state, "-d", out_file]

		p = Popen(cmd, stdout=PIPE, close_fds=True)
		data = p.stdout.readline()

		while data:
			data = data.strip()
			data = p.stdout.readline()
		p.stdout.close()
	except Exception as e:
		print e, type(e)
		return False

	for r, _, files in os.walk(out_file):
		files = [os.path.join(r, f) for f in files]
		break

	return True, files

