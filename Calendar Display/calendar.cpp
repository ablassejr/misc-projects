#include "utils.h"

int main() {

  int *input = getInput();
  int month = input[0];
  int year = input[1];
  int startDay = getStartDay(month, year);
  renderCalendar(month, startDay, year);

  return 0;
}
