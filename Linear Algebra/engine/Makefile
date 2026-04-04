CXX = c++
CXXFLAGS = -O2 -fPIC -Wall -Wextra -std=c++17 -Iinclude
SOURCES = $(wildcard src/*.cpp)
OBJECTS = $(SOURCES:src/%.cpp=build/%.o)

.PHONY: all clean

all: build/liblinalgcore.dylib build/liblinalgcore.a

build/liblinalgcore.dylib: $(OBJECTS)
	$(CXX) -dynamiclib -o $@ $^

build/liblinalgcore.a: $(OBJECTS)
	ar rcs $@ $^

build/%.o: src/%.cpp | build
	$(CXX) $(CXXFLAGS) -c $< -o $@

build:
	mkdir -p build

clean:
	rm -rf build
