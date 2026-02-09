#include <iostream>
#include <stack>

int main(int argc, char *argv[]) {
  std::stack<int> binDig;
  int num;
  if (argc <= 1) {
    std::cout << "Input number to be converted to binary: ";
    std::cin >> num;
  } else {
    num = atoi(argv[1]);
  }
  std::cout << "Your number: " << num;
  while (num >= 1) {
    if (num == 1) {
      binDig.push(1);
      break;
    }

    if (num % 2) {
      binDig.push(1);
      num -= 1;
    } else {
      binDig.push(0);
    }

    num /= 2;
  }
  std::cout << "\nYour number in binary is: ";
  while (!binDig.empty()) {
    std::cout << binDig.top();
    binDig.pop();
  }
  return 0;
}
