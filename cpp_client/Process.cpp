//
// Created by 49152 on 10.05.2023.
//

#include "Process.h"
#include "chrono"
#include <iostream>
#include "logging.h"

/**
 * @brief Constructs the Process object.
 * 
 * Initializes the process with a controller and a message queue.
 *
 * @param controller Reference to the Controller object.
 * @param queue Reference to the MessageQueue object.
 */
Process::Process(Controller& controller, MessageQueue& queue)
        : controller_(controller), queue_(queue) 
        {
        }


/**
 * @brief Operator function to process controller events.
 *
 * Constantly checks for controller events. On a button press, the relevant message 
 * is logged and pushed onto the queue. If no button press event is received 
 * within a given timeframe, a health check message is generated and pushed.
 */
void Process::operator()() {
    auto lastPushTime = std::chrono::high_resolution_clock::now();
    while (true) {
        controller_.processEvents();
        ControllerMessage msg = controller_.readMessage();
        auto now = std::chrono::high_resolution_clock::now();
        auto elapsedSeconds = std::chrono::duration_cast<std::chrono::seconds>(now - lastPushTime).count();
        // std::cout << "Elapsed time: " << elapsedSeconds << " seconds" << std::endl;
        if (msg.payload() != 0) {
            logMessage(msg,"PushInQ");
            queue_.push(msg);
            lastPushTime = now;
        }
        //if no button was pressed for more than 1 sec, send healthcheck to avoid timeout at server
        else if (elapsedSeconds >= 1) {
            // Push your chosen message here
            uint8_t message = controller_.generateHealthCheckMessage();
            queue_.push(ControllerMessage(message));
            lastPushTime = now;
        }
    }
}
