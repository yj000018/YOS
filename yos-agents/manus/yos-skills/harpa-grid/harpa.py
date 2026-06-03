#!/usr/bin/env python3
"""
HARPA Grid — Browser Automation API Client
yOS / Manus skill: harpa-grid
"""

import os
import sys
import json
import argparse
import requests

HARPA_API_URL = "https://api.harpa.ai/api/v1/grid"
HARPA_API_KEY = os.environ.get("HARPA_API_KEY", "")


def call_harpa(payload: dict) -> dict:
    """Send a POST request to the HARPA GRID API."""
    if not HARPA_API_KEY:
        print("ERROR: HARPA_API_KEY not set in environment.", file=sys.stderr)
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {HARPA_API_KEY}",
        "Content-Type": "application/json",
    }

    response = requests.post(HARPA_API_URL, headers=headers, json=payload, timeout=310)

    if response.status_code != 200:
        print(f"ERROR: HTTP {response.status_code} — {response.text}", file=sys.stderr)
        sys.exit(1)

    return response.json()


def action_scrape(args):
    payload = {
        "action": "scrape",
        "url": args.url,
        "timeout": args.timeout,
    }
    if args.grab:
        payload["grab"] = json.loads(args.grab)
    if args.node:
        payload["node"] = args.node
    if args.webhook:
        payload["resultsWebhook"] = args.webhook
    return call_harpa(payload)


def action_search(args):
    payload = {
        "action": "serp",
        "query": args.query,
        "timeout": args.timeout,
    }
    if args.node:
        payload["node"] = args.node
    return call_harpa(payload)


def action_prompt(args):
    payload = {
        "action": "prompt",
        "url": args.url,
        "prompt": args.prompt,
        "connection": args.connection,
        "timeout": args.timeout,
    }
    if args.node:
        payload["node"] = args.node
    if args.webhook:
        payload["resultsWebhook"] = args.webhook
    return call_harpa(payload)


def action_command(args):
    payload = {
        "action": "command",
        "url": args.url,
        "name": args.name,
        "connection": args.connection,
        "resultParam": "message",
        "timeout": args.timeout,
    }
    if args.inputs:
        payload["inputs"] = args.inputs
    if args.node:
        payload["node"] = args.node
    if args.webhook:
        payload["resultsWebhook"] = args.webhook
    return call_harpa(payload)


def main():
    parser = argparse.ArgumentParser(
        description="HARPA Grid API Client — yOS Browser Automation Layer"
    )
    parser.add_argument("--node", help="Target node ID (default: auto)", default=None)
    parser.add_argument("--timeout", type=int, default=30000, help="Timeout in ms (default: 30000)")
    parser.add_argument("--webhook", help="Async results webhook URL", default=None)
    parser.add_argument("--raw", action="store_true", help="Output raw JSON")

    subparsers = parser.add_subparsers(dest="action", required=True)

    # scrape
    p_scrape = subparsers.add_parser("scrape", help="Scrape a web page")
    p_scrape.add_argument("--url", required=True, help="Target URL")
    p_scrape.add_argument("--grab", help="JSON array of grab selectors", default=None)

    # search
    p_search = subparsers.add_parser("search", help="Search the web (SERP)")
    p_search.add_argument("--query", required=True, help="Search query")

    # prompt
    p_prompt = subparsers.add_parser("prompt", help="Run AI prompt on a page")
    p_prompt.add_argument("--url", required=True, help="Target URL")
    p_prompt.add_argument("--prompt", required=True, help="Prompt text (use {{page}} for page content)")
    p_prompt.add_argument("--connection", default="CHAT AUTO", help="LLM connection (default: CHAT AUTO)")

    # command
    p_command = subparsers.add_parser("command", help="Run a HARPA AI command")
    p_command.add_argument("--url", required=True, help="Target URL")
    p_command.add_argument("--name", required=True, help="Command name")
    p_command.add_argument("--inputs", help="Command inputs", default=None)
    p_command.add_argument("--connection", default="HARPA AI", help="LLM connection (default: HARPA AI)")

    args = parser.parse_args()

    dispatch = {
        "scrape": action_scrape,
        "search": action_search,
        "prompt": action_prompt,
        "command": action_command,
    }

    result = dispatch[args.action](args)

    if args.raw:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
