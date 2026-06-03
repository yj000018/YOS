#!/usr/bin/env python3
"""
Sanity CMS Seed Script Template
Usage: python3 seed-sanity.py

Requires env vars:
  SANITY_PROJECT_ID
  SANITY_DATASET (default: production)
  SANITY_TOKEN (editor token with write access)
"""

import os
import json
import requests

PROJECT_ID = os.environ.get("SANITY_PROJECT_ID", "")
DATASET = os.environ.get("SANITY_DATASET", "production")
TOKEN = os.environ.get("SANITY_TOKEN", "")

if not PROJECT_ID or not TOKEN:
    print("ERROR: Set SANITY_PROJECT_ID and SANITY_TOKEN env vars")
    exit(1)

API_URL = f"https://{PROJECT_ID}.api.sanity.io/v2021-06-07/data/mutate/{DATASET}"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}",
}


def create_or_replace(doc_id: str, doc_type: str, data: dict):
    """Create or replace a document in Sanity."""
    doc = {"_id": doc_id, "_type": doc_type, **data}
    mutations = [{"createOrReplace": doc}]
    resp = requests.post(API_URL, headers=HEADERS, json={"mutations": mutations})
    if resp.status_code == 200:
        print(f"  OK: {doc_type}/{doc_id}")
    else:
        print(f"  ERROR: {doc_type}/{doc_id} — {resp.status_code} {resp.text[:200]}")
    return resp


# ============================================================
# CUSTOMIZE BELOW — Add your documents
# ============================================================

def seed():
    print("Seeding Sanity...")

    # Example: Homepage singleton
    create_or_replace("homepage", "homepage", {
        "hero": {
            "headline": "Your headline here",
            "subheadline": "Your subheadline here",
            "ctaText": "Get Started",
            "ctaLink": "/signup",
        },
        # Add more sections...
    })

    # Example: Site settings singleton
    create_or_replace("siteSettings", "siteSettings", {
        "siteName": "Your App",
        "tagline": "Your tagline",
    })

    # Example: Multiple documents (testimonials, blog posts, etc.)
    testimonials = [
        {"name": "Jane Doe", "role": "CEO", "company": "Acme", "quote": "Great product!"},
        {"name": "John Smith", "role": "CTO", "company": "TechCo", "quote": "Saved us hours."},
    ]
    for i, t in enumerate(testimonials):
        create_or_replace(f"testimonial-{i+1}", "testimonial", t)

    print("Done!")


if __name__ == "__main__":
    seed()
