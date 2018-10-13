#/usr/bin/env python3

import os
import glob
import datetime
import subprocess
import sys

#mount = "/video/fuse//geekend/Saal23/1337"
#c = "/video/preview/cccb/Saal23"
#p = "saal23-"
#st = "2018-10-06_21-40-00"
#numfiles = "40"

p = "cccb-"
c = "/video/capture/geekend2018/cccb"
st = "2018-10-06_21-50-00"
numfiles = "12"
totalframes = "49500"
mount = "/video/fuse//geekend2018/CCCB/1"

FILE_LENGTH = 180

def parse_datetime(i):
    parts = i.replace('_', '-').split('-')

    return datetime.datetime(
            year=int(parts[0]),
            month=int(parts[1]),
            day=int(parts[2]),
            hour=int(parts[3]),
            minute=int(parts[4]),
            second=int(parts[5]))

def main():
    global numfiles
    previewfiles = sorted(glob.glob(c.replace("/video/capture", "/video/preview") + "/" + p + "*.ts"))
    startdate = parse_datetime(st)

    usedfiles = 0
    numfiles = int(numfiles)
    firstfile = None

    snippets = []

    for previewfile in previewfiles:
        date = parse_datetime(os.path.basename(previewfile)[len(p):])
        print(previewfile)
        if date < startdate:
            print("skip1")
            continue
        if usedfiles >= numfiles:
            print("skip2")
            break
        if (datetime.datetime.now() - date) < datetime.timedelta(seconds=180):
            print("skip3")
            continue
        if date > (startdate + (1 + usedfiles) * datetime.timedelta(seconds=180)):
            print("skip4")
            continue
        snippets.append(previewfile)
        if usedfiles == 0:
            firstfile = date
        usedfiles += 1
        print("used")

    previewdir = mount.replace("/video/fuse", "/video/preview")
    command = ["/usr/bin/ffmpeg",
        "-v", "verbose", # "-y",
#        "-ss", "%.5f" % (startdate - firstfile).total_seconds(),
        "-i", "concat:" + "|".join(snippets),
        "-map", "0",
        "-c:v", "copy",
        "-c:a", "copy",
        "-hls_time", "30",
        "-hls_playlist_type", "vod",
        "-hls_segment_filename", previewdir + "/snippet%04d.ts",
        previewdir + "/playlist.m3u8",
    ]
    #print(subprocess.list2cmdline(command))
    subprocess.call(command)

if __name__ == '__main__':
    main()
