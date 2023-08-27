#ifndef INC_4X4_GEWINNT_CONTROLLERMESSAGE_H
#define INC_4X4_GEWINNT_CONTROLLERMESSAGE_H

#include <string>
#include <chrono>



/**
 * @class ControllerMessage
 * @brief Represents a message with unique ID and timestamp generated in response to controller events.
 *
 * The ControllerMessage class encapsulates individual messages that may be produced
 * by a controller. Each message carries a payload, is assigned a unique ID, and is 
 * timestamped when created.
 */
class ControllerMessage {
public:

    /**
     * @brief Constructor that initializes the message with a given payload.
     *
     * If the payload is non-zero, assigns a unique ID and stamps the current time.
     *
     * @param payload The content of the message.
     */
    explicit ControllerMessage(uint8_t payload);


    /**
     * @brief Retrieve the payload of the message.
     *
     * @return uint8_t The message payload.
     */
    uint8_t payload() const;

        /**
     * @brief Retrieve the unique ID of the message.
     *
     * @return uint32_t The unique message ID.
     */
    uint32_t id() const;

    /**
     * @brief Retrieve the timestamp of when the message was created or last updated.
     *
     * @return std::chrono::high_resolution_clock::time_point The timestamp of the message.
     */
    std::chrono::high_resolution_clock::time_point timestamp() const;


    /**
     * @brief Update the timestamp of the message to the current time.
     */
    void updateTimestamp();

private:

    uint8_t payload_;   ///< Content of the message
    uint32_t id_;       ///< Unique ID of the message
    std::chrono::high_resolution_clock::time_point timestamp_;  ///< Timestamp of when the message was created or last updated
    static uint32_t s_next_id;  ///< static member for generating unique IDs
};

#endif //INC_4X4_GEWINNT_CONTROLLERMESSAGE_H
