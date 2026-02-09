#include "hashT.h"
#include <iostream>
#include <string>
using std::cout, std::cin, std::string, std::to_string;

int main() {
  string name;
  int studentID, size;
  cout << "Enter the number of students: ";
  cin >> size;
  size *= 2;
  hashT<string> studentTable(size);
  for (int i = 1; i <= size; i++) {
    cout << "Enter the ID and name of student " << i << " (ID *space* name): ";
    cin >> studentID >> name;
    int squared = studentID * studentID;
    string sqStr = to_string(squared);
    int hashIndex = (sqStr[sqStr.length() / 2]) % (size);
    studentTable.insert(hashIndex, name);
  }
  cout << "\nThe hash table is:\n";
  studentTable.print();
  return 0;
}
