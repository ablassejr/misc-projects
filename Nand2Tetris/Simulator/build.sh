#!/bin/bash

# Build script for Nand2Tetris Simulator
# Based on instructions in README.md

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_DIR="$SCRIPT_DIR/InstallDir"
BIN_DIR="$INSTALL_DIR/bin"
LIB_DIR="$BIN_DIR/lib"
CLASSES_DIR="$BIN_DIR/classes"

echo "Building Nand2Tetris Simulator..."

# Create necessary directories
mkdir -p "$LIB_DIR"
mkdir -p "$CLASSES_DIR"
mkdir -p "$INSTALL_DIR/builtInChips"
mkdir -p "$INSTALL_DIR/builtInVMCode"

# Temporary build directory
TMP_DIR="$SCRIPT_DIR/tmp_build"
rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

# 1. Build Hack.jar
echo "Building Hack.jar..."
find "$SCRIPT_DIR/HackPackageSource" -name "*.java" -print0 | xargs -0 javac -d "$TMP_DIR"
(cd "$TMP_DIR" && jar cf "$LIB_DIR/Hack.jar" Hack/)

# 2. Build HackGUI.jar
echo "Building HackGUI.jar..."
rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"
find "$SCRIPT_DIR/HackGUIPackageSource" -name "*.java" -print0 | xargs -0 javac -cp "$LIB_DIR/Hack.jar" -d "$TMP_DIR"
(cd "$TMP_DIR" && jar cf "$LIB_DIR/HackGUI.jar" HackGUI/)

# 3. Build Compilers.jar
echo "Building Compilers.jar..."
rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"
find "$SCRIPT_DIR/CompilersPackageSource" -name "*.java" -print0 | xargs -0 javac -cp "$LIB_DIR/Hack.jar:$LIB_DIR/HackGUI.jar" -d "$TMP_DIR"
(cd "$TMP_DIR" && jar cf "$LIB_DIR/Compilers.jar" Hack/)

# 4. Build Simulators.jar
echo "Building Simulators.jar..."
rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"
find "$SCRIPT_DIR/SimulatorsPackageSource" -name "*.java" -print0 | xargs -0 javac -cp "$LIB_DIR/Hack.jar:$LIB_DIR/HackGUI.jar:$LIB_DIR/Compilers.jar" -d "$TMP_DIR"
(cd "$TMP_DIR" && jar cf "$LIB_DIR/Simulators.jar" Hack/)

# 5. Build SimulatorsGUI.jar
echo "Building SimulatorsGUI.jar..."
rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"
find "$SCRIPT_DIR/SimulatorsGUIPackageSource" -name "*.java" -print0 | xargs -0 javac -cp "$LIB_DIR/Hack.jar:$LIB_DIR/HackGUI.jar:$LIB_DIR/Compilers.jar:$LIB_DIR/Simulators.jar" -d "$TMP_DIR"
(cd "$TMP_DIR" && jar cf "$LIB_DIR/SimulatorsGUI.jar" SimulatorsGUI/)

# 6. Build BuiltInChips
echo "Building BuiltInChips..."
rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"
find "$SCRIPT_DIR/BuiltInChipsSource" -name "*.java" -print0 | xargs -0 javac -cp "$LIB_DIR/Hack.jar:$LIB_DIR/HackGUI.jar:$LIB_DIR/Compilers.jar:$LIB_DIR/Simulators.jar:$LIB_DIR/SimulatorsGUI.jar" -d "$TMP_DIR"
cp -r "$TMP_DIR"/* "$INSTALL_DIR/builtInChips/"

# 7. Build BuiltInVMCode
echo "Building BuiltInVMCode..."
if [ -d "$SCRIPT_DIR/BuiltInVMCodeSource" ]; then
  rm -rf "$TMP_DIR"
  mkdir -p "$TMP_DIR"
  find "$SCRIPT_DIR/BuiltInVMCodeSource" -name "*.java" -print0 | xargs -0 javac -cp "$LIB_DIR/Hack.jar:$LIB_DIR/Simulators.jar" -d "$TMP_DIR"
  cp -r "$TMP_DIR"/* "$INSTALL_DIR/builtInVMCode/"
fi

# 8. Build MainClasses
echo "Building MainClasses..."
find "$SCRIPT_DIR/MainClassesSource" -name "*.java" -print0 | xargs -0 javac -cp "$LIB_DIR/Hack.jar:$LIB_DIR/HackGUI.jar:$LIB_DIR/Compilers.jar:$LIB_DIR/Simulators.jar:$LIB_DIR/SimulatorsGUI.jar" -d "$CLASSES_DIR"

# Cleanup
rm -rf "$TMP_DIR"

echo "Build complete!"
echo "You can now run the simulators from $INSTALL_DIR"
