#! /bin/bash

THIS_DIR=`pwd`
JPEG_TOOLS_DIR=$THIS_DIR/image/lib

cd $JPEG_TOOLS_DIR/Jpeg-Redaction-Library/lib
make
g++ -L . -lredact jpeg.cpp jpeg_decoder.cpp jpeg_marker.cpp debug_flag.cpp byte_swapping.cpp iptc.cpp tiff_ifd.cpp tiff_tag.cpp j3mparser.cpp -o ../../j3mparser.out
make clean

cd $JPEG_TOOLS_DIR/JavaMediaHasher
ant compile dist
cp dist/JavaMediaHasher.jar $JPEG_TOOLS_DIR
ant clean