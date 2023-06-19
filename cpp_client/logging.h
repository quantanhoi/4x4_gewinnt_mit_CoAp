#ifndef LOGGING_H
#define LOGGING_H

#include "ControllerMessage.h"
#include <string>
#include <mutex>

extern std::mutex log_mutex;  // global mutex for log file access

void logMessage(ControllerMessage& message, const std::string& station);

#endif // LOGGING_H
