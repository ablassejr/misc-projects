#!/usr/bin/env python3
"""Update the original Projects page: mark complete, add tasks to incomplete."""

import json
import os
import time
import urllib.request
import urllib.error

NOTION_TOKEN = os.environ.get("NOTION_API_KEY", "")
NOTION_VERSION = "2022-06-28"
# Original Projects page Tasks database
TASKS_DB_ID = "2ffea6ba-eea7-81bd-a335-c63b668c2d69"

# Page IDs from the original Projects page database (302ea6ba-... IDs)
PROJECT_IDS = {
    "Bash Practice": "302ea6ba-eea7-81f5-a0d9-daa7255f0916",
    "Binary Search Tree": "302ea6ba-eea7-8168-abe7-e2927f627820",
    "CS First Principles": "302ea6ba-eea7-8199-bcb2-f207c1956513",
    "Calendar Display": "302ea6ba-eea7-81fa-a38a-db12fc561585",
    "Campus Fitness Center": "302ea6ba-eea7-811a-a2e6-e772e6fd972c",
    "Challenging Projects": "302ea6ba-eea7-81a5-9053-da273eb5cb8b",
    "Company Database": "302ea6ba-eea7-8178-8504-f7cb2a1c7512",
    "Count Primes": "302ea6ba-eea7-8165-a239-e45cd78f786c",
    "Decimal To Binary": "302ea6ba-eea7-8127-83a5-c41a7b36a8cc",
    "Feed Handler": "302ea6ba-eea7-8186-b98c-feba2f90ea9c",
    "Forage Midas": "302ea6ba-eea7-8168-98a8-f0e9ccb86d7d",
    "Git Tools": "302ea6ba-eea7-815b-b2b9-f84607960d18",
    "Hash Track": "302ea6ba-eea7-8166-93b4-ef9513b6b23d",
    "Learn AI Agents": "302ea6ba-eea7-8164-8a7d-eb94362b75d2",
    "Nand2Tetris": "302ea6ba-eea7-813f-bc81-e52d7e8b49ff",
    "Prompt Engineering": "302ea6ba-eea7-81f7-8d80-d0cf6c4375de",
    "QuickSort": "302ea6ba-eea7-8105-8468-d0844412ea8c",
    "Reversal": "302ea6ba-eea7-81cb-b372-c4ec7744ce15",
    "Shortest Distance": "302ea6ba-eea7-817b-8185-d7dd5f4d09d2",
    "Simple Shell": "302ea6ba-eea7-8106-a1da-f752bef1e00b",
    "Sleeping Barber": "302ea6ba-eea7-81f3-802b-f5e31a6ddea5",
    "Text Generation": "302ea6ba-eea7-81cc-b098-e1128d37539e",
    "Education Aides": "302ea6ba-eea7-8108-9214-cd7411a87755",
    "IBM FizzBuzz": "302ea6ba-eea7-8136-b547-e055648a2eb3",
}

COMPLETE_PROJECTS = [
    "Bash Practice", "Binary Search Tree", "Campus Fitness Center",
    "Company Database", "Decimal To Binary", "Feed Handler", "Hash Track",
    "Prompt Engineering", "QuickSort", "Reversal", "Shortest Distance",
    "Education Aides", "IBM FizzBuzz",
]

INCOMPLETE_PROJECTS = {
    "CS First Principles": [
        "Implement 13 stub functions in 01-Binary-Basics (decimal_to_binary, binary_to_decimal, binary_add, twos_complement, etc.)",
        "Implement 30 stub functions in 02-Hash-Table (hashing functions, insert/lookup, collision handling)",
        "Implement 20 stub functions in 03-Sorting-Algorithms (bubble, insertion, selection, quick, merge, heap sort)",
        "Implement 45 stub functions in 04-Build-An-Interpreter (lexer, parser, AST evaluation, interpreter)",
        "Implement 21 stub functions in 05-TCP-Protocol-Simulator (IP packets, routing, TCP state machine)",
    ],
    "Calendar Display": [
        "Implement calendar rendering logic in calendar.cpp (currently empty)",
        "Implement utility functions in utils.h (currently empty)",
        "Implement header declarations in calendar.h (currently empty)",
    ],
    "Challenging Projects": [
        "Implement Console Emulator (CPU instructions, memory mapping, graphics, sound, input)",
        "Implement Mini Operating System (process mgmt, memory mgmt, file system, syscalls)",
        "Implement Space Invaders (sprites, game loop, collision detection, scoring, game states)",
        "Implement Spreadsheet (cell storage, formula evaluation, data manipulation, UI)",
        "Implement Text Editor (file I/O, text rendering, editing operations, syntax highlighting)",
        "Implement Tiny BASIC Compiler (lexer, parser, code generator, runtime)",
    ],
    "Count Primes": [
        "Fix uninitialized pointer in scanf input variable",
        "Fix thrd_start_t function pointer syntax in thrd_create call",
        "Implement proper thread creation and synchronization with parent process",
        "Verify correct return type for primefunc thread function",
    ],
    "Forage Midas": [
        "Implement Kafka consumer logic in TransactionListener with message processing",
        "Implement Balance and Transaction classes with full business logic",
        "Add UserRepository query methods and database operations",
        "Implement DatabaseConduit with full CRUD operations and transaction management",
        "Add REST API endpoints for user and transaction management",
        "Implement Kafka producer for sending transactions",
        "Add error handling, logging, and validation",
    ],
    "Git Tools": [
        "Implement actual git command execution (status, log, diff, add, commit)",
        "Implement gh (GitHub CLI) command execution (PR, issue, release operations)",
        "Add proper error handling and output formatting for command results",
    ],
    "Learn AI Agents": [
        "Implement Project 1: Complete BERT-based model beyond basic loading",
        "Implement Project 2: sentiment_agent.py (currently empty)",
        "Implement Project 2: summarization.py (only imports, no logic)",
        "Add data loading and preprocessing pipelines",
        "Add model training/fine-tuning code and evaluation metrics",
    ],
    "Nand2Tetris": [
        "Implement Project 6: Assembler (translate .asm to .hack binary)",
        "Implement Project 7: VM Translator Part 1 (stack arithmetic and memory access)",
        "Implement Project 8: VM Translator Part 2 (program flow and function calls)",
        "Implement Project 10: Compiler Part 1 (Jack tokenizer and parser)",
        "Implement Project 11: Compiler Part 2 (semantic analysis and code generation)",
        "Complete Project 13 implementation",
    ],
    "Simple Shell": [
        "Implement pipe operator (|) support (currently commented out)",
        "Fix I/O redirection flags (O_RDWR used for both input/output)",
        "Implement proper file descriptor handling for complex redirection",
        "Implement pipe chaining for multiple commands",
    ],
    "Sleeping Barber": [
        "Create IO utility class with static println(String) method",
        "Fix Main class: make main() public and add String[] args parameter",
        "Start customer generation thread (customerGen.start() never called)",
        "Test and verify synchronization logic after implementing IO class",
    ],
    "Text Generation": [
        "Implement text generation models (GPT-style or similar)",
        "Add training pipeline with dataset loading",
        "Implement sampling strategies (temperature, top-k, nucleus sampling)",
        "Add model evaluation metrics",
        "Create inference/generation API",
    ],
}


def notion_request(method, url, data=None):
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(
        url, data=body,
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
        method=method,
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return True, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        return False, f"HTTP {e.code}: {error_body}"


def main():
    print("=" * 60)
    print("STEP 1: Marking completed projects (Projects page)")
    print("=" * 60)
    for name in COMPLETE_PROJECTS:
        page_id = PROJECT_IDS[name]
        print(f"  [COMPLETED] {name}...", end=" ")
        ok, msg = notion_request("PATCH", f"https://api.notion.com/v1/pages/{page_id}", {
            "properties": {"Status": {"status": {"name": "Completed"}}}
        })
        print("OK" if ok else f"FAILED: {msg}")
        time.sleep(0.35)

    print()
    print("=" * 60)
    print("STEP 2: Adding tasks to incomplete projects (Projects page)")
    print("=" * 60)
    total_tasks = 0
    failed_tasks = 0
    for project_name, tasks in INCOMPLETE_PROJECTS.items():
        project_id = PROJECT_IDS[project_name]
        print(f"\n  [{project_name}] ({len(tasks)} tasks)")
        for task in tasks:
            print(f"    + {task[:60]}...", end=" ")
            data = {
                "parent": {"database_id": TASKS_DB_ID},
                "properties": {
                    "Name": {"title": [{"text": {"content": task}}]},
                    "Status": {"status": {"name": "Inbox"}},
                    "Project": {"relation": [{"id": project_id}]},
                },
            }
            ok, msg = notion_request("POST", "https://api.notion.com/v1/pages", data)
            if ok:
                total_tasks += 1
                print("OK")
            else:
                failed_tasks += 1
                print(f"FAILED: {msg}")
            time.sleep(0.35)

    print()
    print("=" * 60)
    print(f"Done! {len(COMPLETE_PROJECTS)} projects marked completed.")
    print(f"      {total_tasks} tasks added, {failed_tasks} failed.")
    print("=" * 60)


if __name__ == "__main__":
    main()
