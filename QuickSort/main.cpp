#include "arrayListType.h"
#include <iostream>
#include <string>
using std::cout, std::cin, std::string;

int main() {
  cout << "Enter list of positive integers ending in -999:";
  int num;
  arrayListType<int> list;
  cin >> num;
  while (num != -999) {
    list.insert(num);
    cin >> num;
  }
  list.quickSort();
  cout << "Sorted list: ";
  list.print();
  return 0;
}
