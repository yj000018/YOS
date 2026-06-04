#!/usr/bin/env python3
"""Seed Sanity CMS with initial content for Pulse demo app."""

import requests
import json

PROJECT_ID = "5uj6i155"
DATASET = "production"
TOKEN = "skKcKIp8ECTLIOqtVyzauVTIpTsAXXFMI3F1Ki2l6s5tZunIex4nXtTePXMikAyvXNVCnKLIcM2H9RRFR41Ax86gKgVtb8tL8jw12DGgiCE3U1AHrQvRg83TQYjHltNJoMF5lWyzR05XXyYq6SQ2822Va2QrrI47Y1ErQY3KLCbFzhPGgkkX"

API_URL = f"https://{PROJECT_ID}.api.sanity.io/v2021-06-07/data/mutate/{DATASET}"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

mutations = [
    # Site Settings
    {
        "createOrReplace": {
            "_id": "siteSettings",
            "_type": "siteSettings",
            "siteName": "Pulse",
            "tagline": "The future of team productivity",
            "primaryColor": "#6366f1",
            "secondaryColor": "#8b5cf6",
            "navigation": [
                {"label": "Features", "href": "#features"},
                {"label": "Testimonials", "href": "#testimonials"},
                {"label": "Pricing", "href": "#pricing"}
            ],
            "footer": {
                "copyright": "2026 Pulse. All rights reserved.",
                "links": [
                    {"label": "Privacy", "href": "/privacy"},
                    {"label": "Terms", "href": "/terms"},
                    {"label": "Contact", "href": "mailto:hello@pulse.app"}
                ]
            }
        }
    },
    # Homepage
    {
        "createOrReplace": {
            "_id": "homepage",
            "_type": "homepage",
            "hero": {
                "headline": "Work smarter, not harder",
                "subheadline": "Pulse brings your team's tasks, communication, and goals into one intelligent workspace. Less noise, more flow.",
                "ctaText": "Join the Waitlist",
                "ctaLink": "/signup",
                "secondaryCtaText": "Learn More",
                "secondaryCtaLink": "#features"
            },
            "valueProposition": {
                "title": "Why teams choose Pulse",
                "subtitle": "Built for modern teams who value clarity and momentum",
                "items": [
                    {
                        "_key": "vp1",
                        "icon": "zap",
                        "title": "Lightning Fast",
                        "description": "Real-time sync across all devices. No lag, no friction, just pure productivity."
                    },
                    {
                        "_key": "vp2",
                        "icon": "shield",
                        "title": "Enterprise Security",
                        "description": "SOC 2 compliant with end-to-end encryption. Your data stays yours."
                    },
                    {
                        "_key": "vp3",
                        "icon": "brain",
                        "title": "AI-Powered Insights",
                        "description": "Smart suggestions that help your team focus on what matters most."
                    }
                ]
            },
            "features": {
                "title": "Everything you need",
                "subtitle": "A complete toolkit for high-performing teams",
                "items": [
                    {
                        "_key": "f1",
                        "title": "Smart Task Management",
                        "description": "Organize, prioritize, and track tasks with AI-assisted workflows that adapt to your team's rhythm.",
                        "icon": "layout"
                    },
                    {
                        "_key": "f2",
                        "title": "Unified Communication",
                        "description": "Threads, channels, and direct messages — all contextually linked to your work.",
                        "icon": "message-circle"
                    },
                    {
                        "_key": "f3",
                        "title": "Goal Tracking",
                        "description": "Set OKRs, track progress, and celebrate wins. Keep everyone aligned on what matters.",
                        "icon": "target"
                    },
                    {
                        "_key": "f4",
                        "title": "Analytics Dashboard",
                        "description": "Real-time insights into team performance, bottlenecks, and opportunities.",
                        "icon": "bar-chart"
                    }
                ]
            },
            "finalCta": {
                "headline": "Ready to transform your workflow?",
                "subheadline": "Join thousands of teams already using Pulse to work better together.",
                "ctaText": "Get Early Access",
                "ctaLink": "/signup"
            }
        }
    },
    # Signup Page
    {
        "createOrReplace": {
            "_id": "signupPage",
            "_type": "signupPage",
            "headline": "Get early access to Pulse",
            "subheadline": "Be among the first to experience the future of team productivity. We'll notify you as soon as we launch.",
            "formFields": {
                "firstNameLabel": "First Name",
                "firstNamePlaceholder": "Enter your first name",
                "emailLabel": "Email",
                "emailPlaceholder": "you@company.com",
                "submitText": "Join the Waitlist",
                "submittingText": "Joining..."
            },
            "successMessage": {
                "headline": "You're on the list!",
                "body": "Thanks for joining the Pulse waitlist. We'll be in touch soon with updates and early access details."
            },
            "socialProof": "Join 2,400+ professionals already on the waitlist"
        }
    },
    # Testimonials
    {
        "createOrReplace": {
            "_id": "testimonial-1",
            "_type": "testimonial",
            "name": "Sarah Chen",
            "role": "VP of Engineering",
            "company": "TechFlow",
            "quote": "Pulse transformed how our engineering team collaborates. We shipped 40% more features last quarter.",
            "order": 1
        }
    },
    {
        "createOrReplace": {
            "_id": "testimonial-2",
            "_type": "testimonial",
            "name": "Marcus Rivera",
            "role": "Head of Product",
            "company": "ScaleUp",
            "quote": "The AI insights alone saved us hours of manual reporting. It's like having an extra team member.",
            "order": 2
        }
    },
    {
        "createOrReplace": {
            "_id": "testimonial-3",
            "_type": "testimonial",
            "name": "Emma Larsson",
            "role": "CEO",
            "company": "NordTech",
            "quote": "Finally, a tool that brings everything together without the complexity. Our team adopted it in days.",
            "order": 3
        }
    }
]

print("Seeding Sanity CMS for Pulse...")
response = requests.post(
    API_URL,
    headers=headers,
    json={"mutations": mutations}
)

if response.status_code == 200:
    result = response.json()
    print(f"Success! Created/updated {len(result.get('results', []))} documents.")
    for r in result.get('results', []):
        print(f"  - {r.get('id', 'unknown')}: {r.get('operation', 'unknown')}")
else:
    print(f"Error {response.status_code}: {response.text}")
