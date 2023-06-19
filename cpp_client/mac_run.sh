#!/bin/bash

# Stop script on any error
set -e

# Clone the repository and enter its directory
git clone https://github.com/obgm/libcoap
cd libcoap/

# Install necessary packages
brew install libtool autoconf automake pkg-config

# Build libcoap
./autogen.sh
./configure --disable-doxygen --disable-manpages --disable-dtls
make
sudo make install

# Install SDL2 dev library
brew install sdl2

# Export library path
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# Compile your program
CPP_FILES="main.cpp Controller.cpp MessageQueue.cpp Process.cpp CoAPSender.cpp common.o"
cd ..
g++ -c common.cc
g++ -o my_program $CPP_FILES -I/opt/homebrew/Cellar/sdl2/2.26.5/include/SDL2/ -L/opt/homebrew/Cellar/sdl2/2.26.5/lib/ -lSDL2 -lpthread -lcoap-3

# Run your program
./my_program 