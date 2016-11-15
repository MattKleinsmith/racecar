#include <iostream>
#include <cstdlib>
#include <fstream>

#include "split.h"


int main () {
    system("./setupRFCOMMport.sh");
    const char* bluetooth = std::getenv("bluetooth");
    std::string str;
    std::fstream f;
    f.open("/dev/rfcomm0");
    const char delim = ',';
    typdef std::vector<std::string> StringVector;
    while (true)
    {
        f >> str;
        StringVector elems = split(str, delim);
		for (StringVector::const_iterator i = elems.begin(); i != elems.end(); ++i)
		    std::cout << *i << ' ';
        std::cout << std::endl;
    }
}
