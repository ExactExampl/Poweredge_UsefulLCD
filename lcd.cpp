#include <iostream>
#include <vector>
#include <sstream>
#include <string>

using namespace std;

int main(int argc, char *argv[]) {
    std::string textToWrite = ""; 
    for (int i=1;i<argc;i++) textToWrite.append(std::string(argv[i]).append(" "));

    if (textToWrite.size() == 0) {
        std::cout << "Wrong text size!!!" << std::endl;
        exit(0);
    }
       
    textToWrite.resize(textToWrite.size() - 1);
    std::vector<char> charToWrite(textToWrite.c_str(), textToWrite.c_str() + textToWrite.size() + 1);
    std::string charRawValues("ipmitool raw 0x6 0x58 193 0x0 0x0 0x" + std::to_string(charToWrite.size()));
    
    if (charToWrite.size() > 14) {
        std::cout << "Wrong text size!!!" << std::endl;
        exit(0);
    }

    for (int i = 0; i < charToWrite.size(); i++) {
        std::stringstream ss;
        ss << std::hex << int(charToWrite[i]);
        charRawValues += " 0x" + ss.str();
    }
    const char* command = charRawValues.c_str();
                
    system(command);
    system("ipmitool raw 0x6 0x58 0xc2 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0 0x0");
    
}
