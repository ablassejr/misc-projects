#include <stdio.h>
#include <sys/types.h>
#include <threads.h>
#include <unistd.h>

int main() {
  pid_t pid;
  int *input;
  thrd_t *thread;
  printf("Enter a number: ");
  if (scanf("%d", input)) {
    pid = fork();
    if (pid == 0) {
      thrd_start_t primefunc(int);
      printf("Process ID: %d\n", pid);
      thrd_create(thread, primefunc(*input), input);
    } else if (pid == -1) {
      printf("Error\n");
      return -1;
    }
  } else {
    do {
      printf("Invalid input\n Input your number again: ");
    } while (!(scanf("%d", input)));
  }
  return 0;
}

thrd_start_t primefunc(int userInput) {
  // printf("Function Started\n");
  int check = 0;
  // printf("check: %d\n", check);
  printf("Prime Numbers Less Than or Equal To %d:\n", userInput);
  for (int i = 1; i <= userInput; i++) {
    // printf("Current number: %d\n", i);
    if (i == 1)
      continue;
    else {
      for (int j = 2; j <= i; j++) {
        // printf("Inner Iteration: %d check: %d\n", j, check);
        if (i % j == 0) {
          check++;
        }
      }
      if (check <= 1)
        printf("%d ", i);
      check = 0;
    }
  }
  return 0;
}
