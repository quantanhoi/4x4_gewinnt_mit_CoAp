#include "ControllerMessage.h"

// Initialize static member outside of the class
uint32_t ControllerMessage::s_next_id = 0;


/**
 * @brief Constructor for the ControllerMessage class.
 * 
 * Initializes a new message with the given payload. If the payload is not zero,
 * the message is timestamped and assigned a unique identifier.
 * 
 * @param payload The payload for the message.
 */
ControllerMessage::ControllerMessage(uint8_t payload)
        : payload_(payload) {
    if(payload != 0){
        id_ = ++s_next_id;
        timestamp_ = std::chrono::high_resolution_clock::now();
    }
}

/**
 * @brief Updates the timestamp of the message to the current time.
 */
void ControllerMessage::updateTimestamp() {
    timestamp_ = std::chrono::high_resolution_clock::now();
}


/**
 * @brief Gets the payload of the message.
 * 
 * @return The payload as a byte.
 */
uint8_t ControllerMessage::payload() const {
    return payload_;
}


/**
 * @brief Gets the unique identifier of the message.
 * 
 * @return The unique identifier as a 32-bit unsigned integer.
 */
uint32_t ControllerMessage::id() const {
    return id_;
}


/**
 * @brief Gets the timestamp of the message.
 * 
 * @return The timestamp as a high-resolution time_point object.
 */
std::chrono::high_resolution_clock::time_point ControllerMessage::timestamp() const {
    return timestamp_;
}
