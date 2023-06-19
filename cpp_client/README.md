### Controller as CoAP-Client
First you have to install libcoap: check out https://github.com/obgm/libcoap
install sdl2-dev
```
sudo apt-get install libsdl2-dev
```
before compiling common.cc
```
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
```
complile common.cc:
```
g++ -c common.cc
```
To compile, you need all dependencies libraries
For Ubuntu:
```
g++ -o my_program main.cpp Controller.cpp MessageQueue.cpp Process.cpp CoAPSender.cpp common.o  -I/usr/include/SDL2 -lSDL2 -lpthread -lcoap-3
```

for MacOS: 
```
g++ -std=c++14 -o my_program main.cpp Controller.cpp MessageQueue.cpp Process.cpp CoAPSender.cpp common.o -I/opt/homebrew/Cellar/sdl2/2.26.5/include/SDL2/ -L/opt/homebrew/Cellar/sdl2/2.26.5/lib/ -lSDL2 -lpthread -lcoap-3

```


Run the test program:
```
./my-program
```
