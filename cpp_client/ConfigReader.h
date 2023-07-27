//
// Created by simon on 28.06.2023.
//

#ifndef INC_4X4_GEWINNT_CONFIGREADER_H
#define INC_4X4_GEWINNT_CONFIGREADER_H


#include <string>

class ConfigReader {
public:
    static std::string readConfigFile(const std::string& whatIneed);
};



#endif //INC_4X4_GEWINNT_CONFIGREADER_H
