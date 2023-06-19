//
// Created by 49152 on 10.05.2023.
//

#include "MessageQueue.h"

void MessageQueue::push(const ControllerMessage& message) {
    std::lock_guard<std::mutex> lock(mtx_);
    queue_.push(message);
    cv_.notify_one();
}

ControllerMessage MessageQueue::pop() {
    std::unique_lock<std::mutex> lock(mtx_);
    cv_.wait(lock, [this]{ return !queue_.empty(); });
    ControllerMessage msg = queue_.front();
    queue_.pop();
    return msg;
}
