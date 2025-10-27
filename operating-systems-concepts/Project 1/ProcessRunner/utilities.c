#include "utilities.h"

#define true 1
#define false 0

// Function to execute a command using execvp
void executeCommand(char *args[], int isConcurrent) {
  pid_t pid = fork();
  pid_t currentpid = getpid();

  printf("Executing Cmd %s\n\n", args[0]);
  if (pid > 0) {
    printf("Parent process %d:\n", getpid());
    if (!isConcurrent) {
      printf("\tWaiting for child process %d to complete...\n", pid);
      wait(NULL);
      printf("\tChild process %d completed.\n", pid);
    } else {
      printf("\tExecuting process %d\n", pid);
    }
  } else if (pid == 0) {
    printf("Child process %d: \n", getpid());
    if (execvp(args[0], args) == -1) {
      printf("Error executing command %s\n", args[0]);
    }
  } else {
    printf("Fork failed.\n");
  }
}

// Function to get user input and parse it into command and arguments
int input(char *cmd[]) {
  static char buf[100];
  char *arg;
  int i = 0;
  int ampersandFound = 0;
  char *item;
  fgets(buf, 100, stdin);

  if (strchr(buf, '&'))
    ampersandFound = 1;

  // printf("buffer: %s\n", buf);
  arg = strtok(buf, " ");
  cmd[0] = arg;
  i = 1;
  while (i < 100 / 2 && (arg = strtok(NULL, " ")) != NULL) {
    cmd[i] = arg;
    printf("argument %d: %s\n", i, cmd[i]);
    i++;
  }
  cmd[i] = NULL;
  return ampersandFound;
}

// Function to check if the command is "exit"
int exitCheck(char *cmd) {
  if (cmd && !strcmp(cmd, "exit\n")) {
    return true;
  } else {
    return false;
  }
}
