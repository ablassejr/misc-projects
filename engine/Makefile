CC = cc
CFLAGS = -O2 -fPIC -Wall -Wextra -std=c11 -Iinclude
SOURCES = $(wildcard src/*.c)
OBJECTS = $(SOURCES:src/%.c=build/%.o)

.PHONY: all clean

all: build/liblinalgcore.dylib build/liblinalgcore.a

build/liblinalgcore.dylib: $(OBJECTS)
	$(CC) -dynamiclib -o $@ $^

build/liblinalgcore.a: $(OBJECTS)
	ar rcs $@ $^

build/%.o: src/%.c | build
	$(CC) $(CFLAGS) -c $< -o $@

build:
	mkdir -p build

clean:
	rm -rf build
