#include "utils.h"
#include <iomanip>
#include <iostream>
#include <stdexcept>
using std::cin;
using std::cout;
using std::endl;
// getInput()
int *getInput() {
  int month, year;
  cout << "Enter month (1-12): ";
  cin >> month;
  cout << "Enter year(>=1800): ";
  cin >> year;
  try {
    if (month < 1 || month > 12 || year < 1800) {
      throw std::out_of_range("Month must be between 1 and 12, and year must "
                              "be positive and after 1800.");
    }
    return new int[2]{month, year};
  } catch (std::out_of_range &e) {
    cout << e.what();

    exit(1);
  }
}
// getNumOfDaysInMonth()
int getNumOfDaysInMonth(int month, int year) {
  if (month == 2) {
    return isLeapYear(year) ? 29 : 28;
  }
  // Months with 31 days: Jan, Mar, May, Jul, Aug, Oct, Dec
  if (month == 1 || month == 3 || month == 5 || month == 7 || month == 8 ||
      month == 10 || month == 12) {
    return 31;
  }
  // Months with 30 days: Apr, Jun, Sep, Nov
  return 30;
}

// getStartDay()
int getStartDay(int month, int year) {
  // Jan 1, 1800 was a Wednesday (day 3)
  int startDay = 3;
  int startYear = 1800;

  // Calculate day of week for Jan 1 of the target year
  for (int y = startYear; y < year; y++) {
    int daysInYear = isLeapYear(y) ? 366 : 365;
    startDay = (startDay + daysInYear) % 7;
  }

  // Add days from Jan 1 through the end of the previous month
  for (int m = 1; m < month; m++) {
    startDay = (startDay + getNumOfDaysInMonth(m, year)) % 7;
  }

  return startDay;
}

// isLeapYear()
bool isLeapYear(int year) {
  if ((year % 400 == 0) || ((year % 4 == 0) && (year % 100 != 0)))
    return true;
  else
    return false;
}

void renderCalendar(int month, int startDay, int year) {
  int fmtLength = 5;
  std::string dayNames[7] = {"Sun",   "Mon", "Tues", "Weds",
                             "Thurs", "Fri", "Sat"};

  int daysInMonth = getNumOfDaysInMonth(month, year);
  cout << "Days in month: " << daysInMonth << endl;
  cout << "Start day: " << dayNames[startDay] << endl;
  int currentDate = 1;
  int currentDay = 0;
  for (int j = 0; j < 7; j++) {
    cout << std::setw(fmtLength) << dayNames[j] << " | ";
  }
  cout << endl;
  for (int i = 1; i < 7; i++) {
    for (int j = 0; j < 7; j++) {
      if (currentDate > daysInMonth) {
        cout << std::setw(fmtLength) << " " << " | ";
        continue;
      } else if (currentDate < startDay && currentDay < startDay) {
        cout << std::setw(fmtLength) << " " << " | ";
        currentDay++;
        continue;
      } else {
        cout << std::setw(fmtLength) << currentDate << " | ";
        currentDate++;
        currentDay++;
      }
    }
    cout << endl;
  }
}
