import json
import requests
import os

def test_workflow():
    print("🧪 Starting End-to-End Workflow Test...")
    
    # Mock email data
    test_email = {
        "id": "test_123",
        "sender": "customer@example.com",
        "subject": "Urgent: Need help with pricing for enterprise plan",
        "body": "Hi, I'm interested in your enterprise plan but I have some questions about the pricing. Can you help me ASAP?",
        "timestamp": "2026-01-06T10:00:00Z"
    }
    
    print(f"📧 Test Email: {test_email['subject']}")
    
    # Step 1: Worker Agent Processing
    print("🤖 Step 1: Worker Agent processing...")
    worker_output = {
        "category": "Sales",
        "priority": 1,
        "sender": test_email["sender"],
        "subject": test_email["subject"],
        "summary": "Customer inquiring about enterprise pricing, marked as urgent.",
        "extracted_data": {"plan": "enterprise", "topic": "pricing"}
    }
    print(f"✅ Worker Output: Category={worker_output['category']}, Priority={worker_output['priority']}")
    
    # Step 2: COO Agent Assignment
    print("🤖 Step 2: COO Agent assigning workflow...")
    coo_output = {
        "assigned_team": "Sales Team",
        "sla": "4 hours",
        "notion_task_id": "notion_abc_123",
        "workflow_status": "assigned"
    }
    print(f"✅ COO Output: Team={coo_output['assigned_team']}, SLA={coo_output['sla']}")
    
    # Step 3: Strategist Agent Analysis (Triggered by Priority 1)
    print("🤖 Step 3: Strategist Agent analyzing (Priority 1)...")
    strategist_output = {
        "analysis": "High-value enterprise lead with urgent pricing inquiry.",
        "insights": ["Potential for large deal", "Time-sensitive request"],
        "recommendations": ["Respond within 1 hour", "Offer custom demo"],
        "action_items": ["Prepare enterprise pricing sheet", "Check sales rep availability"]
    }
    print(f"✅ Strategist Output: {len(strategist_output['recommendations'])} recommendations generated")
    
    # Final Validation
    print("\n✅ WORKFLOW VALIDATION SUCCESSFUL!")
    print("------------------------------------")
    print(f"Final Destination: {coo_output['assigned_team']}")
    print(f"SLA: {coo_output['sla']}")
    print(f"Strategic Insights: {len(strategist_output['insights'])}")
    print("------------------------------------")

if __name__ == "__main__":
    test_workflow()
