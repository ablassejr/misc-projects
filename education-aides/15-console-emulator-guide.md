# Console Emulator - Education Aide
## Building a Video Game Emulator from First Principles

### Overview
This guide teaches you how to build a video game console emulator. You'll learn CPU emulation, graphics rendering, and hardware simulation - combining challenges from compilers, operating systems, and game engines.

**Recommended path:** Start with CHIP-8, then Game Boy, then NES!

---

## Part 1: What is Emulation?

### Question 1: Emulation vs Simulation
**Think about this:** What's the difference?

**Your Answer:** _[Write your understanding]_

<details>
<summary>Emulation Concept</summary>

**Emulation:** Replicate exact hardware behavior in software
- Run real game ROMs
- Cycle-accurate timing
- Identical behavior to original hardware

**Simulation:** Approximate behavior
- May not run real ROMs
- Simplified timing
- Good enough for many purposes

**Example:**
- **Emulator:** PS1 emulator runs actual PS1 discs
- **Simulator:** Flight simulator doesn't run real aircraft code

**Why emulate?**
- Preserve old games
- Study hardware architecture
- No need for rare/expensive hardware
- Debugging capabilities
</details>

### Question 2: What Needs to be Emulated?
**Question:** What hardware components?

<details>
<summary>Console Components</summary>

**Typical game console:**
```
┌─────────────────────────────────┐
│  CPU (Central Processing Unit)  │ ← Execute instructions
├─────────────────────────────────┤
│  Memory (RAM)                   │ ← Store data
├─────────────────────────────────┤
│  PPU/GPU (Graphics)             │ ← Render visuals
├─────────────────────────────────┤
│  APU (Audio)                    │ ← Generate sound
├─────────────────────────────────┤
│  Input (Controllers)            │ ← Button presses
├─────────────────────────────────┤
│  Cartridge (ROM)                │ ← Game data
└─────────────────────────────────┘
```

**Each must be emulated!**
</details>

---

## Part 2: CHIP-8 - The Perfect Starting Point

### Why CHIP-8?

**Question:** Why not start with Game Boy or NES?

<details>
<summary>CHIP-8 Advantages</summary>

**CHIP-8 is perfect for learning:**
- Not a real console (interpreted language from 1970s)
- Only 35 instructions
- Simple graphics (64×32 monochrome)
- Simple input (16 keys)
- Can complete in a weekend!
- Tons of documentation

**Complexity comparison:**
- CHIP-8: 35 instructions
- Game Boy: ~500 instructions
- NES: ~150 instructions + PPU complexity
- PlayStation: Multiple processors!

**Start here!**
</details>

### CHIP-8 Specifications

<details>
<summary>Hardware Specifications</summary>

**Memory:**
- 4096 bytes (4KB) of RAM
- Program starts at address 0x200
- Font data at 0x000-0x1FF

**Registers:**
- 16 8-bit registers: V0-VF
- VF is flag register (don't use for storage)
- 1 16-bit index register: I
- 1 16-bit program counter: PC
- 1 8-bit stack pointer: SP

**Display:**
- 64×32 pixels
- Monochrome (on/off)
- Sprites are XORed onto screen

**Timers:**
- Delay timer (60Hz)
- Sound timer (60Hz, beeps when > 0)

**Stack:**
- 16 levels (for subroutine calls)

**Input:**
- 16 keys (0-9, A-F)
```
Keyboard:    CHIP-8:
1 2 3 4      1 2 3 C
Q W E R      4 5 6 D
A S D F      7 8 9 E
Z X C V      A 0 B F
```
</details>

---

## Part 3: Building CHIP-8 Emulator

### Memory and Registers

<details>
<summary>Basic Structure</summary>

```python
class Chip8:
    def __init__(self):
        # Memory
        self.memory = [0] * 4096

        # Registers
        self.V = [0] * 16       # V0-VF
        self.I = 0              # Index register
        self.PC = 0x200         # Program counter (programs start at 0x200)
        self.SP = 0             # Stack pointer

        # Timers
        self.delay_timer = 0
        self.sound_timer = 0

        # Display (64x32 pixels)
        self.display = [[0] * 64 for _ in range(32)]

        # Stack
        self.stack = [0] * 16

        # Input
        self.keys = [0] * 16    # 16 keys (0-F)

        # Load font into memory
        self.load_font()

    def load_font(self):
        """Load built-in font sprites (0-F)"""
        fonts = [
            0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
            0x20, 0x60, 0x20, 0x20, 0x70,  # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
            0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
            0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
            0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
            0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
            0xF0, 0x80, 0xF0, 0x80, 0x80   # F
        ]

        for i, byte in enumerate(fonts):
            self.memory[i] = byte

    def load_rom(self, filename):
        """Load ROM file into memory"""
        with open(filename, 'rb') as f:
            rom = f.read()

        for i, byte in enumerate(rom):
            self.memory[0x200 + i] = byte
```
</details>

### Fetch-Decode-Execute Cycle

<details>
<summary>CPU Cycle</summary>

```python
def cycle(self):
    """Execute one CPU cycle"""
    # Fetch
    opcode = (self.memory[self.PC] << 8) | self.memory[self.PC + 1]

    # Decode and Execute
    self.execute(opcode)

    # Update timers
    if self.delay_timer > 0:
        self.delay_timer -= 1

    if self.sound_timer > 0:
        if self.sound_timer == 1:
            print("BEEP!")  # Play sound
        self.sound_timer -= 1

def execute(self, opcode):
    """Decode and execute opcode"""
    # Extract parts of opcode
    # Opcode format: 0xABCD
    nibble = (opcode & 0xF000) >> 12    # A
    x = (opcode & 0x0F00) >> 8          # B
    y = (opcode & 0x00F0) >> 4          # C
    n = opcode & 0x000F                 # D
    nn = opcode & 0x00FF                # CD
    nnn = opcode & 0x0FFF               # BCD

    # Decode based on first nibble
    if opcode == 0x00E0:
        # 00E0 - Clear screen
        self.display = [[0] * 64 for _ in range(32)]
        self.PC += 2

    elif opcode == 0x00EE:
        # 00EE - Return from subroutine
        self.SP -= 1
        self.PC = self.stack[self.SP]
        self.PC += 2

    elif nibble == 0x1:
        # 1NNN - Jump to NNN
        self.PC = nnn

    elif nibble == 0x2:
        # 2NNN - Call subroutine at NNN
        self.stack[self.SP] = self.PC
        self.SP += 1
        self.PC = nnn

    elif nibble == 0x3:
        # 3XNN - Skip next if VX == NN
        if self.V[x] == nn:
            self.PC += 4
        else:
            self.PC += 2

    elif nibble == 0x6:
        # 6XNN - Set VX to NN
        self.V[x] = nn
        self.PC += 2

    elif nibble == 0x7:
        # 7XNN - Add NN to VX
        self.V[x] = (self.V[x] + nn) & 0xFF
        self.PC += 2

    elif nibble == 0x8:
        # 8XY_ - Arithmetic/logic operations
        if n == 0x0:
            # 8XY0 - Set VX to VY
            self.V[x] = self.V[y]
        elif n == 0x1:
            # 8XY1 - VX = VX OR VY
            self.V[x] |= self.V[y]
        elif n == 0x2:
            # 8XY2 - VX = VX AND VY
            self.V[x] &= self.V[y]
        elif n == 0x4:
            # 8XY4 - VX = VX + VY, VF = carry
            result = self.V[x] + self.V[y]
            self.V[0xF] = 1 if result > 255 else 0
            self.V[x] = result & 0xFF

        self.PC += 2

    elif nibble == 0xA:
        # ANNN - Set I to NNN
        self.I = nnn
        self.PC += 2

    elif nibble == 0xD:
        # DXYN - Draw sprite
        self.draw_sprite(x, y, n)
        self.PC += 2

    else:
        print(f"Unknown opcode: {opcode:04X}")
        self.PC += 2
```
</details>

### Drawing Sprites

<details>
<summary>Graphics Implementation</summary>

```python
def draw_sprite(self, x, y, height):
    """Draw sprite at (VX, VY) with height N"""
    x_pos = self.V[x] % 64
    y_pos = self.V[y] % 32

    self.V[0xF] = 0  # Reset collision flag

    for row in range(height):
        sprite_byte = self.memory[self.I + row]

        for col in range(8):
            # Check if pixel is set
            if (sprite_byte & (0x80 >> col)) != 0:
                # Screen wrapping
                screen_x = (x_pos + col) % 64
                screen_y = (y_pos + row) % 32

                # Check collision
                if self.display[screen_y][screen_x] == 1:
                    self.V[0xF] = 1  # Collision!

                # XOR pixel
                self.display[screen_y][screen_x] ^= 1
```
</details>

### Rendering to Screen

<details>
<summary>Display with Pygame</summary>

```python
import pygame

def render(chip8, screen, scale=10):
    """Render CHIP-8 display to Pygame screen"""
    for y in range(32):
        for x in range(64):
            if chip8.display[y][x]:
                color = (255, 255, 255)  # White
            else:
                color = (0, 0, 0)        # Black

            pygame.draw.rect(screen, color,
                           (x * scale, y * scale, scale, scale))

    pygame.display.flip()

# Main loop
pygame.init()
screen = pygame.display.set_mode((640, 320))
clock = pygame.time.Clock()

chip8 = Chip8()
chip8.load_rom("pong.ch8")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Run multiple cycles per frame (for speed)
    for _ in range(10):
        chip8.cycle()

    render(chip8, screen)
    clock.tick(60)  # 60 FPS

pygame.quit()
```
</details>

---

## Part 4: Moving to Real Hardware - Game Boy

### Game Boy Architecture

<details>
<summary>Game Boy Components</summary>

**CPU:** Sharp LR35902 (Z80-like)
- 8-bit CPU
- 4.19 MHz clock speed
- ~500 instructions

**Memory map:**
```
0x0000-0x3FFF: ROM Bank 0 (16KB)
0x4000-0x7FFF: ROM Bank 1-N (switchable)
0x8000-0x9FFF: Video RAM (VRAM)
0xA000-0xBFFF: External RAM (cartridge)
0xC000-0xDFFF: Work RAM
0xFE00-0xFE9F: Sprite Attribute Table (OAM)
0xFF00-0xFF7F: I/O Registers
0xFF80-0xFFFE: High RAM
0xFFFF: Interrupt Enable
```

**Display:**
- 160×144 pixels
- 4 shades of gray
- Tile-based rendering
- 40 sprites max
- 10 sprites per line

**Sound:**
- 4 channels
- 2 pulse waves
- 1 wave table
- 1 noise
</details>

### CPU Instructions

<details>
<summary>Implementing Instructions</summary>

```python
class GameBoyCPU:
    def __init__(self):
        # 8-bit registers
        self.A = 0  # Accumulator
        self.B = 0
        self.C = 0
        self.D = 0
        self.E = 0
        self.H = 0
        self.L = 0

        # Flags
        self.F = 0  # Flags: Z N H C 0 0 0 0

        # 16-bit registers
        self.SP = 0  # Stack pointer
        self.PC = 0x100  # Program counter (starts at 0x100)

    def execute_instruction(self, opcode):
        """Execute one instruction"""

        # 0x00 - NOP (no operation)
        if opcode == 0x00:
            self.PC += 1
            return 4  # 4 cycles

        # 0x01 - LD BC, nn (load 16-bit immediate into BC)
        elif opcode == 0x01:
            nn = self.read_word(self.PC + 1)
            self.set_BC(nn)
            self.PC += 3
            return 12

        # 0x06 - LD B, n (load 8-bit immediate into B)
        elif opcode == 0x06:
            self.B = self.read_byte(self.PC + 1)
            self.PC += 2
            return 8

        # 0x80 - ADD A, B (add B to A)
        elif opcode == 0x80:
            result = self.A + self.B

            # Set flags
            self.set_flag('Z', (result & 0xFF) == 0)
            self.set_flag('N', False)
            self.set_flag('H', ((self.A & 0xF) + (self.B & 0xF)) > 0xF)
            self.set_flag('C', result > 0xFF)

            self.A = result & 0xFF
            self.PC += 1
            return 4

        # ... 500+ more instructions!

    def set_flag(self, flag, value):
        """Set CPU flag"""
        flags = {'Z': 7, 'N': 6, 'H': 5, 'C': 4}
        bit = flags[flag]

        if value:
            self.F |= (1 << bit)
        else:
            self.F &= ~(1 << bit)

    def get_flag(self, flag):
        """Get CPU flag"""
        flags = {'Z': 7, 'N': 6, 'H': 5, 'C': 4}
        bit = flags[flag]
        return (self.F >> bit) & 1
```
</details>

---

## Part 5: Testing and Debugging

### Test ROMs

<details>
<summary>Using Test ROMs</summary>

**Test ROMs validate correctness:**

**For CHIP-8:**
- chip8-test-rom
- BC_test.ch8

**For Game Boy:**
- Blargg's test ROMs (essential!)
  - cpu_instrs - Tests all instructions
  - instr_timing - Tests cycle accuracy
  - mem_timing - Tests memory timing

**How to use:**
```python
# Load test ROM
chip8.load_rom("test.ch8")

# Run until output appears
while True:
    chip8.cycle()

# Check screen for PASS/FAIL message
```

**Blargg's tests print results to serial port or display**
</details>

### Debugging Tools

<details>
<summary>Debugger Implementation</summary>

```python
class Debugger:
    def __init__(self, emulator):
        self.emu = emulator
        self.breakpoints = set()
        self.step_mode = False

    def add_breakpoint(self, address):
        self.breakpoints.add(address)

    def run(self):
        while True:
            # Check breakpoint
            if self.emu.PC in self.breakpoints:
                print(f"Breakpoint hit at 0x{self.emu.PC:04X}")
                self.print_state()
                self.step_mode = True

            if self.step_mode:
                cmd = input("(s)tep, (c)ontinue, (r)egisters, (m)emory: ")

                if cmd == 's':
                    self.emu.cycle()
                    self.print_state()
                elif cmd == 'c':
                    self.step_mode = False
                elif cmd == 'r':
                    self.print_registers()
                elif cmd == 'm':
                    addr = int(input("Address: "), 16)
                    self.print_memory(addr)
            else:
                self.emu.cycle()

    def print_state(self):
        opcode = self.emu.memory[self.emu.PC]
        print(f"PC: 0x{self.emu.PC:04X}  Opcode: 0x{opcode:02X}")
        self.print_registers()

    def print_registers(self):
        print(f"A: 0x{self.emu.A:02X}  B: 0x{self.emu.B:02X}  "
              f"C: 0x{self.emu.C:02X}  D: 0x{self.emu.D:02X}")
```
</details>

---

## Learning Projects

### Project 1: CHIP-8 (1-2 weeks)
- [ ] Implement all 35 instructions
- [ ] Display rendering
- [ ] Input handling
- [ ] Load and run Pong

### Project 2: CHIP-8 Polish (1 week)
- [ ] Sound (beep on timer)
- [ ] Configurable speed
- [ ] Save states
- [ ] Debugger

### Project 3: Game Boy CPU (4-6 weeks)
- [ ] Implement instruction set
- [ ] Pass Blargg's CPU tests
- [ ] Memory management
- [ ] Timing accuracy

### Project 4: Game Boy Complete (8-12 weeks)
- [ ] PPU (graphics)
- [ ] Sound (APU)
- [ ] Cartridge types (MBC1, MBC3)
- [ ] Play Tetris, Pokemon!

---

## Resources

### CHIP-8
- [Cowgod's CHIP-8 Reference](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM)
- [CHIP-8 Test Suite](https://github.com/corax89/chip8-test-rom)

### Game Boy
- [Pan Docs](https://gbdev.io/pandocs/) - Complete documentation
- [Game Boy CPU Manual](http://marc.rawer.de/Gameboy/Docs/GBCPUman.pdf)
- [Blargg's Test ROMs](https://github.com/retrio/gb-test-roms)

### Communities
- r/EmuDev (Reddit)
- EmuDev Discord
- NesDev forums

---

**Key Takeaways:**

1. **Start with CHIP-8** - Perfect learning platform
2. **Use test ROMs** - Validate correctness
3. **Build debugger** - Essential for development
4. **Be patient** - Emulation is complex!
5. **Study documentation** - Hardware manuals are your friend

---

*"Emulation is understanding hardware by rebuilding it in software."*
