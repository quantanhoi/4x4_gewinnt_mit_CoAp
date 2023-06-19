//
// Created by 49152 on 10.05.2023.
//
#include "Controller.h"
#include <iostream>
#include <sstream>
#include <unistd.h>
#include <cstdio>  // Required for std::remove
#include <thread>
#include <chrono>

Controller::Controller() {
    if (SDL_Init(SDL_INIT_JOYSTICK) < 0) {
        std::cerr << "Failed to initialize SDL: " << SDL_GetError() << std::endl;
        exit(1);
    }

    joystick_ = SDL_JoystickOpen(0);
    if (!joystick_) {
        std::cerr << "Failed to open joystick: " << SDL_GetError() << std::endl;
        SDL_Quit();
        exit(1);
    }
    uint8_t initMessage = generateInitMessage();
    messages_.push(ControllerMessage(initMessage));
    std::cout << "init message pushed" << std::endl;
}

Controller::~Controller() {
    SDL_JoystickClose(joystick_);
    SDL_Quit();
}

ControllerMessage Controller::readMessage() {
    if (!messages_.empty()) {
        ControllerMessage msg = messages_.front();
        messages_.pop();
        return msg;
    }
    return ControllerMessage(0);
}


void Controller::processEvents() {
    SDL_Event e;
    while (SDL_PollEvent(&e)) {
        if (e.type == SDL_JOYBUTTONDOWN) {
            uint8_t buttonPressed = static_cast<uint8_t>(e.jbutton.button);
            std::cout<<"Button pressed: "<< static_cast<int>(buttonPressed) <<std::endl;

            if(buttonPressed == 0 || buttonPressed == 1 || buttonPressed == 3) {
                uint8_t buttonMessage = generatePayload(static_cast<uint8_t>(e.jbutton.button));
                messages_.push(ControllerMessage(buttonMessage));
            }
            else if(buttonPressed == 4) {  //button 4 = L1 on Controller
                //Logging
                std::remove("log.txt"); //remove existing Log file
                std::cout<<"simulate 10000 Buttonpresses"<< std::endl;
                for(int x = 0; x<100; x++){
                    messages_.push(ControllerMessage(generatePayload(static_cast<uint8_t>(4))));
                    std::cout<<"pushed Message"<< std::endl;
                    //std::this_thread::sleep_for(std::chrono::milliseconds(50));
                }
                std::cout<<"Logging successful"<< std::endl;
            }
            else if(buttonPressed == 2) {
                std::cout<<"Exiting Program."<< std::endl;
                exit(0);
            }
        }
        else if (e.type == SDL_JOYDEVICEREMOVED) {
            // A joystick has been disconnected
            if (joystick_ && e.jdevice.which == SDL_JoystickInstanceID(joystick_)) {
                // The disconnected joystick is the one we're using
                SDL_JoystickClose(joystick_);
                joystick_ = nullptr;
                std::cout << "Joystick disconnected" << std::endl;
                //reconnect to Pi when connection lost
                system("bash connectController.sh");
            }
        } else if (e.type == SDL_JOYDEVICEADDED) {
            // A joystick has been connected
            if (!joystick_) {
                joystick_ = SDL_JoystickOpen(e.jdevice.which);
                if (joystick_) {
                    std::cout << "Joystick connected" << std::endl;
                } else {
                    std::cerr << "Failed to open joystick: " << SDL_GetError() << std::endl;
                }
            }
        }
    }
}

uint8_t Controller::generatePayload(uint8_t button) {
    if (button > 4) {
        std::cerr << "invalid button, button number should be less than 127\n";
        return 0;
    }
    bool controllerIsConnected = SDL_JoystickGetAttached(joystick_);
    uint8_t payload = 0;
    payload |= (controllerIsConnected ? 1 : 0) << 3;
    payload |= button;
    return payload;
}
uint8_t Controller::generateHealthCheckMessage() {
    //TODO: health check funktioniert noch nicht
    bool controllerIsConnected = SDL_JoystickGetAttached(joystick_);
    std::cout << "HealthCheck: Controller is " << (controllerIsConnected ? "connected" : "not connected") << std::endl;
    uint8_t payload = 0;
    payload |= (controllerIsConnected ? 1 : 0) << 3;
    payload |= 1 << 2;

    return payload;
}

uint8_t Controller::generateInitMessage() {
    uint8_t payload = 0;
    payload |= 1 << 4;
    return payload;
}

std::queue<ControllerMessage> Controller::getMessageQueue() {
    return messages_;
}

