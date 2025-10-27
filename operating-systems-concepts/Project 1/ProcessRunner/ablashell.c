#include "utilities.h"

#define true 1
#define false 0
int main() {

  // variable declarations
  char *args[100 / 2 + 1];
  int isConcurrent;
  // and definitions
  int shouldRun = true;
  char *shellDis = "lash⚟";
  int i = 0;
  // execution
  while (shouldRun) {
    for (int j = 0; j < 100 / 2 + 1; j++) {
      args[j] = NULL;
    }

    printf("execution %d: %s ", i, shellDis);
    isConcurrent = input(args);
    // printf("check exit on: %s\n", args[0]);

    if (!exitCheck(args[0])) {
      printf("\t No Exit, Command Received: %s", args[0]);
      executeCommand(args, isConcurrent);
    } else {
      printf("\tExit command received.\n");
      shouldRun = false;
    }
    i++;
  }

  printf("Exiting shell...\n");
  exit(0);
  return 0;
}
