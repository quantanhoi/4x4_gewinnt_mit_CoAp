//
// Created by 49152 on 10.05.2023.
//

#ifndef INC_4X4_GEWINNT_PROCESS_H
#define INC_4X4_GEWINNT_PROCESS_H


#include "Controller.h"
#include "MessageQueue.h"

class Process {
public:
    Process(Controller& controller, MessageQueue& queue);
    void operator()();

private:
    Controller& controller_;
    MessageQueue& queue_;
};


#endif //INC_4X4_GEWINNT_PROCESS_H
