#include <fstream>
#include <iostream>



int main() {
    std::string reversed;
    std::string text;
    std::ifstream* inputFile;
    std::ofstream* outFile;
    std::string inputFileName;;
    
    std::cout << "Enter the input file name: ";
    getline(std::cin, inputFileName);
    if (inputFileName.empty()) {
        std::cout << "Error: no input file name provided." << std::endl;
        return 1;
    }
    inputFile = new std::ifstream(inputFileName);
    outFile = new std::ofstream("reversed.txt");
    if (inputFile->fail()) {
        std::cout << "Input File Error" << std::endl;
        return 2;
    }
    
    if (outFile->fail()) {
        std::cout << "Output File Error " << std::endl;
        return 3;
    }
    else if (*inputFile && *outFile) {
       while (std::getline(*inputFile, text)) {
        int length = text.length();
        int index = length - 1;
        while (index >= 0) {
            reversed += text[index];
            index--;
        } 
        *outFile << reversed << std::endl;
        reversed = "";
        }
        return 0;
    }
    std::cout << "Unknown Error" << std::endl;
    return 10;
}
