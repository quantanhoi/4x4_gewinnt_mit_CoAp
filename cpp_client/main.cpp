//
// Created by 49152 on 10.05.2023.
//

#include "Controller.h"
#include "MessageQueue.h"
#include "Process.h"
#include "CoAPSender.h"
#include "ConfigReader.h"
#include<iostream>
#include <thread>
#include<SDL.h>

int main() {
    std::cout << "Program is running . . ." << std::endl;
    if (SDL_Init(SDL_INIT_JOYSTICK) < 0) {
        std::cerr << "Failed to initialize SDL: " << SDL_GetError() << std::endl;
        return 1;
    }

    std::string serverIP = ConfigReader::readConfigFile("Server-IP");
    std::cout << "Server IP: " << serverIP << "\n";

    std::string controllerMac = ConfigReader::readConfigFile("Controller-MAC");
    std::cout << "Controller MAC: " << controllerMac << "\n";


    Controller controller;
    MessageQueue queue;
    Process process(controller, queue);
    CoAPSender coapSender(queue);

    std::thread processThread(std::ref(process));
    std::thread coapSenderThread(std::ref(coapSender));

    processThread.join();
    coapSenderThread.join();

    SDL_Quit();
    return 0;
}
