#ifndef LOGGING_H
#define LOGGING_H

#include "ControllerMessage.h"
#include <string>
#include <mutex>

extern std::mutex log_mutex;  // global mutex for log file access

/**
 * @brief Logs the given ControllerMessage with its associated station.
 *
 * This function logs details of the provided message including its ID, associated 
 * station and the elapsed time since the message's timestamp. It writes these 
 * details to a file named "log.txt".
 *
 * @param message The message to be logged.
 * @param station The station associated with the message.
 */
void logMessage(ControllerMessage& message, const std::string& station);

#endif // LOGGING_H
