#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

void executeCommand(char *args[], int isConcurrent, int isRedirect,
                    int *childFlag, char redirectSign);
int *input(char *cmd[], char historyBuffer[], char gltsChar);
int exitCheck(char *cmd);
void handleRedirect(char *args, char *redirectSign, char *cmd);
