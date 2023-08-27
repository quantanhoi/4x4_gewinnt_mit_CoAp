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

/**
 * @brief Initialize SDL and sets up joystick device for communication.
 */
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


/**
 * @brief Reads a message from the message queue.
 * 
 * If the queue is not empty, it pops the front message, otherwise
 * it returns an empty ControllerMessage.
 * 
 * @return The front ControllerMessage or an empty ControllerMessage.
 */
ControllerMessage Controller::readMessage() {
    if (!messages_.empty()) {
        ControllerMessage msg = messages_.front();
        messages_.pop();
        return msg;
    }
    return ControllerMessage(0);
}



/**
 * @brief Process events from the joystick device.
 * 
 * Handles joystick button presses (at e.type == SDL_JOYBUTTONDOWN), 
 * disconnections (at e.type == SDL_JOYDEVICEREMOVED), 
 * reconnections (at e.type == SDL_JOYDEVICEADDED), etc.
 * Generates messages based on joystick events and pushes them to the message queue.
 */
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
                std::cout<<"simulate 100 Buttonpresses"<< std::endl;
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
            std::cout<<"Controller is disconnected"<< std::endl;
            exit(0);
        } /*else if (e.type == SDL_JOYDEVICEADDED) {
            // A joystick has been connected
            if (!joystick_) {
                joystick_ = SDL_JoystickOpen(e.jdevice.which);
                if (joystick_) {
                    std::cout << "Joystick connected" << std::endl;
                } else {
                    std::cerr << "Failed to open joystick: " << SDL_GetError() << std::endl;
                }
            }
        }*/
    }
}


/**
 * @brief Generate payload based on the button pressed on the joystick.
 * 
 * The generated payload includes information about the joystick connection 
 * and the button that was pressed.
 * 
 * @param button The button number pressed on the joystick.
 * @return The generated payload as a byte.
 */
uint8_t Controller::generatePayload(uint8_t button) {
    if (button > 4) {
        std::cerr << "invalid button, button number should be less than 127\n";
        return 0;
    }
    //payload should not be empty as in CoApSender it is required payload != 0 to send the message
    if(button == 0) {
        button = 2;
    }
    bool controllerIsConnected = SDL_JoystickGetAttached(joystick_);
    uint8_t payload = 0;
    payload |= button;
    return payload;
}

/**
 * @brief Generate a health check message.
 * 
 * Generates the health check payload that is consistently sent to the server.
 * Payload: 0-1-0-0
 * 
 * @return The health check payload as a byte.
 */
uint8_t Controller::generateHealthCheckMessage() {
    bool controllerIsConnected = SDL_JoystickGetAttached(joystick_);
    std::cout << "HealthCheck: Controller is " << (controllerIsConnected ? "connected" : "not connected") << std::endl;
    uint8_t payload = 0;
    payload |= 1 << 2;

    return payload;
}

/**
 * @brief Generate an initialization message.
 * 
 * This function generates a specific initialization payload byte.
 * Payload: 1-0-0-0
 *
 * @return The initialization payload as a byte.
 */
uint8_t Controller::generateInitMessage() {
    uint8_t payload = 0;
    payload |= 1 << 3;
    return payload;
}


/**
 * @brief Retrieve the message queue.
 * 
 * Provides access to the message queue containing ControllerMessage objects.
 * 
 * @return The message queue.
 */
std::queue<ControllerMessage> Controller::getMessageQueue() {
    return messages_;
}

