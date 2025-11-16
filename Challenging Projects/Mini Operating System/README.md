# Mini Operating System

## Overview
Build a minimal operating system from scratch to understand how computers really work at the lowest level - from bootloading to scheduling to file systems.

## The Challenge
This project **combines low-level hardware interaction, systems programming, and computer architecture**. You'll learn what happens between pressing the power button and seeing a login screen.

## Core Features to Implement

### Phase 1: Bootloader
- [ ] Boot sector code (first 512 bytes)
- [ ] Switch from 16-bit real mode to 32-bit protected mode
- [ ] Load kernel from disk into memory
- [ ] Jump to kernel entry point

### Phase 2: Kernel Basics
- [ ] Screen output (VGA text mode)
- [ ] Keyboard input
- [ ] Interrupt handling (IDT setup)
- [ ] Basic shell/command prompt

### Phase 3: Memory Management
- [ ] Physical memory manager
- [ ] Virtual memory (paging)
- [ ] Heap allocator (malloc/free)
- [ ] Memory protection

### Phase 4: Process Management
- [ ] Process creation
- [ ] Context switching
- [ ] Scheduler (round-robin or priority-based)
- [ ] System calls

### Phase 5: File System
- [ ] Simple file system (like FAT or ext2 subset)
- [ ] File operations (create, read, write, delete)
- [ ] Directory support
- [ ] Disk I/O

### Advanced Features (Optional)
- [ ] Multi-core support
- [ ] Network stack (TCP/IP)
- [ ] Device drivers
- [ ] User space programs
- [ ] ELF executable loading
- [ ] IPC (Inter-Process Communication)

## Key Concepts

### Boot Process
1. **BIOS/UEFI** loads first sector (boot sector)
2. **Bootloader** loads kernel into memory
3. **Kernel** initializes hardware and starts first process
4. **Init process** starts system services

### Memory Management
- **Segmentation:** Legacy x86 memory model
- **Paging:** Modern virtual memory
- **Page tables:** Map virtual to physical addresses
- **TLB:** Translation Lookaside Buffer cache

### Process Scheduling
- **Cooperative:** Processes yield voluntarily
- **Preemptive:** Timer interrupts force context switch
- **Round-robin:** Each process gets equal time
- **Priority-based:** Important processes run first

### Interrupts
- **Hardware interrupts:** Keyboard, timer, disk
- **Software interrupts:** System calls
- **IDT:** Interrupt Descriptor Table
- **ISR:** Interrupt Service Routine

## Learning Objectives
- Understanding boot process
- Working with assembly language
- Memory management (virtual and physical)
- Process scheduling and context switching
- Interrupt handling
- File system design
- Hardware interaction
- System call interface

## Technology Suggestions

### Architecture
- **x86 (32-bit):** Most resources available, well-documented
- **x86-64:** Modern, but more complex
- **ARM:** Good for embedded, Raspberry Pi
- **RISC-V:** Open architecture, increasingly popular

### Language
- **Assembly:** For boot code and low-level initialization
- **C:** Most of kernel
- **Rust:** Modern alternative, memory safety
- **C++:** Possible but adds complexity

### Tools
- **QEMU:** Emulator for testing
- **Bochs:** x86 emulator with excellent debugging
- **NASM/GAS:** Assemblers
- **GCC/Clang:** Cross-compiler
- **GDB:** Debugging

## Implementation Tips

1. **Use an Emulator:** QEMU/Bochs, don't test on real hardware initially
2. **Start Small:** Get "Hello World" on screen first
3. **Read OSDev Wiki:** Comprehensive resource
4. **Follow Tutorials:** Many good step-by-step guides
5. **Study Existing OSes:** Look at Linux, xv6, Minix source code
6. **Debug Early:** Set up debugging tools from the start

## Milestones

### Milestone 1: Bare Bones
- Boot and display text on screen
- No keyboard, no nothing, just text

### Milestone 2: Basic I/O
- Keyboard input
- Text output
- Simple command prompt

### Milestone 3: Memory Management
- Physical memory manager
- Virtual memory with paging
- Heap allocator

### Milestone 4: Multitasking
- Create processes
- Context switching
- Preemptive scheduler

### Milestone 5: File System
- Simple file system
- Read/write files
- Directory navigation

## Recommended Tutorials

### OSDev Wiki
- [Bare Bones](https://wiki.osdev.org/Bare_Bones) - Minimal kernel
- [Meaty Skeleton](https://wiki.osdev.org/Meaty_Skeleton) - Better structure
- Comprehensive hardware documentation

### Book/Course-Based
- [Writing a Simple Operating System from Scratch](https://www.cs.bham.ac.uk/~exr/lectures/opsys/10_11/lectures/os-dev.pdf) - Nick Blundell's book
- [Making a RISC-V Operating System using Rust](https://osblog.stephenmarz.com/) - Modern approach
- [xv6: A simple Unix-like teaching OS](https://pdos.csail.mit.edu/6.828/2020/xv6.html) - MIT course
- [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/) - Theory

### Video Series
- [Writing an OS in Rust](https://os.phil-opp.com/) - Philipp Oppermann's blog
- Various YouTube tutorials for x86 OS development

## Example Boot Sector (x86)

```nasm
; Simple boot sector that prints "Hello"
[bits 16]
[org 0x7c00]

start:
    mov si, hello
    call print_string
    jmp $

print_string:
    mov ah, 0x0e
.loop:
    lodsb
    cmp al, 0
    je .done
    int 0x10
    jmp .loop
.done:
    ret

hello: db 'Hello, OS World!', 0

times 510-($-$$) db 0
dw 0xaa55
```

## Resources
- [OSDev Wiki](https://wiki.osdev.org/) - Essential resource
- [Bran's Kernel Development](http://www.osdever.net/bkerndev/Docs/intro.htm) - Classic tutorial
- [JamesM's Kernel Tutorial](https://web.archive.org/web/20160326062442/http://jamesmolloy.co.uk/tutorial_html/index.html) - Popular guide
- [Linux Kernel Source](https://github.com/torvalds/linux) - Real-world example
- [xv6 Source](https://github.com/mit-pdos/xv6-public) - Educational Unix-like OS
- [SerenityOS](https://github.com/SerenityOS/serenity) - Modern from-scratch OS

## Extensions
- **Graphics mode:** VGA, VESA, framebuffer
- **Sound:** Audio drivers
- **Networking:** Network card drivers, TCP/IP stack
- **Multi-core:** SMP (Symmetric Multi-Processing)
- **GUI:** Window manager and desktop
- **Package manager:** Install software
- **Programming language support:** Run Python, Lua, etc.
- **Port applications:** Vim, Git, GCC

## Common Pitfalls
- Not understanding memory layout (stack, heap, code)
- Forgetting to disable interrupts during critical sections
- Page faults from incorrect paging setup
- Not testing on real hardware before claiming it works
- Underestimating complexity of device drivers
- Memory corruption from incorrect allocator

## Hardware Concepts You'll Learn

### CPU Modes
- Real mode (16-bit, BIOS)
- Protected mode (32-bit)
- Long mode (64-bit)

### Privilege Rings
- Ring 0: Kernel mode
- Ring 3: User mode
- Ring 1-2: Rarely used

### I/O
- Port I/O (in/out instructions)
- Memory-mapped I/O (MMIO)
- DMA (Direct Memory Access)

## Estimated Time
- **Bootloader + basic output:** 1-2 weeks
- **Basic kernel with I/O:** 1-2 months
- **With memory management:** 3-4 months
- **Multitasking:** 4-6 months
- **File system:** 6-12 months
- **Production-ready:** Years (Linux started in 1991!)

## Advice from Developers
- Start with tutorials, don't try to be original yet
- Read and understand x86 architecture manuals
- Use version control from day one
- Document your code extensively
- Join OSDev community for help
- Expect to rewrite everything at least once
- Be patient - this is a marathon, not a sprint

---

*From Austin Z. Henley's "Challenging Projects Every Programmer Should Try"*
