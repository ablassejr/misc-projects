#!/usr/bin/env python3
"""Script to add all misc-projects to the Cortex Projects database in Notion."""

import json
import os
import time
import urllib.request
import urllib.error

NOTION_TOKEN = os.environ.get("NOTION_API_KEY", "")
# Cortex Projects database (actual source database)
DATABASE_ID = "303ea6ba-eea7-81ed-9aee-eb42901b05c2"
NOTION_VERSION = "2022-06-28"

PROJECTS = [
    {
        "name": "Bash Practice",
        "language": "Bash",
        "description": "Collection of bash scripting exercises focusing on shell operations and file handling.",
        "status": "In progress",
    },
    {
        "name": "Binary Search Tree",
        "language": "C++",
        "description": "Implementation of binary search tree and B-tree data structures with header-based templates.",
        "status": "In progress",
    },
    {
        "name": "CS First Principles",
        "language": "Python",
        "description": "Hands-on curriculum covering CS fundamentals: binary representation, hash tables, sorting algorithms, interpreters, and TCP/IP simulation.",
        "status": "In progress",
    },
    {
        "name": "Calendar Display",
        "language": "C++",
        "description": "Calendar application for displaying and managing calendar operations.",
        "status": "In progress",
    },
    {
        "name": "Campus Fitness Center",
        "language": "SQL",
        "description": "Database design for a fitness center management system with membership plans and member tracking.",
        "status": "In progress",
    },
    {
        "name": "Challenging Projects",
        "language": "Python, C++, Java",
        "description": "Collection of 6 ambitious projects: Console Emulator, Space Invaders, Text Editor, Spreadsheet, BASIC Compiler, and Mini OS.",
        "status": "In progress",
    },
    {
        "name": "Company Database",
        "language": "SQL",
        "description": "SQL database schema for a company management system with departments and employees.",
        "status": "In progress",
    },
    {
        "name": "Count Primes",
        "language": "C",
        "description": "Concurrent prime number calculation using POSIX threads and process forking to explore multi-threading patterns.",
        "status": "In progress",
    },
    {
        "name": "Decimal To Binary",
        "language": "C++",
        "description": "Command-line utility to convert decimal numbers to binary using a stack data structure.",
        "status": "In progress",
    },
    {
        "name": "Feed Handler",
        "language": "Python",
        "description": "Message processing system for handling order book feeds with buy/sell events and state management.",
        "status": "In progress",
    },
    {
        "name": "Forage Midas",
        "language": "Java",
        "description": "JPMC Advanced Software Engineering project with Spring Boot, Apache Kafka, microservices, and financial transaction processing.",
        "status": "In progress",
    },
    {
        "name": "Git Tools",
        "language": "C",
        "description": "CLI tool wrapper for git and GitHub operations with command routing and argument parsing.",
        "status": "In progress",
    },
    {
        "name": "Hash Track",
        "language": "C++",
        "description": "Hash table implementation from scratch with quadratic probing, templates, and collision resolution.",
        "status": "In progress",
    },
    {
        "name": "Learn AI Agents",
        "language": "Python",
        "description": "AI agents and NLP projects covering transformer models (BERT), caching, sentiment analysis, and text summarization.",
        "status": "In progress",
    },
    {
        "name": "Nand2Tetris",
        "language": "Java, Python",
        "description": "Complete computer system course: hardware design (gates to CPU), assembler, VM, compiler, and OS from first principles.",
        "status": "In progress",
    },
    {
        "name": "Prompt Engineering",
        "language": "Python",
        "description": "Anthropic's interactive tutorial on crafting effective prompts for Claude with 9 chapters from basic to advanced techniques.",
        "status": "In progress",
    },
    {
        "name": "QuickSort",
        "language": "C++",
        "description": "Implementation of QuickSort algorithm with template-based generic array list data structure.",
        "status": "In progress",
    },
    {
        "name": "Reversal",
        "language": "C++",
        "description": "File I/O utility that reads text files and outputs reversed content, demonstrating C++ stream operations.",
        "status": "In progress",
    },
    {
        "name": "Shortest Distance",
        "language": "C++",
        "description": "Graph algorithms implementation for finding shortest paths in weighted graphs (Dijkstra's algorithm).",
        "status": "In progress",
    },
    {
        "name": "Simple Shell",
        "language": "C",
        "description": "Shell implementation demonstrating fork-exec pattern, process management, I/O redirection, and command parsing.",
        "status": "In progress",
    },
    {
        "name": "Sleeping Barber",
        "language": "C, Java",
        "description": "Classic synchronization problem solved using POSIX threads/semaphores and Java synchronization for concurrent access.",
        "status": "In progress",
    },
    {
        "name": "Text Generation",
        "language": "Python",
        "description": "NLP project exploring text generation techniques, language models, and transformer-based approaches.",
        "status": "In progress",
    },
    {
        "name": "Education Aides",
        "language": "Markdown",
        "description": "Comprehensive collection of interactive learning guides for all major projects covering systems programming, data structures, and AI/ML.",
        "status": "In progress",
    },
    {
        "name": "IBM FizzBuzz",
        "language": "C++",
        "description": "FizzBuzz algorithm implementation in C++, classic coding challenge.",
        "status": "In progress",
    },
]


def create_page(project):
    """Create a page in the Cortex Projects database."""
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": project["name"]
                        }
                    }
                ]
            },
            "Status": {
                "status": {
                    "name": project["status"]
                }
            },
            "Priority": {
                "select": {
                    "name": "Medium"
                }
            },
        },
        "children": [
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": project["description"]
                            }
                        }
                    ],
                    "icon": {"emoji": "\ud83d\udcdd"},
                    "color": "blue_background"
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": "Language: "},
                            "annotations": {"bold": True}
                        },
                        {
                            "type": "text",
                            "text": {"content": project["language"]}
                        }
                    ]
                }
            },
        ]
    }

    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        "https://api.notion.com/v1/pages",
        data=body,
        headers={
            "Authorization": f"Bearer {NOTION_TOKEN}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return True, result.get("url", "")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        return False, f"HTTP {e.code}: {error_body}"


def main():
    success_count = 0
    fail_count = 0

    for i, project in enumerate(PROJECTS, 1):
        print(f"[{i}/{len(PROJECTS)}] Adding '{project['name']}'...", end=" ")
        ok, msg = create_page(project)
        if ok:
            success_count += 1
            print(f"OK -> {msg}")
        else:
            fail_count += 1
            print(f"FAILED -> {msg}")
        time.sleep(0.35)

    print(f"\nDone! {success_count} added, {fail_count} failed.")


if __name__ == "__main__":
    main()
