#include "utilities.h"

#define true 1
#define false 0

int main() {

  // variable declarations
  static char historyBuffer[100 / 2 + 1];
  char *args[100 / 2 + 1], glts = '\0';
  int *inputChecks = malloc(2 * sizeof(int) + 1);
  int isConcurrent, isRedirect;

  int isChild = false;
  // and definitions
  int shouldRun = true;
  char *shellDis = "lash⚟";
  int i = 0;
  // execution
  system("clear");
  while (shouldRun) {
    sleep(1 / 2);
    // printf("Last Command: %s\n", historyBuffer);
    for (int j = 0; j < 100 / 2 + 1; j++) {
      args[j] = NULL;
    }

    printf("%s ", shellDis);
    *inputChecks = *input(args, historyBuffer, glts);
    isRedirect = inputChecks[1];
    isConcurrent = inputChecks[0];
    printf("Redirect: %d, Concurrent: %d\n", isRedirect, isConcurrent);
    // printf("check exit on: %s\n", args[0]);
    if (isRedirect) {
      continue;
    }
    if (!exitCheck(args[0])) {
      // printf("\t No Exit, Command Received: %s\n", args[0]);
      executeCommand(args, isConcurrent, isRedirect, &isChild, glts);
    } else {
      // printf("\tExit command received.\n");
      shouldRun = false;
    }
    if (isChild) {
      return 0;
    }
    i++;
  }

  // printf("Exiting shell...\n");
  exit(0);
  return 0;
}
