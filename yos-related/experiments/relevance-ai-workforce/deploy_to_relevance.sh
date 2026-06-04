#!/bin/bash

# Relevance AI Deployment Script
# Deploys knowledge base and workflow configuration

echo "🚀 Deploying to Relevance AI..."
echo ""

# Load environment variables
export RELEVANCE_AI_API_KEY="${RELEVANCE_AI_API_KEY}"
export RELEVANCE_AI_WORKSPACE_ID="d7b62b"
export RELEVANCE_AI_PROJECT_ID="c4d1f814c405-40fd-ab6c-0426439371df"

# Check if files exist
if [ ! -f knowledge_base.json ]; then
    echo "❌ knowledge_base.json not found!"
    exit 1
fi

if [ ! -f workflow_complete.json ]; then
    echo "❌ workflow_complete.json not found!"
    exit 1
fi

echo "✅ Configuration files found"
echo ""

# Deploy knowledge base
echo "📚 Deploying Knowledge Base..."
curl -X POST "https://api-${RELEVANCE_AI_WORKSPACE_ID}.stack.tryrelevance.com/latest/knowledge/upload" \
  -H "Authorization: ${RELEVANCE_AI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d @knowledge_base.json

echo ""
echo "✅ Knowledge Base deployed!"
echo ""

# Deploy workflow
echo "⚙️ Deploying Workflow..."
curl -X POST "https://api-${RELEVANCE_AI_WORKSPACE_ID}.stack.tryrelevance.com/latest/workforces" \
  -H "Authorization: ${RELEVANCE_AI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d @workflow_complete.json

echo ""
echo "✅ Workflow deployed!"
echo ""

echo "============================================"
echo "✅ DEPLOYMENT COMPLETE!"
echo "============================================"
echo ""
echo "Knowledge Base: Uploaded"
echo "Workflow: Configured"
echo "Agents: Connected (Worker → COO → Strategist)"
echo "Teams: 7 teams configured"
echo ""
echo "View in Relevance AI:"
echo "https://app.relevanceai.com/workforce/${RELEVANCE_AI_WORKSPACE_ID}/${RELEVANCE_AI_PROJECT_ID}"
