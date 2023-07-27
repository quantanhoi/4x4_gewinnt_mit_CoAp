#!/bin/bash

# Stop script on any error
#set -e
set -x #to debug

# Clone the repository and enter its directory
if [ ! -d "libcoap" ]; then
    git clone https://github.com/obgm/libcoap
    cd libcoap/
    # Check if libtool, autoconf, automake and pkg-config are installed
    dpkg -l libtool autoconf automake pkg-config > /dev/null 2>&1 || {
      # If they're not installed, install them
      sudo apt-get install libtool autoconf automake pkg-config
    }

    # Build libcoap
    ./autogen.sh
    ./configure --disable-doxygen --disable-manpages --disable-dtls
    make
    sudo make install
    cd ..
fi

# Check if SDL2 dev library is installed
dpkg -l libsdl2-dev > /dev/null 2>&1 || {
    # If it's not installed, install it
    sudo apt-get install libsdl2-dev
}

# Export library path
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# Compile your program
CPP_FILES="main.cpp Controller.cpp MessageQueue.cpp Process.cpp CoAPSender.cpp common.o ControllerMessage.cpp logging.cpp ConfigReader.cpp"
g++ -c common.cc
g++ -o my_program $CPP_FILES -I/usr/include/SDL2 -lSDL2 -lpthread -lcoap-3 -Wno-psabi


# Connect Controller
bash connectController.sh

# Run your program
./my_program
