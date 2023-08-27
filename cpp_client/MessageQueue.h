//
// Created by 49152 on 10.05.2023.
//

#ifndef INC_4X4_GEWINNT_MESSAGEQUEUE_H
#define INC_4X4_GEWINNT_MESSAGEQUEUE_H


#include <queue>
#include "ControllerMessage.h"
#include <mutex>
#include <condition_variable>


/**
 * @class MessageQueue
 * @brief A thread-safe queue for ControllerMessage objects.
 *
 * This class provides a thread-safe mechanism to push and pop ControllerMessage
 * objects. It uses a mutex to synchronize access and a condition variable to 
 * handle the synchronization of data flow in the queue.
 */
class MessageQueue {
public:
    /**
     * @brief Pushes a new ControllerMessage to the back of the queue.
     * 
     * This method safely adds a message to the back of the queue and notifies
     * one waiting thread (if any) about the availability of a new message.
     * 
     * @param message The ControllerMessage object to be pushed.
     */
    void push(const ControllerMessage& message);

        /**
     * @brief Pops and returns the ControllerMessage from the front of the queue.
     * 
     * This method waits if the queue is empty and pops the message from the front
     * once a message becomes available.
     * 
     * @return ControllerMessage object from the front of the queue.
     */
    ControllerMessage pop();

private:
    std::queue<ControllerMessage> queue_;   ///< The underlying queue storing the ControllerMessages.
    std::mutex mtx_;                        ///< Mutex to synchronize access to the queue.
    std::condition_variable cv_;            ///< Condition variable to synchronize data flow.
};



#endif //INC_4X4_GEWINNT_MESSAGEQUEUE_H
