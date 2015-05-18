from subprocess import Popen, PIPE

gpg_sentinel = ["-----BEGIN PGP MESSAGE-----", "Version: BCPG v@RELEASE_NAME@"]

def decrypt_file(infile, outfile):
	cmd = ["gpg", "--yes", "--output", outfile, "--decrypt", infile]

	p = Popen(cmd, stdout=PIPE, close_fds=True)
	data = p.stdout.readline()

	while data:
		data = data.strip()
		data = p.stdout.readline()
	p.stdout.close()