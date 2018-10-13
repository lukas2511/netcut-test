#/usr/bin/env python3

import os
import glob
import datetime
import subprocess
import sys

p = "cccb-"
c = "/video/capture/geekend2018/cccb"
st = "2018-10-06_21-50-00"

def parse_datetime(i):
    parts = i.replace('_', '-').split('-')

    return datetime.datetime(
            year=int(parts[0]),
            month=int(parts[1]),
            day=int(parts[2]),
            hour=int(parts[3]),
            minute=int(parts[4]),
            second=int(parts[5]))

def generate_preview(capturefile, previewfile):
    command = [
        "/usr/bin/ffmpeg", "-v", "verbose", # "-y",
#        "-re",
        "-i", capturefile,
        "-init_hw_device", "vaapi=hw1:/dev/dri/renderD128", "-filter_hw_device", "hw1",
        "-filter_complex", "[0:v] hwupload,scale_vaapi=w=640:h=-2:format=nv12 [scaled]",
        "-map", "[scaled]", "-c:v:0", "h264_vaapi", "-profile:v:0", "578", "-level:v:0", "30", "-b:v:0", "1M", "-maxrate:v:0", "1M", "-keyint_min:v:0", "5", "-bf:v:0", "0", "-g:v:0", "5",
        "-map", "0:a:0", "-c:a:0", "aac", "-b:a:0", "48k", "-ac:a:0", "2", "-ar:a:0", "48000",
        previewfile
    ]
    print("Generating %s" % previewfile)
    try:
        subprocess.call(command)
        print("Done generating %s" % previewfile)
    except KeyboardInterrupt:
        os.unlink(previewfile)
        print("Aborted generating %s" % previewfile)
        sys.exit(0)
    except:
        os.unlink(previewfile)
        print("Error generating %s" % previewfile)

def main():
    capturefiles = sorted(glob.glob(c + "/" + p + "*.ts"))
    startdate = parse_datetime(st)

    for capturefile in capturefiles:
        previewfile = capturefile.replace("/video/capture", "/video/preview")

        if not os.path.exists(previewfile):
            date = parse_datetime(os.path.basename(capturefile)[len(p):])
            if date < (startdate - datetime.timedelta(seconds=180)):
                continue
            if (datetime.datetime.now() - date) < datetime.timedelta(seconds=180):
                continue
            generate_preview(capturefile, previewfile)

if __name__ == '__main__':
    main()
