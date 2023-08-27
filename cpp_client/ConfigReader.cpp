#include "ConfigReader.h"
#include <fstream>
#include <iostream>


/**
 * @brief Implementation of the readConfigFile function.
 * 
 * Opens the config file and searches for the provided key. If found,
 * returns the associated value. If the file cannot be opened or the
 * key isn't found, it prints an error message and returns an empty string.
 * 
 * @param whatIneed The key to search for in the config file.
 * @return The value associated with the key or an empty string if not found.
 */
std::string ConfigReader::readConfigFile(const std::string& whatIneed) {
    std::ifstream configFile("../config.txt");  // replace with your file path
    if (!configFile) {
        std::cout << "Unable to open file\n";
        return "";  // return an empty string
    }

    std::string line;
    while (std::getline(configFile, line)) {
        // Skip comment lines
        if (line[0] == '#') continue;

        std::string::size_type pos = line.find('=');
        if (pos != std::string::npos) {
            std::string key = line.substr(0, pos);
            std::string value = line.substr(pos + 1);
            if (key == whatIneed) {
                configFile.close();
                return value;
            }
        }
    }

    configFile.close();

    std::cout << "Unable to find value for " << whatIneed << "\n";
    return "";  // return an empty string
}

