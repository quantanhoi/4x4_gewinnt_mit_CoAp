//
// Created by 49152 on 10.05.2023.
//

#ifndef INC_4X4_GEWINNT_PROCESS_H
#define INC_4X4_GEWINNT_PROCESS_H


#include "Controller.h"
#include "MessageQueue.h"


/**
 * @class Process
 * @brief Continuous polling and queueing of messages from Controller.
 *
 * The Process class provides the mechanism to continuously poll the Controller 
 * for messages and then push them into the MessageQueue. The class is designed 
 * to run as part of a threaded or concurrent environment to keep the queue updated 
 * with the latest messages.
 */
class Process {
public:

    /**
     * @brief Constructs a Process object with references to Controller and MessageQueue.
     * 
     * @param controller Reference to the Controller object to poll for messages.
     * @param queue Reference to the MessageQueue object to push messages into.
     */
    Process(Controller& controller, MessageQueue& queue);


    /**
     * @brief Operator to run the continuous polling and queueing loop.
     * 
     * This operator, when invoked, starts the continuous loop where messages are 
     * polled from the Controller and subsequently pushed into the MessageQueue.
     */
    void operator()();

private:
    Controller& controller_;    ///< Reference to the Controller instance.
    MessageQueue& queue_;       ///< Reference to the MessageQueue instance.
};


#endif //INC_4X4_GEWINNT_PROCESS_H
