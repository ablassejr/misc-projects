//****************************************************************
// COSC3333 Module 1 Assignment - Question 4
// Hash Table Implementation with Folding Method
//****************************************************************

#include "Student.h"
#include "hashT.h"
#include <iostream>
#include <string>
#include <vector>

using namespace std;

//****************************************************************
// Function: foldingHash
// Purpose: Calculate hash index using the folding method
// Parameters:
//   - id: Student ID to hash
//   - tableSize: Size of the hash table
// Returns: Hash index (sum of 2-digit parts % tableSize)
//
// Example: For ID 123456789 with 2-digit parts:
//   Parts: 12, 34, 56, 78, 9
//   Sum: 12 + 34 + 56 + 78 + 9 = 189
//   Hash: 189 % tableSize
//****************************************************************
int foldingHash(int id, int tableSize) {
  int sum = 0;

  // Convert ID to positive if negative (shouldn't happen for student IDs)
  if (id < 0)
    id = -id;

  // Extract 2-digit parts and sum them
  while (id > 0) {
    int part = id % 100; // Get last 2 digits
    sum += part;
    id = id / 100; // Remove last 2 digits
  }

  // Return hash index
  return sum % tableSize;
}

//****************************************************************
// Function: main
// Purpose: Demonstrate hash table operations with student records
//****************************************************************
int main() {
  const int HASH_TABLE_SIZE = 11;
  const int NUM_STUDENTS = 5;

  // Create hash table for students
  hashT<Student> studentTable(HASH_TABLE_SIZE);

  cout << "========================================" << endl;
  cout << "  Hash Table Student Management System" << endl;
  cout << "========================================" << endl;
  cout << "Hash Table Size: " << HASH_TABLE_SIZE << endl;
  cout << "Hash Method: Folding (2-digit parts)" << endl;
  cout << "Collision Resolution: Quadratic Probing" << endl;
  cout << "========================================" << endl << endl;

  // Step 1: Input students
  cout << "Please enter information for " << NUM_STUDENTS
       << " students:" << endl;
  cout << "----------------------------------------" << endl;

  for (int i = 1; i <= NUM_STUDENTS; i++) {
    int id;
    string name;

    cout << "\nStudent " << i << ":" << endl;
    cout << "  Enter Student ID: ";
    cin >> id;

    cout << "  Enter Student Name: ";
    cin.ignore(); // Clear newline from previous input
    getline(cin, name);

    // Create student object
    Student student(id, name);

    // Calculate hash index using folding method
    int hashIndex = foldingHash(id, HASH_TABLE_SIZE);

    cout << "  Hash Index (before collision resolution): " << hashIndex << endl;

    // Insert into hash table
    studentTable.insert(hashIndex, student);
    cout << "  Student added successfully!" << endl;
  }

  // Step 2: Display hash table contents
  cout << "\n========================================" << endl;
  cout << "  Current Hash Table Contents" << endl;
  cout << "========================================" << endl;
  studentTable.print();
  cout << "========================================" << endl;

  // Step 3: Delete a student
  cout << "\n----------------------------------------" << endl;
  cout << "  Delete Student Record" << endl;
  cout << "----------------------------------------" << endl;

  int deleteId;
  string deleteName;

  cout << "Enter Student ID to delete: ";
  cin >> deleteId;

  cout << "Enter Student Name to delete: ";
  cin.ignore();
  getline(cin, deleteName);

  // Create student object to delete
  Student studentToDelete(deleteId, deleteName);

  // Calculate hash index for the student to delete
  int deleteHashIndex = foldingHash(deleteId, HASH_TABLE_SIZE);

  cout << "Hash Index for deletion: " << deleteHashIndex << endl;

  // Remove from hash table
  studentTable.remove(deleteHashIndex, studentToDelete);
  cout << "Student deletion attempted." << endl;

  // Step 4: Display final hash table contents
  cout << "\n========================================" << endl;
  cout << "  Final Hash Table Contents" << endl;
  cout << "========================================" << endl;
  studentTable.print();
  cout << "========================================" << endl;

  cout << "\nProgram completed successfully!" << endl;

  return 0;
}
