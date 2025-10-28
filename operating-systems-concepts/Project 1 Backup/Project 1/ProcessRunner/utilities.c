#include "utilities.h"

#define true 1
#define false 0

//*******************************************************************
// Function to execute a command using execvp
void executeCommand(char *args[], int isConcurrent, int isRedirect,
                    int *childFlag, char redirectSign)
{
  pid_t pid = fork();
  pid_t currentpid = getpid();

  if (pid > 0)
  {
    // printf("Parent process %d:\n", getpid());

    if (!isConcurrent)
    {
      // printf("\tWaiting for child process %d to complete...\n", pid);
      wait(NULL);
      // printf("\tChild process %d completed.\n", pid);
    } // else {
      // printf("\tExecuting process %d\n", pid);
    //}
  }
  else if (pid == 0)
  {
    printf("Child process %d: \n", getpid());
    *childFlag = true;
    if (execvp(args[0], args) == -1)
    {
      printf("\tError executing command\n");
      exit(1);
    }
  }
  else
  {
    printf("Fork failed.\n");
  }
}
//*******************************************************************
// Function to get user input and parse it into command and arguments
int *input(char *cmd[], char hisBuf[], char glts)
{
  // Variable Declarations
  static char buf[100];
  char *arg, *gltsptr = malloc(10 * sizeof(char));
  int i = 0;
  int ampersandFound = 0, gltsFound = 0;
  char *item;
  char *ampersand;
  int *flags = malloc(2 * sizeof(int));
  char *charBuffer = malloc(1 * sizeof(char) + 1);
  void handleRedirect(char *args, char *redirectSign,
                      char *cmd); // Function Prototype
  // Input
  fgets(buf, 100, stdin);

  // Handle History Command
  if (!strcmp(buf, "!!\n"))
  {
    if (strlen(hisBuf) == 0)
    {
      printf("No commands in history.\n");
      buf[0] = '\0';
      flags[0] = ampersandFound;
      flags[1] = gltsFound;
      return flags;
    }

    strcpy(buf, hisBuf);
    // printf("Repeating Command : %s\n", buf);
  }

  strcpy(hisBuf, buf); // Update history buffer

  if ((ampersand = strstr(buf, " &\n")))
  {
    *ampersand = '\0';
    ampersandFound = 1;
  }

  if ((gltsptr = strpbrk(buf, "<>")) != NULL)
  {
    gltsFound = 1;
    glts = *gltsptr;

    // Parse the command line
    arg = strtok(buf, " \n");
    int i = 0;
    while (arg != NULL && i < 100 / 2)
    {
      // Skip the redirect symbol
      if (strcmp(arg, "<") != 0 && strcmp(arg, ">") != 0)
      {
        cmd[i] = arg;
        i++;
      }
      arg = strtok(NULL, " \n");
    }
    cmd[i] = NULL;

    // cmd[0] should be the command, cmd[1] should be the filename
    if (cmd[0] != NULL && cmd[1] != NULL)
    {
      handleRedirect(cmd[1], &glts, cmd[0]);
    }
  }
  // printf(gbuffer: %s\ng, buf);
  //  arg = strtok(buf, " ");
  //  cmd[0] = arg;
  //  i = 1;
  else
  {
    arg = strtok(buf, " \n");
    i = 0;
    while (arg != NULL && i < 100 / 2)
    {
      cmd[i] = arg;
      // printf("argument %d: %s\n", i, cmd[i]);
      i++;
      arg = strtok(NULL, " ");
    }
    cmd[i] = NULL;
  }
  flags[0] = ampersandFound;
  flags[1] = gltsFound;
  return flags;
}

//*******************************************************************
// Function to handle redirection
void handleRedirect(char *args, char *redirectSign, char *cmd)
{
  int fd;
  int i = 0, isInput;

  char *filename = args;
  pid_t pid = fork();
  if (pid > 0)
  {
    wait(NULL);
  }
  else if (pid == 0)
  {
    switch (*redirectSign)
    {
    case '<':
      fd = open(filename, O_RDONLY);
      dup2(fd, STDIN_FILENO);
      close(fd);
      isInput = 1;
      break;
    case '>':
      fd = open(filename, O_WRONLY | O_CREAT | O_TRUNC, 0644);
      if (fd == -1)
      {
        perror("Error opening file for output");
        exit(1);
      }
      dup2(fd, STDOUT_FILENO);
      close(fd);
      isInput = 0;
      break;
    }

    // Create argv array for execvp
    char *argv[] = {cmd, NULL};
    if (execvp(cmd, argv) == -1)
    {
      perror("Error executing command");
      exit(1);
    }
  }
}

//*******************************************************************
// Function to check if the command is "exit"
int exitCheck(char *cmd)
{
  if (cmd && !strcmp(cmd, "exit"))
  {
    system("clear");
    return true;
  }
  else
  {
    return false;
  }
}
