#! /bin/bash

THIS_DIR=`pwd`
JPEG_TOOLS_DIR=$THIS_DIR/image/lib
VID_TOOLS_DIR=$THIS_DIR/video/lib

cd $JPEG_TOOLS_DIR/Jpeg-Redaction-Library/lib
make
g++ -L . -lredact jpeg.cpp jpeg_decoder.cpp jpeg_marker.cpp debug_flag.cpp byte_swapping.cpp iptc.cpp tiff_ifd.cpp tiff_tag.cpp j3mparser.cpp -o ../../j3mparser.out
make clean

cd $JPEG_TOOLS_DIR/JavaMediaHasher
ant compile dist
cp dist/JavaMediaHasher.jar $JPEG_TOOLS_DIR
ant clean

FFMPEG_VERSION=`which ffmpeg`
if [[ $FFMPEG_VERSION == *bin/ffmpeg ]]
then
	echo "ffmpeg already installed.  Skipping"
else
	cd $VID_TOOLS_DIR/FFmpeg
	./configure
	make
	sudo make install
	cd $THIS_DIR
fi