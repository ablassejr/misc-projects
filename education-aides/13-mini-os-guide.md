# Mini Operating System - Education Aide
## Building an OS from First Principles

### Overview
This guide teaches you how operating systems work by building a minimal OS from scratch. You'll learn about bootloaders, memory management, process scheduling, and more - the foundations of Linux, Windows, and macOS.

**Warning:** This is one of the most challenging projects! Start small and be patient.

---

## Part 1: What is an Operating System?

### Question 1: OS Responsibilities
**Think about this:** What does an operating system do?

**Your Answer:** _[List responsibilities]_

<details>
<summary>OS Responsibilities</summary>

An operating system sits between hardware and applications:

```
┌─────────────────────────────────┐
│      Applications (Firefox, Word)      │
├─────────────────────────────────┤
│    System Libraries (libc, etc)         │
├─────────────────────────────────┤
│      Operating System Kernel            │
│  • Process management                   │
│  • Memory management                    │
│  • File system                          │
│  • Device drivers                       │
│  • Networking                           │
├─────────────────────────────────┤
│         Hardware (CPU, RAM, Disk)      │
└─────────────────────────────────┘
```

**Core responsibilities:**
1. **Process management** - Run multiple programs
2. **Memory management** - Allocate RAM safely
3. **File system** - Organize data on disk
4. **Device drivers** - Control hardware
5. **System calls** - API for applications

</details>

### Question 2: Boot Process
**Question:** What happens when you press the power button?

<details>
<summary>Boot Sequence</summary>

**Step by step:**

1. **Power on** → CPU starts executing BIOS/UEFI firmware
2. **BIOS** → Initializes hardware, runs POST (Power-On Self-Test)
3. **Bootloader** → BIOS loads first sector (512 bytes) from disk
4. **Boot sector** → Loads kernel into memory
5. **Kernel** → Initializes system, starts first process
6. **Init** → Starts system services and user interface

**Visual:**
```
Press power button
       ↓
   BIOS/UEFI (firmware in motherboard)
       ↓
   Read boot sector (first 512 bytes of disk)
       ↓
   Bootloader code runs
       ↓
   Load kernel from disk to RAM
       ↓
   Jump to kernel entry point
       ↓
   Kernel initializes hardware
       ↓
   Start first process (init/systemd)
       ↓
   System ready!
```

</details>

---

## Part 2: The Boot Sector

### Understanding Real Mode

**Question:** What is real mode?

<details>
<summary>CPU Modes</summary>

x86 CPUs have different modes:

**Real Mode (16-bit):**
- CPU boots into this mode
- Can only address 1MB of memory
- No memory protection
- Direct hardware access
- Like the original Intel 8086 (1978!)

**Protected Mode (32-bit):**
- Memory protection
- Virtual memory
- Multiple privilege levels
- Can address 4GB of memory
- Must switch from real mode

**Long Mode (64-bit):**
- Modern mode
- Can address huge amounts of memory
- Required for 64-bit OSes
</details>

### Creating a Boot Sector

**Question:** What's the minimal bootable program?

<details>
<summary>Hello World Boot Sector</summary>

```nasm
; boot.asm - Minimal boot sector
[bits 16]           ; Real mode is 16-bit
[org 0x7c00]        ; BIOS loads us at address 0x7c00

start:
    ; Clear screen
    mov ah, 0x00    ; Video function: set mode
    mov al, 0x03    ; Text mode 80x25
    int 0x10        ; Call BIOS video interrupt

    ; Print message
    mov si, message
    call print_string

    ; Hang forever
    jmp $

print_string:
    mov ah, 0x0e    ; Teletype output
.loop:
    lodsb           ; Load byte from SI into AL, increment SI
    cmp al, 0       ; Check for null terminator
    je .done
    int 0x10        ; Print character in AL
    jmp .loop
.done:
    ret

message: db 'Hello from OS!', 0

; Boot signature
times 510-($-$$) db 0    ; Pad with zeros
dw 0xaa55                 ; Boot signature (magic number)
```

**Understanding the code:**
- `[org 0x7c00]` - BIOS loads boot sector at this address
- `int 0x10` - Call BIOS video services
- `times 510-($-$$) db 0` - Pad to 510 bytes
- `dw 0xaa55` - Boot signature (BIOS checks for this!)

**Compile and test:**
```bash
nasm -f bin boot.asm -o boot.bin
qemu-system-x86_64 -drive format=raw,file=boot.bin
```

**You should see "Hello from OS!" on screen!**
</details>

### Reading from Disk

**Question:** How do you load more code from disk?

<details>
<summary>BIOS Disk Read</summary>

```nasm
; Read sectors from disk using BIOS interrupt 0x13
read_disk:
    pusha           ; Save all registers

    mov ah, 0x02    ; BIOS read function
    mov al, 15      ; Number of sectors to read
    mov ch, 0       ; Cylinder 0
    mov cl, 2       ; Sector 2 (sector 1 is boot sector)
    mov dh, 0       ; Head 0
    mov dl, 0x80    ; Drive (0x80 = first hard disk)

    mov bx, 0x8000  ; Destination: ES:BX = 0x0000:0x8000
    int 0x13        ; Call BIOS disk interrupt

    jc disk_error   ; Jump if carry flag set (error)

    popa            ; Restore registers
    ret

disk_error:
    mov si, disk_error_msg
    call print_string
    jmp $

disk_error_msg: db 'Disk read error!', 0
```

**This loads your kernel from disk into memory!**
</details>

---

## Part 3: Entering Protected Mode

### Why Protected Mode?

**Question:** Why switch from real mode?

<details>
<summary>Benefits of Protected Mode</summary>

**Real mode limitations:**
- Only 1MB addressable memory
- No memory protection (any program can access any memory)
- No privilege levels (all code runs with full access)

**Protected mode advantages:**
- Access to 4GB memory
- Memory protection (programs can't access each other's memory)
- Privilege rings (kernel vs user code)
- Hardware multitasking support

**The switch is one-way!** Can't easily return to real mode.
</details>

### The GDT (Global Descriptor Table)

**Concept:** Memory segmentation setup

<details>
<summary>GDT Implementation</summary>

```nasm
; Global Descriptor Table
gdt_start:

gdt_null:    ; Null descriptor (required)
    dd 0x0
    dd 0x0

gdt_code:    ; Code segment descriptor
    ; Base: 0x0, Limit: 0xfffff
    ; Flags: present, ring 0, code segment, executable, readable
    dw 0xffff    ; Limit (bits 0-15)
    dw 0x0       ; Base (bits 0-15)
    db 0x0       ; Base (bits 16-23)
    db 10011010b ; Access byte: present, ring 0, code
    db 11001111b ; Flags + Limit (bits 16-19)
    db 0x0       ; Base (bits 24-31)

gdt_data:    ; Data segment descriptor
    dw 0xffff
    dw 0x0
    db 0x0
    db 10010010b ; Access byte: present, ring 0, data
    db 11001111b
    db 0x0

gdt_end:

; GDT descriptor
gdt_descriptor:
    dw gdt_end - gdt_start - 1    ; Size
    dd gdt_start                   ; Address

; Segment selector constants
CODE_SEG equ gdt_code - gdt_start
DATA_SEG equ gdt_data - gdt_start
```

**Switching to protected mode:**
```nasm
switch_to_pm:
    cli                  ; Disable interrupts

    lgdt [gdt_descriptor]    ; Load GDT

    mov eax, cr0         ; Read control register 0
    or eax, 0x1          ; Set PE (Protection Enable) bit
    mov cr0, eax         ; Write back

    jmp CODE_SEG:init_pm ; Far jump to flush pipeline

[bits 32]                ; Now in 32-bit mode!
init_pm:
    mov ax, DATA_SEG     ; Set all segment registers
    mov ds, ax
    mov ss, ax
    mov es, ax
    mov fs, ax
    mov gs, ax

    mov ebp, 0x90000     ; Set up stack
    mov esp, ebp

    call kernel_main     ; Jump to C kernel!
```

**Congratulations!** You're now in protected mode!
</details>

---

## Part 4: The C Kernel

### Writing Kernel in C

**Question:** How do you write to screen from C?

<details>
<summary>VGA Text Mode</summary>

VGA text mode buffer is at memory address `0xb8000`:

```c
// kernel.c
#define VIDEO_MEMORY 0xb8000
#define WHITE_ON_BLACK 0x0f

void clear_screen() {
    char *video = (char *)VIDEO_MEMORY;
    for (int i = 0; i < 80 * 25 * 2; i++) {
        video[i] = 0;
    }
}

void print_char(char c, int col, int row, char attr) {
    char *video = (char *)VIDEO_MEMORY;

    if (attr == 0) {
        attr = WHITE_ON_BLACK;
    }

    int offset = 2 * (row * 80 + col);
    video[offset] = c;
    video[offset + 1] = attr;
}

void print_string(char *str) {
    int col = 0;
    int row = 0;

    for (int i = 0; str[i] != '\0'; i++) {
        if (str[i] == '\n') {
            row++;
            col = 0;
        } else {
            print_char(str[i], col, row, WHITE_ON_BLACK);
            col++;
            if (col >= 80) {
                col = 0;
                row++;
            }
        }
    }
}

void kernel_main() {
    clear_screen();
    print_string("Welcome to MyOS!\n");
    print_string("Kernel loaded successfully!");

    // Hang
    while (1) {
        __asm__("hlt");  // Halt CPU until interrupt
    }
}
```

**Build it:**
```bash
# Compile kernel
gcc -m32 -ffreestanding -c kernel.c -o kernel.o

# Link
ld -m elf_i386 -T link.ld kernel.o -o kernel.bin

# Combine bootloader and kernel
cat boot.bin kernel.bin > os.img

# Test
qemu-system-i386 os.img
```
</details>

---

## Part 5: Interrupts

### Understanding Interrupts

**Question:** How does hardware communicate with CPU?

<details>
<summary>Interrupt Concept</summary>

**Interrupts** are signals that temporarily stop the CPU to handle events:

**Hardware interrupts:**
- Timer (IRQ 0)
- Keyboard (IRQ 1)
- Disk (IRQ 14)

**Software interrupts:**
- System calls (int 0x80 on Linux)
- Exceptions (divide by zero, page fault)

**IDT (Interrupt Descriptor Table):**
Maps interrupt numbers to handler functions

```c
typedef struct {
    uint16_t base_low;
    uint16_t selector;
    uint8_t  always0;
    uint8_t  flags;
    uint16_t base_high;
} __attribute__((packed)) idt_entry_t;

idt_entry_t idt[256];  // 256 possible interrupts

void idt_set_gate(uint8_t num, uint32_t base, uint16_t selector, uint8_t flags) {
    idt[num].base_low = base & 0xFFFF;
    idt[num].base_high = (base >> 16) & 0xFFFF;
    idt[num].selector = selector;
    idt[num].always0 = 0;
    idt[num].flags = flags;
}

void idt_install() {
    idt_ptr_t idt_ptr;
    idt_ptr.limit = sizeof(idt_entry_t) * 256 - 1;
    idt_ptr.base = (uint32_t)&idt;

    // Set up interrupt handlers
    idt_set_gate(0, (uint32_t)isr0, 0x08, 0x8E);  // Divide by zero
    idt_set_gate(1, (uint32_t)isr1, 0x08, 0x8E);  // Debug
    // ... more handlers ...

    // Load IDT
    __asm__("lidt %0" : : "m"(idt_ptr));
}
```
</details>

### Keyboard Driver

<details>
<summary>Simple Keyboard Handler</summary>

```c
// Keyboard interrupt handler
void keyboard_handler() {
    uint8_t scancode = inb(0x60);  // Read from keyboard port

    if (scancode & 0x80) {
        // Key released
    } else {
        // Key pressed
        char key = scancode_to_char(scancode);
        print_char(key, cursor_col++, cursor_row, WHITE_ON_BLACK);
    }

    // Send EOI (End of Interrupt) to PIC
    outb(0x20, 0x20);
}

// Port I/O functions
uint8_t inb(uint16_t port) {
    uint8_t result;
    __asm__("in %%dx, %%al" : "=a"(result) : "d"(port));
    return result;
}

void outb(uint16_t port, uint8_t data) {
    __asm__("out %%al, %%dx" : : "a"(data), "d"(port));
}
```
</details>

---

## Part 6: Memory Management

### Physical Memory Allocator

<details>
<summary>Bitmap Allocator</summary>

```c
#define MEMORY_SIZE (16 * 1024 * 1024)  // 16 MB
#define BLOCK_SIZE 4096  // 4 KB blocks
#define BITMAP_SIZE (MEMORY_SIZE / BLOCK_SIZE / 8)

uint8_t memory_bitmap[BITMAP_SIZE];

void set_block_used(uint32_t block) {
    memory_bitmap[block / 8] |= (1 << (block % 8));
}

void set_block_free(uint32_t block) {
    memory_bitmap[block / 8] &= ~(1 << (block % 8));
}

int is_block_used(uint32_t block) {
    return memory_bitmap[block / 8] & (1 << (block % 8));
}

void *allocate_block() {
    for (uint32_t block = 0; block < MEMORY_SIZE / BLOCK_SIZE; block++) {
        if (!is_block_used(block)) {
            set_block_used(block);
            return (void *)(block * BLOCK_SIZE);
        }
    }
    return NULL;  // Out of memory
}

void free_block(void *ptr) {
    uint32_t block = (uint32_t)ptr / BLOCK_SIZE;
    set_block_free(block);
}
```
</details>

---

## Part 7: Process Scheduling

### Multitasking

<details>
<summary>Round-Robin Scheduler</summary>

```c
#define MAX_TASKS 16

typedef struct {
    uint32_t eax, ebx, ecx, edx;
    uint32_t esi, edi, ebp;
    uint32_t esp, eip;
    uint32_t eflags;
    int state;  // 0 = free, 1 = ready, 2 = running
} task_t;

task_t tasks[MAX_TASKS];
int current_task = 0;

void create_task(void (*entry)()) {
    for (int i = 0; i < MAX_TASKS; i++) {
        if (tasks[i].state == 0) {
            tasks[i].eip = (uint32_t)entry;
            tasks[i].esp = allocate_stack();
            tasks[i].state = 1;  // Ready
            return;
        }
    }
}

void schedule() {
    // Save current task state
    save_context(&tasks[current_task]);

    // Find next ready task
    do {
        current_task = (current_task + 1) % MAX_TASKS;
    } while (tasks[current_task].state != 1);

    tasks[current_task].state = 2;  // Running

    // Switch to next task
    restore_context(&tasks[current_task]);
}

// Called by timer interrupt
void timer_handler() {
    schedule();
    outb(0x20, 0x20);  // EOI
}
```
</details>

---

## Learning Path

### Phase 1: Boot (2 weeks)
- [ ] "Hello World" boot sector
- [ ] Read from disk
- [ ] Enter protected mode
- [ ] Jump to C kernel

### Phase 2: Output (1 week)
- [ ] VGA text mode driver
- [ ] Print functions
- [ ] Scrolling

### Phase 3: Input (2 weeks)
- [ ] Set up IDT
- [ ] Keyboard driver
- [ ] Simple shell

### Phase 4: Memory (3 weeks)
- [ ] Physical memory manager
- [ ] Paging (virtual memory)
- [ ] Heap allocator (malloc/free)

### Phase 5: Processes (4 weeks)
- [ ] Task structures
- [ ] Context switching
- [ ] Round-robin scheduler
- [ ] System calls

---

## Resources

### Essential Reading
- [OSDev Wiki](https://wiki.osdev.org/) - THE resource
- [os-tutorial](https://github.com/cfenollosa/os-tutorial) - Excellent step-by-step
- [Writing an OS in Rust](https://os.phil-opp.com/) - Modern approach
- [xv6](https://pdos.csail.mit.edu/6.828/2020/xv6.html) - MIT teaching OS

### Books
- "Operating Systems: Three Easy Pieces" (free online)
- "Modern Operating Systems" - Tanenbaum

---

## Key Takeaways

1. **Start simple** - Boot sector "Hello World" is an achievement!
2. **Use QEMU** - Don't test on real hardware
3. **Read OSDev wiki** - Your best friend
4. **Be patient** - This takes months, not weeks
5. **Join community** - r/osdev is helpful

---

**Warning:** OS development is extremely challenging but incredibly rewarding!

*"If you wish to make an apple pie from scratch, you must first invent the universe." - Carl Sagan*
