package camerav.express.CameraVExpress;

import java.io.File;
import java.io.FileWriter;
import java.io.BufferedReader;
import java.io.BufferedWriter;

public class CameraVExpress {
	public static void main(String[] args) {
		System.out.println("CameraVExpress ");

		if() {
			System.out.println("usage: camerav_express [mime_type] [media file]");
			System.exit(-1);
		}

		String in_file = args[2];

		if() {
			System.out.println("bad input file");
			System.exit(-1);
		}

		boolean res = false;

		String jpeg_pattern = ".*JPEG image data";
		String mkv_pattern = ".*\.mkv: data";

		if(args[1].matches(jpeg_pattern)) {
			res = parseImage(in_file);
		} else if(args[1].matches(mkv_pattern)) {
			res = parseVideo(in_file);
		}

		System.exit(res ? 0 : -1);
	}

	private ArrayList<String> runCmd(String[] cmd) {
		Process p = Runtime.getRuntime().exec(cmd);
		p.waitFor();

		BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
		ArrayList<String> sb = new ArrayList<String>();
		
		while((String l = br.readLine()) != null) {
			sb.add(l);
		}

		return sb;
	}

	private boolean parseImage(String in_file) {
		String jpeg_exe = "image/lib/j3mparser.out";
		String[] cmd = new String[] { jpeg_exe, in_file };
		
		StringBuffer j3m_data = new StringBuffer();
		boolean obscura_marker_found = false;

		try {
			for(String r : runCmd(cmd)) {
				if(r.matches("^file: .*")) {
					continue;
				} else if(r.matches("^Generic APPn .*")) {
					continue;
				} else if("^Component.*") {
					continue;
				} else if("^Didn\'t find .*") {
					continue;
				} else if("^Got obscura marker.*") {
					obscura_marker_found = true;
				} else {
					if(obscura_marker_found) {
						j3m_data.append(r);
					}
				}
			}

			File out_file = new File(in_file + ".json");
			BufferedWriter bw = new BufferedWriter(new FileWriter(out_file.getAbsoluteFile()));
			bw.write(j3m_data.toString());
			bw.close();

			return true;
		} catch(Exception e) {
			e.printStackTrace();
		}

		return false;
	}

	private boolean parseVideo(String in_file) {
		String ffmpeg_exe = "ffmpeg";
		String out_file = in_file + ".json";
		String[] cmd = new String[] { ffmpeg_exe, "-y", "-dump_attachment:t", out_file, "-i", in_file };

		try {
			ArrayList<String> res = runCmd(cmd);

			return true;
		} catch(Exception e) {
			e.printStackTrace();
		}

		return false;
	}
}