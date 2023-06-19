//
// Created by 49152 on 10.05.2023.
//

#include "Process.h"
#include "chrono"
#include <iostream>
#include "logging.h"


Process::Process(Controller& controller, MessageQueue& queue)
        : controller_(controller), queue_(queue) 
        {
        }

void Process::operator()() {
    auto lastPushTime = std::chrono::high_resolution_clock::now();
    while (true) {
        controller_.processEvents();
        ControllerMessage msg = controller_.readMessage();
        auto now = std::chrono::high_resolution_clock::now();
        //TODO: should probably be in milliseconds instead
        auto elapsedSeconds = std::chrono::duration_cast<std::chrono::seconds>(now - lastPushTime).count();
        // std::cout << "Elapsed time: " << elapsedSeconds << " seconds" << std::endl;
        if (msg.payload() != 0) {
            logMessage(msg,"PushInQ");
            queue_.push(msg);
            lastPushTime = now;
        }
        else if (elapsedSeconds >= 5) {
            // Push your chosen message here
            uint8_t message = controller_.generateHealthCheckMessage();
            queue_.push(ControllerMessage(message));
            lastPushTime = now;
        }
    }
}
