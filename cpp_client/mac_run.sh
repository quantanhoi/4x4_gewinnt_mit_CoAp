#!/bin/bash

# Stop script on any error
#set -e
set -x #for debugging

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Homebrew could not be found, please install it. See: https://brew.sh"
    exit 1
fi

# Check if git is installed
if ! command -v git &> /dev/null; then
    brew install git
fi

# Clone the repository and enter its directory
if [ ! -d "libcoap" ]; then
    git clone https://github.com/obgm/libcoap
    cd libcoap/
    
    # Check if libtool, autoconf, automake and pkg-config are installed
    brew list libtool &> /dev/null || brew install libtool
    brew list autoconf &> /dev/null || brew install autoconf
    brew list automake &> /dev/null || brew install automake
    brew list pkg-config &> /dev/null || brew install pkg-config

    # Build libcoap
    ./autogen.sh
    ./configure --disable-doxygen --disable-manpages --disable-dtls
    make
    sudo make install
    cd ..
fi

# Check if SDL2 dev library is installed
brew list sdl2 &> /dev/null || brew install sdl2

# Export library path
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# Compile your program
CPP_FILES="main.cpp Controller.cpp MessageQueue.cpp Process.cpp CoAPSender.cpp common.o ControllerMessage.cpp logging.cpp"
g++ -c common.cc
g++ -c ControllerMessage.cpp
g++ -c logging.cpp
g++ -std=c++11 -o my_program $CPP_FILES -I/opt/homebrew/Cellar/sdl2/2.26.5/include/SDL2/ -L/opt/homebrew/Cellar/sdl2/2.26.5/lib/ -lSDL2 -lpthread -lcoap-3 -Wno-psabi

# Connect Controller
bash connectController.sh

# Run your program
./my_program
