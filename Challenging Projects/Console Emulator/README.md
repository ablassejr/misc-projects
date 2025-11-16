# Video Game Console Emulator

## Overview
Build an emulator for a vintage video game console to understand how hardware works at the lowest level. This project **combines the challenges of writing a compiler, an operating system, and a game engine all into one**.

## The Challenge
Accurately simulating hardware behavior in software requires understanding:
- CPU instruction sets and timing
- Memory mapping and I/O
- Graphics rendering
- Sound synthesis
- Input handling
- Synchronization and timing

## Recommended Learning Path

### Start Here: CHIP-8 (Beginner)
**Why:** Not a real console, but perfect for learning
- Only 35 instructions
- Simple graphics (64×32 monochrome)
- Well-documented
- Can complete in a weekend
- **Time:** 1-2 weeks

### Next: Game Boy (Intermediate)
**Why:** Real console, manageable complexity
- Sharp LR35902 CPU (similar to Z80)
- ~500 instructions
- Tile-based graphics
- Extensive documentation
- Large game library
- **Time:** 2-4 months

### Advanced: NES (Nintendo Entertainment System)
**Why:** Classic console, well-documented
- MOS 6502 CPU
- PPU (Picture Processing Unit) for graphics
- APU (Audio Processing Unit)
- Mapper chips add complexity
- **Time:** 4-6 months

### Expert: SNES, PlayStation, N64
**Why:** Complex architectures, 3D graphics
- Multiple processors
- Complex graphics pipelines
- Extensive timing requirements
- **Time:** 6-12+ months each

## Core Components to Implement

### CPU Emulation
- [ ] Fetch-decode-execute cycle
- [ ] All CPU instructions
- [ ] Registers and flags
- [ ] Memory access
- [ ] Accurate timing/cycle counts

### Memory Management
- [ ] Memory map implementation
- [ ] ROM loading
- [ ] RAM
- [ ] Memory-mapped I/O
- [ ] Bank switching (if applicable)

### Graphics (PPU/GPU)
- [ ] Frame buffer
- [ ] Sprites
- [ ] Background/tiles
- [ ] Scrolling
- [ ] Display synchronization (V-Sync)

### Sound (APU)
- [ ] Sound channels (pulse, triangle, noise)
- [ ] Sound synthesis
- [ ] Audio buffer
- [ ] Synchronization with frame rate

### Input
- [ ] Controller/keyboard mapping
- [ ] Button states
- [ ] Polling vs interrupt-driven

### Cartridge/ROM
- [ ] ROM loading
- [ ] Save states
- [ ] Battery-backed RAM

## Key Concepts

### CPU Instruction Cycle
```
while (running) {
    opcode = fetch()
    decode(opcode)
    execute(opcode)
    update_timers()
    handle_interrupts()
}
```

### Memory Mapping Example (Game Boy)
```
0x0000-0x3FFF: ROM Bank 0
0x4000-0x7FFF: ROM Bank 1-N (switchable)
0x8000-0x9FFF: Video RAM
0xA000-0xBFFF: External RAM
0xC000-0xDFFF: Work RAM
0xFE00-0xFE9F: Sprite Attribute Table
0xFF00-0xFF7F: I/O Registers
0xFF80-0xFFFE: High RAM
0xFFFF: Interrupt Enable Register
```

### Timing Synchronization
- CPU runs at specific clock speed (e.g., 4.19 MHz for Game Boy)
- Graphics update at fixed rate (e.g., 60 FPS)
- Must sync emulation speed to real hardware
- Use frame limiting and sleep

## Learning Objectives
- Understanding CPU architectures
- Implementing instruction sets
- Memory-mapped I/O
- Graphics rendering techniques
- Sound synthesis
- Timing and synchronization
- Debugging complex systems
- Reading technical specifications

## Technology Suggestions

### Language
- **C/C++:** Traditional choice, good performance
- **Rust:** Memory safety, modern features
- **Python:** Rapid prototyping (slower, but okay for CHIP-8)
- **JavaScript:** Can run in browser
- **Go:** Good balance of speed and ease

### Graphics Libraries
- **SDL2:** Cross-platform, widely used
- **SFML:** Easy-to-use, C++
- **OpenGL:** If you want low-level control
- **HTML Canvas:** For web-based emulators

### Audio Libraries
- **SDL_mixer:** Simple audio playback
- **miniaudio:** Single-header library
- **PortAudio:** Cross-platform

## CHIP-8 Specifications

### CPU
- 16 8-bit registers (V0-VF)
- 1 16-bit index register (I)
- 16-bit program counter (PC)
- 8-bit stack pointer (SP)
- 16-level stack

### Memory
- 4KB RAM (4096 bytes)
- Program starts at 0x200
- Font data at 0x000-0x1FF

### Display
- 64×32 pixels
- Monochrome
- XOR drawing

### Input
- 16-key hexadecimal keypad (0-F)

### Timers
- 60Hz delay timer
- 60Hz sound timer

### Example Instructions
```
00E0: Clear screen
1NNN: Jump to address NNN
6XNN: Set register VX to NN
7XNN: Add NN to register VX
ANNN: Set index register to NNN
DXYN: Draw sprite
```

## Implementation Tips

1. **Start with CHIP-8:** Don't jump straight to Game Boy
2. **CPU First:** Get instruction execution working
3. **Test ROMs:** Use test ROMs to verify correctness
4. **Logging:** Extensive logging helps debugging
5. **Debugger:** Build a debugger into your emulator
6. **Accuracy vs Speed:** Start accurate, optimize later
7. **Reference Emulators:** Study existing open-source emulators

## Milestones

### Milestone 1: CPU Only (CHIP-8)
- Implement all 35 instructions
- Run test ROM
- Verify with logs

### Milestone 2: Graphics (CHIP-8)
- Implement display
- Draw sprites
- See something on screen

### Milestone 3: Full CHIP-8
- Add input
- Add timers
- Play simple games (Pong, Space Invaders)

### Milestone 4: Game Boy CPU
- Implement LR35902 instruction set
- Pass CPU test ROMs (Blargg's tests)

### Milestone 5: Game Boy Graphics
- Implement PPU
- Render tiles and sprites
- Display game graphics

### Milestone 6: Playable Game Boy
- Add input
- Add sound
- Play Tetris or Pokemon

## Resources

### CHIP-8
- [Cowgod's CHIP-8 Reference](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM) - Complete spec
- [CHIP-8 Test ROM](https://github.com/corax89/chip8-test-rom)
- [Awesome CHIP-8](https://github.com/tobiasvl/awesome-chip-8) - Curated resources

### Game Boy
- [Pan Docs](https://gbdev.io/pandocs/) - Complete Game Boy documentation
- [Game Boy CPU Manual](http://marc.rawer.de/Gameboy/Docs/GBCPUman.pdf) - CPU reference
- [Blargg's Test ROMs](https://github.com/retrio/gb-test-roms) - Comprehensive tests
- [The Ultimate Game Boy Talk](https://www.youtube.com/watch?v=HyzD8pNlpwI) - Excellent video

### NES
- [NESDev Wiki](https://www.nesdev.org/wiki/Nesdev_Wiki) - Comprehensive resource
- [6502 Reference](http://www.6502.org/) - CPU documentation
- [NES Emulator From Scratch](https://bugzmanov.github.io/nes_ebook/) - Tutorial

### General
- [Emulator Development](https://emudev.org/) - Community and resources
- [r/EmuDev](https://www.reddit.com/r/EmuDev/) - Reddit community
- [Awesome Emulators](https://github.com/mcicolella/awesome-emulators) - List of emulators

## Debugging Tips

### Test ROMs
- Use official test ROMs to verify correctness
- Blargg's test suites are comprehensive
- Start with CPU tests before graphics

### Logging
```c
void log_instruction(uint16_t pc, uint8_t opcode) {
    printf("PC: 0x%04X | OP: 0x%02X | A: 0x%02X | Flags: %c%c%c%c\n",
           pc, opcode, cpu.a,
           cpu.flags.z ? 'Z' : '-',
           cpu.flags.n ? 'N' : '-',
           cpu.flags.h ? 'H' : '-',
           cpu.flags.c ? 'C' : '-');
}
```

### Debugger Features
- Step through instructions
- Breakpoints
- Memory viewer
- Register display
- Disassembler

## Common Pitfalls
- Not handling CPU flags correctly
- Incorrect timing (games run too fast/slow)
- Endianness issues (little vs big endian)
- Off-by-one errors in graphics rendering
- Not implementing all edge cases
- Ignoring memory protection
- Sound synchronization issues

## Extensions
- **Save states:** Serialize entire emulator state
- **Debugging tools:** Built-in debugger, disassembler
- **Cheats:** Game Genie/Action Replay codes
- **Fast forward:** Run faster than real-time
- **Rewind:** Replay previous frames
- **Netplay:** Play multiplayer over network
- **Graphics filters:** CRT shader, smoothing
- **Controller support:** Gamepad mapping
- **Multiple systems:** Support multiple consoles

## Performance Optimization
- **JIT compilation:** Compile instructions to native code
- **Cached interpreters:** Pre-decode instructions
- **Graphics optimizations:** Dirty rectangle tracking
- **Multi-threading:** Separate CPU/GPU threads
- **Profile:** Use profiler to find bottlenecks

## Estimated Time
- **CHIP-8:** 1-2 weeks
- **Game Boy:** 2-4 months (playable in 1-2 months)
- **NES:** 4-6 months
- **SNES:** 6-12 months
- **PlayStation:** 12+ months
- **Accurate timing:** Add 50-100% more time

## Success Criteria

### CHIP-8
- All test ROMs pass
- Can play Pong, Space Invaders, Tetris

### Game Boy
- Passes Blargg's CPU tests
- Tetris playable
- Pokemon boots and plays
- Audio works correctly

### NES
- Passes test ROMs
- Super Mario Bros playable
- Zelda works
- Various mappers supported

---

*From Austin Z. Henley's "Challenging Projects Every Programmer Should Try"*
