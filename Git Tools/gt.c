#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

enum GitTool { GH, GIT };

int main(int argc, char *argv[]) {
  char *filename = argv[0];
  char *command = argv[1];
  enum GitTool tool;
  printf("Git Tools - Command Line Interface\n");
  printf("----------------------------------------\n");
  printf("Running command: %s %s\n", command, argv[2]);
  strcmp(argv[1], "git") == 0  ? tool = GIT
  : strcmp(argv[1], "gh") == 0 ? tool = GH
                               : exit(1);
  switch (tool) {
  case GIT:
    printf("Using Git tool\n");
    break;
  case GH:
    printf("Using GitHub CLI tool\n");
    break;
  }
  return 0;
}
