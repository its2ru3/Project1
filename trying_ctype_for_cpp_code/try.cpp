#include <iostream>
extern "C" {
    void hello() {
        std::cout << "Hello from C++!" << std::endl;
    }

    int add(int a, int b) {
        return a + b;
    }
}
