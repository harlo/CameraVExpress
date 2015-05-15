import re, os
from subprocess import Popen, PIPE

def parse_j3mlog(log, out_dir=None):
	print "parsing j3m log %s" % log

	out_zip = "%s.zip" % log
	log_name = log.split("/")[-1]

	if out_dir is not None:
		out_file = os.path.join(out_dir, out_zip)

	j3m_log = None

	try:
		with open(out_file, 'rb') as L:
			j3m_log = L.read()
	except Exception as e:
		print e, type(e)

	if j3m_log is None:
		return False

	# is it b64'd? (i.e. starts with LS0T)
	if j3m_log[:4] == "LS0T":

		# if so, un-b64
		cmd = ["base64", "-d", os.path.join(out_dir, log_name)]

		p = Popen(cmd, stdout=PIPE, close_fds=True)
		data = p.stdout.readline()

		while data:
			data = data.strip()
			print data


			data = p.stdout.readline()
		p.stdout.close()


	# is it pgp? (i.e. starts with BEGIN PGP MESSAGE)
	if j3m_log.splitlines()[1] == "-----BEGIN PGP MESSAGE-----":

		# if so, prompt user to decrypt
		cmd = ["gpg", "--yes", "--output", os.path.join(out_dir, log_name), \
			"--decrypt", log]

		p = Popen(cmd, stdout=PIPE, close_fds=True)
		data = p.stdout.readline()

		while data:
			data = data.strip()
			print data

			data = p.stdout.readline()
		p.stdout.close()

	# finally, unzip
	try:
		cmd = ["unzip", "-o", os.path.join(out_dir, log_name), \
			"-d", os.path.join(out_dir, "%s_unzipped" % log_name)]

		p = Popen(cmd, stdout=PIPE, close_fds=True)
		data = p.stdout.readline()

		while data:
			data = data.strip()
			print data

			data = p.stdout.readline()
		p.stdout.close()
	except Exception as e:
		print e, type(e)
		return False

	for r, _, files in os.walk(os.path.join(out_dir, "%s_unzipped" % log_name)):
		files = [os.path.join(r, f) for f in files]
		break

	return True, files

