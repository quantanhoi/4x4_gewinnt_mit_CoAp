//
// Created by simon on 28.06.2023.
//

#ifndef INC_4X4_GEWINNT_CONFIGREADER_H
#define INC_4X4_GEWINNT_CONFIGREADER_H


#include <string>


/**
 * @class ConfigReader
 * @brief Utility to read configurations from a file.
 *
 * The ConfigReader class provides a static method to fetch specific
 * configurations from a predefined configuration file.
 */
class ConfigReader {
public:

    /**
     * @brief Fetches a specific configuration value.
     *
     * Reads the configuration file and retrieves the value associated
     * with the provided key.
     *
     * @param whatIneed The key whose associated value needs to be fetched.
     * @return std::string The value associated with the key.
     */
    static std::string readConfigFile(const std::string& whatIneed);
};



#endif //INC_4X4_GEWINNT_CONFIGREADER_H
