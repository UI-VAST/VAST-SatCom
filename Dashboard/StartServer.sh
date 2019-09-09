#!/bin/bash

LABEL=$1
DIRECTORY=$2
RISE_DIR=$(pwd)


#start LogReader through websocket on port 8080
cd $RISE_DIR/scripts/websocketd
./websocketd --port=8080 python $RISE_DIR/scripts/LogReader/LogReader.py -d $DIRECTORY/$LABEL &

#start PacketDownloader
cd $RISE_DIR/scripts/PacketDownloader
./PacketDownloader.py -l $LABEL -d $DIRECTORY &
#./fakePacketDownloader.py -d $DIRECTORY/$LABEL &
