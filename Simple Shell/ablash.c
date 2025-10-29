// Program: ablashell.c
// Programmer: Ablasse Kingcaid-Ouedraogo
// Assignment: Project 1
// Purpose: A shell implementation in C
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#define true 1
#define false 0

// function prototypes
void executeCommand(int isConcurrent);
void input();
int exitCheck();
void handleRedirect(char *redirectSign, char *commandString[]);

static char hisBuf[100 / 2 + 1];
char glts;
char *filename = NULL;
char buf[100];
char *cmd[100 / 2 + 1];
int isConcurrent = 0;
int isRedirect = 0;

int main()
{

  // variable declarations

  char *args[100 / 2 + 1];


  // and definitions
  int shouldRun = true;
  char *shellDis = "lash⚟";
  // execution
  system("clear");
  while (shouldRun)
  {
    filename = NULL;
    isConcurrent = 0; 
    for (int j = 0; j < 100 / 2 + 1; j++)
    {
      args[j] = NULL;
    }
    // printf("Last Command: %s\n", historyBuffer);
    printf("%s ", shellDis);
    input();
    // printf("Redirect: %d, Concurrent: %d\n", isRedirect, isConcurrent);
    // printf("check exit on: %s\n", args[0]);

    if (!exitCheck())
    {
      // printf("\t No Exit, Command Received: %s\n", args[0]);
      executeCommand(isConcurrent);
    }
    else
    {
      // printf("\tExit command received.\n");
      shouldRun = false;
    }
  }

  // printf("Exiting shell...\n");
  free(filename);
  exit(0);
  return 0;
}

//*******************************************************************
// Function to execute a command using execvp
void executeCommand(int isConcurrent)
{
  pid_t pid = fork();

  if (pid > 0)
  {
    // Parent process
    if (!isConcurrent)
    {
      // Wait for child to complete
      wait(NULL);
    }
    else {
      printf("executing concurrently\n");
    }
  }
  else if (pid == 0)
  {
    if (isRedirect)
    {
      char *commandString[100 / 2 + 1];
      int i = 0;
      while (cmd[i] != NULL && i < 100 / 2)
      {
        if (strcmp(cmd[i], "<") == 0 || strcmp(cmd[i], ">") == 0)
        {
      filename = cmd[i + 1];
          break; // Stop parsing
        }
        commandString[i] = cmd[i];
        i++;
      }
      handleRedirect(&glts, commandString);
    }
      // Child process - execute the command
      if (execvp(cmd[0], cmd) == -1)
      {
        perror("Error executing command");
        exit(1);
      }
  }
  else
  {
    perror("Fork failed");
  }
}
//*******************************************************************
// Function to get user input and parse it into command and arguments
void input()
{
  fflush(NULL);
  // Variable Declarations
  char *arg = NULL, *gltsptr = NULL;
  int i = 0;
  char *ampersand;
  fgets(buf, 100, stdin);
 if ((ampersand = strchr(buf, '&')) != NULL)
  {
    *ampersand = '\0';
    isConcurrent = 1;
  }
  // Handle History Command
  if (!strcmp(buf, "!!\n"))
  {
    if (strlen(hisBuf) == 0)
    {
      printf("No commands in history.\n");
      buf[0] = '\0';
    }

    strcpy(buf, hisBuf);
    // printf("Repeating Command: %s\n", buf);
  }
  strcpy(hisBuf, buf); // Update history buffer
  // Process Input
  //printf("buffer: %s\n", buf);
  strcpy(buf, strtok(buf, "\n"));
  arg = strtok(buf, " ");
  i = 0;
  while (arg != NULL && i < 100 / 2)
  {
    cmd[i] = arg;
    char *gtlsPtr = NULL;
    if (strcmp(cmd[i], "<") == 0)
    {
      //printf("input redirect found\n");
      isRedirect = 1;
      glts = '<';
    }
    else if (strcmp(cmd[i], ">") == 0)
    {
      //printf("output redirect found\n");
      isRedirect = 1;
      glts = '>';
    }
    //printf("argument %d: %s\n", i, cmd[i]);
    i++;
    arg = strtok(NULL, " ");
  }


 



  //  else
  //{
  // arg = strtok(buf, " \n");
  // i = 0;
  // while (arg != NULL && i < 100 / 2)
  //{
  // cmd[i] = arg;
  //// printf("argument %d: %s\n", i, cmd[i]);
  // i++;
  // arg = strtok(NULL, " \n");
  //}
  // cmd[i] = NULL;
  //}
}

//*******************************************************************
// Function to handle redirection
void handleRedirect(char *redirectSign, char *commandString[])
{
  int fd;
    switch (*redirectSign)
    {
    case '<':
      fd = open(filename, O_RDWR);
      if (fd == -1)
      {
        perror("Error opening file for input");
        exit(1);
      }
      dup2(fd, STDIN_FILENO);
      close(fd);
      break;
    case '>':
      fd = open(filename, O_RDWR);
      if (fd == -1)
      {
        perror("Error opening file for output");
        exit(1);
      }
      dup2(fd, STDOUT_FILENO);
      close(fd);
      break;
    }

    // Execute command with its arguments
    if (execvp(commandString[0], commandString) == -1)
    {
      perror("Error executing command");
      exit(1);
    }
  }

//*******************************************************************
// Function to check if the command is "exit"
int exitCheck()
{
  if (cmd[0] == NULL)
  {
    return false;
  }
  if (!strcmp(cmd[0], "exit"))
  {
    system("clear");
    return true;
  }
  else
  {
    return false;
  }
}