#include <iostream>
#include <cmath>  // 包含数学函数
#include <limits> // 包含无穷大常量

int main() {
    // 使用INFINITY常量（正无穷大）
    double result1 = cos(std::numeric_limits<double>::infinity());
    // 使用负INFINITY常量（负无穷大）
    double result2 = cos(-std::numeric_limits<double>::infinity());

    std::cout << "cos(INFINITY) = " << result1 << std::endl;  // 输出: nan
    std::cout << "cos(-INFINITY) = " << result2 << std::endl; // 输出: nan

    return 0;
}
