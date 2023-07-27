//
// Created by 49152 on 10.05.2023.
//

#ifndef INC_4X4_GEWINNT_CONTROLLER_H
#define INC_4X4_GEWINNT_CONTROLLER_H


#include <SDL.h>
#include "ControllerMessage.h"
#include <queue>

class Controller {
public:
    Controller();
    ~Controller();
    ControllerMessage readMessage();
    void processEvents();
    void initializeSDL();
    uint8_t generatePayload(uint8_t button);
    uint8_t generateHealthCheckMessage();
    std::queue<ControllerMessage> getMessageQueue();
    static uint8_t generateInitMessage();

private:
    SDL_Joystick* joystick_;
    std::queue<ControllerMessage> messages_;
};


#endif //INC_4X4_GEWINNT_CONTROLLER_H
