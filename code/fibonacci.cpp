#include <iostream>

constexpr int Fibonacci(int n) {
    return n == 1 ? 1 : n == 2 ? 1 : Fibonacci(n - 1) + Fibonacci(n - 2);
}

int main() {
    int fibs[] = {
        Fibonacci(4),
        Fibonacci(8),
        Fibonacci(20)
    };
    for(int i : fibs) {
        std::cout << i << "\n";
    }
    return 0;
}