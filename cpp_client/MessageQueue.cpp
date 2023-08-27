//
// Created by 49152 on 10.05.2023.
//

#include "MessageQueue.h"


/**
 * @brief Pushes a ControllerMessage onto the queue in a thread-safe manner.
 * 
 * It locks the mutex, pushes the message, notifies a waiting pop operation (if any), 
 * and then unlocks the mutex automatically at the end of scope.
 * 
 * @param message The ControllerMessage to be pushed onto the queue.
 */
void MessageQueue::push(const ControllerMessage& message) {
    std::lock_guard<std::mutex> lock(mtx_);
    queue_.push(message);
    cv_.notify_one();
}



/**
 * @brief Pops a ControllerMessage from the queue in a thread-safe manner.
 * 
 * If the queue is empty, it waits using a condition variable until a message is available.
 * It then locks the mutex, pops the message from the front of the queue, 
 * and then unlocks the mutex automatically at the end of scope.
 * 
 * @return ControllerMessage The message popped from the front of the queue.
 */
ControllerMessage MessageQueue::pop() {
    std::unique_lock<std::mutex> lock(mtx_);
    cv_.wait(lock, [this]{ return !queue_.empty(); });
    ControllerMessage msg = queue_.front();
    queue_.pop();
    return msg;
}
