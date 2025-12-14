# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

This is a Maven project using Java 25.

```bash
# Compile
mvn compile

# Clean and compile
mvn clean compile

# Run the main class
mvn exec:java -Dexec.mainClass="barber.Main"
```

## Architecture

This project implements the classic **Sleeping Barber Problem** - a concurrency synchronization problem.

### Components

- **Shop** (singleton): Central coordinator that manages waiting chairs, customer queue, and the barber. Generates customers at random intervals (10ms-10s). Has 3 waiting chairs.
- **Barber** (singleton): Can be sleeping or awake. Cuts hair with a 5-second delay. Wakes when a customer arrives while sleeping.
- **Customer**: Created with an ID and a shop reference. Checks into the shop on creation. Leaves if no chairs available.
- **IO**: Utility class for output (referenced but not yet implemented - needs `IO.println()` method).

### Threading Model

- Shop spawns a thread to generate customers over time
- Each Customer and Barber has an associated Thread object
- Synchronization is handled via `synchronized` methods on Barber

### Known Issues

- `IO` class is missing - code references `IO.println()` but the class doesn't exist
- `Main.main()` is not public and has no `String[] args` parameter
- Customer generation thread is created but never started (`.start()` not called)
