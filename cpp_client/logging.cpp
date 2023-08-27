#include "ControllerMessage.h"
#include "logging.h"

#include <fstream>
#include <iostream>

std::mutex log_mutex;  // global mutex for log file access


/**
 * @brief Logs the given ControllerMessage.
 * 
 * The function calculates the time elapsed since the message was last logged or created,
 * then logs the message's ID, the station, and the elapsed time to a file.
 * 
 * @param message The ControllerMessage to log.
 * @param station The station where the message is processed.
 */
void logMessage(ControllerMessage& message, const std::string& station) {
    // Get the current time
    auto now = std::chrono::high_resolution_clock::now();

    // Calculate the difference
    auto diff = now - message.timestamp();

    // Convert to milliseconds
    auto elapsed_ms = std::chrono::duration_cast<std::chrono::nanoseconds>(diff);

    // Log elapsed time to file
    std::lock_guard<std::mutex> lock(log_mutex);  // lock the mutex during this function
    std::ofstream log_file("log.txt", std::ios_base::app); // open in append mode

    if(log_file) {
        log_file << message.id() << "," << station << "," << elapsed_ms.count() << "ns" << std::endl;
    }
    else {
        // handle file error
        std::cerr << "Cannot open Log-File!\n";
    }
    // Update timestamp after logging
    message.updateTimestamp();
}
