#include "hashT.h"
#include <iostream>
#include <string>
using std::cout, std::cin, std::string;

int main()
{
    char input;
    string name;
    int hashID;
    bool willDelete = true;
    hashT<string> studentTable(7);
    cout << "Enter the names and IDs of 5 students: ";
    for (int i = 1; i <= 5; i++)
    {
        cout << "\n\tStudent " << i << "(ID *space* name): ";
        cin >> hashID >> name;
        studentTable.insert(hashID % 7, name);
    }
    cout << "\nThe hash table is:\n";
    studentTable.print();
    do
    {
        cout << "\n\n Enter the name and ID of a student to be deleted: ";
        cout << "\n\tStudent (ID *space* name): ";
        cin >> hashID >> name;
        studentTable.remove(hashID % 7, name);
        cout << "\nThe updated table is:\n";
        studentTable.print();
        cout << "Do you want to delete another student? (y/N): ";
        cin >> input;
        willDelete = input == 'y' || input == 'Y' ? true : false;
    } while (willDelete);
    return 0;
}
