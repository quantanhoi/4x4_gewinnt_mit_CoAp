#include "ControllerMessage.h"

// Initialize static member outside of the class
uint32_t ControllerMessage::s_next_id = 0;

ControllerMessage::ControllerMessage(uint8_t payload)
        : payload_(payload) {
    if(payload != 0){
        id_ = ++s_next_id;
        timestamp_ = std::chrono::high_resolution_clock::now();
    }
}

void ControllerMessage::updateTimestamp() {
    timestamp_ = std::chrono::high_resolution_clock::now();
}

uint8_t ControllerMessage::payload() const {
    return payload_;
}

uint32_t ControllerMessage::id() const {
    return id_;
}

std::chrono::high_resolution_clock::time_point ControllerMessage::timestamp() const {
    return timestamp_;
}
