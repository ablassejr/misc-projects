#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

void executeCommand(char *args[], int isConcurrent);
int input(char *cmd[]);
int exitCheck(char *cmd);
