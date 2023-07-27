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
    initializeSDL();
}

Controller::~Controller() {
    SDL_JoystickClose(joystick_);
    SDL_Quit();
}

void Controller::initializeSDL(){
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
                // Attempt to reconnect for up to 1 minute
                auto start = std::chrono::steady_clock::now();
                do {
                    // Reinitialize SDL
                    SDL_QuitSubSystem(SDL_INIT_JOYSTICK);
                    auto reconnect = std::chrono::steady_clock::now();
                    std::chrono::duration<double> elapsed_seconds = reconnect-start;
                    
                    if(elapsed_seconds.count() > 10.0) {
                        // Reconnect to Pi
                        //push a health check message 
                        uint8_t message = generateHealthCheckMessage();
                        messages_.push(ControllerMessage(message));
                        std::this_thread::sleep_for(std::chrono::seconds(2));
                        system("bash connectController.sh");
                        initializeSDL();
                        start = std::chrono::steady_clock::now();
                    }
                    
                    // Check the elapsed time
                    // auto end = std::chrono::steady_clock::now();
                    // std::chrono::duration<double> elapsed_seconds = end-start;
                    // if (elapsed_seconds.count() > 60.0) {
                    //     std::cerr << "Timeout: Failed to reconnect joystick after 1 minute" << std::endl;
                    //     break;
                    // }
                } while (!joystick_);
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

