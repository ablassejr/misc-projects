#include "bTree.h"
#include <iostream>

using std::cout, std::cin, std::endl;

int main() {
  cout << "Enter list of positive integers ending with -999:" << endl;
  int input;
  bTree<int, 5> btree;
  while (cin >> input && input != -999) {
    btree.insert(input);
  }
  cout << "Enter a number to search: ";
  cin >> input;
  if (btree.search(input))
    cout << input << " is found in the tree." << endl;
  else
    cout << input << " is not found in the tree." << endl;
  return 0;
}
