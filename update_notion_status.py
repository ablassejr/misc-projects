#!/usr/bin/env python3
"""Update Notion: mark complete projects, add tasks to incomplete ones."""

import json
import os
import time
import urllib.request
import urllib.error

NOTION_TOKEN = os.environ.get("NOTION_API_KEY", "")
NOTION_VERSION = "2022-06-28"
# Cortex Tasks database
TASKS_DB_ID = "303ea6ba-eea7-81eb-874a-d3a7a4af55df"

# Map project names to their Cortex Notion page IDs
PROJECT_IDS = {
    "Bash Practice": "303ea6ba-eea7-81b0-a196-d38a9832faff",
    "Binary Search Tree": "303ea6ba-eea7-8136-930e-cf0b278f6c69",
    "CS First Principles": "303ea6ba-eea7-815a-a663-fe06178350d1",
    "Calendar Display": "303ea6ba-eea7-8183-9ac6-fefb08555b48",
    "Campus Fitness Center": "303ea6ba-eea7-814c-bab9-c82f96c77d79",
    "Challenging Projects": "303ea6ba-eea7-81c6-83d1-d718d746bbf2",
    "Company Database": "303ea6ba-eea7-8139-9f66-c854b473e75b",
    "Count Primes": "303ea6ba-eea7-817b-a6d4-e3c60080f43a",
    "Decimal To Binary": "303ea6ba-eea7-8123-bb69-ef649011ca4e",
    "Feed Handler": "303ea6ba-eea7-81d2-96dc-f18437c24f2b",
    "Forage Midas": "303ea6ba-eea7-81c0-9e98-d9b371325006",
    "Git Tools": "303ea6ba-eea7-81b9-a837-fc22733766be",
    "Hash Track": "303ea6ba-eea7-81b8-8e87-da1ac864bc8b",
    "Learn AI Agents": "303ea6ba-eea7-8192-975a-c0dc7c774b6f",
    "Nand2Tetris": "303ea6ba-eea7-81f9-bfce-e493e184a4d6",
    "Prompt Engineering": "303ea6ba-eea7-812e-8b50-fd190682c933",
    "QuickSort": "303ea6ba-eea7-8143-9588-d2a683acfee9",
    "Reversal": "303ea6ba-eea7-81c2-90a9-df88ba2e365c",
    "Shortest Distance": "303ea6ba-eea7-81cc-8a6c-d5dd3f0419b4",
    "Simple Shell": "303ea6ba-eea7-8149-b680-dfb42a70fec1",
    "Sleeping Barber": "303ea6ba-eea7-814b-be41-ed56ab8ff726",
    "Text Generation": "303ea6ba-eea7-81e6-9ce1-c8981cb1843c",
    "Education Aides": "303ea6ba-eea7-81aa-97d5-e04b01131d80",
    "IBM FizzBuzz": "303ea6ba-eea7-8175-8592-f2d80f218de0",
}

COMPLETE_PROJECTS = [
    "Bash Practice",
    "Binary Search Tree",
    "Campus Fitness Center",
    "Company Database",
    "Decimal To Binary",
    "Feed Handler",
    "Hash Track",
    "Prompt Engineering",
    "QuickSort",
    "Reversal",
    "Shortest Distance",
    "Education Aides",
    "IBM FizzBuzz",
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
    """Make a Notion API request."""
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(
        url,
        data=body,
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


def update_status(project_name, status):
    """Update a project's status."""
    page_id = PROJECT_IDS[project_name]
    url = f"https://api.notion.com/v1/pages/{page_id}"
    data = {
        "properties": {
            "Status": {"status": {"name": status}}
        }
    }
    return notion_request("PATCH", url, data)


def create_task(task_name, project_id):
    """Create a task in the Tasks database linked to a project."""
    data = {
        "parent": {"database_id": TASKS_DB_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": task_name}}]},
            "Status": {"status": {"name": "Inbox"}},
            "Project": {"relation": [{"id": project_id}]},
        },
    }
    return notion_request("POST", "https://api.notion.com/v1/pages", data)


def main():
    print("=" * 60)
    print("STEP 1: Marking completed projects")
    print("=" * 60)
    for name in COMPLETE_PROJECTS:
        print(f"  [COMPLETED] {name}...", end=" ")
        ok, msg = update_status(name, "Completed")
        print("OK" if ok else f"FAILED: {msg}")
        time.sleep(0.35)

    print()
    print("=" * 60)
    print("STEP 2: Adding tasks to incomplete projects")
    print("=" * 60)
    total_tasks = 0
    failed_tasks = 0
    for project_name, tasks in INCOMPLETE_PROJECTS.items():
        project_id = PROJECT_IDS[project_name]
        print(f"\n  [{project_name}] ({len(tasks)} tasks)")
        for task in tasks:
            print(f"    + {task[:60]}...", end=" ")
            ok, msg = create_task(task, project_id)
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
