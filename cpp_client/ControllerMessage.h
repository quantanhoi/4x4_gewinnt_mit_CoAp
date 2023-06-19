#ifndef INC_4X4_GEWINNT_CONTROLLERMESSAGE_H
#define INC_4X4_GEWINNT_CONTROLLERMESSAGE_H

#include <string>
#include <chrono>

class ControllerMessage {
public:
    explicit ControllerMessage(uint8_t payload);

    uint8_t payload() const;
    uint32_t id() const;
    std::chrono::high_resolution_clock::time_point timestamp() const;
    void updateTimestamp();

private:
    uint8_t payload_;
    uint32_t id_;
    std::chrono::high_resolution_clock::time_point timestamp_;
    static uint32_t s_next_id;  // static member for generating unique IDs
};

#endif //INC_4X4_GEWINNT_CONTROLLERMESSAGE_H
