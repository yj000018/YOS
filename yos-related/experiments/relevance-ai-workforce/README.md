# Relevance AI Email Management Workforce

Automated deployment of Relevance AI workforce for email management.

## Features

- 🤖 3 specialized agents (Worker, COO, Strategist)
- 👥 7 teams configured (Sales, Support, HR, Finance, Operations, Executive, Admin)
- ⚡ High-performance parallel processing
- 📊 Real-time monitoring and metrics
- 🔄 Automated CI/CD deployment

## Quick Start

### Prerequisites
- Node.js 16+
- npm or yarn
- Relevance AI API key

### Installation

```bash
npm install -g @relevanceai/cli
```

### Configuration

Set environment variables:

```bash
export RELEVANCE_AI_API_KEY="your-api-key"
export RELEVANCE_AI_WORKSPACE_ID="d7b62b"
export RELEVANCE_AI_PROJECT_ID="c4d1f814c405-40fd-ab6c-0426439371df"
```

### Deploy

```bash
relevance-ai workforces create --config workforce_config.json
```

## CI/CD Pipeline

This repository includes automated GitHub Actions CI/CD pipeline.

### Setup

1. Push code to GitHub
2. Add `RELEVANCE_AI_API_KEY` as GitHub secret
3. Every push to `main` triggers automatic deployment

### Workflow

```
Push to GitHub
    ↓
GitHub Actions triggers
    ↓
Validate configuration
    ↓
Deploy to Relevance AI
    ↓
Verify deployment
    ↓
Notify on success/failure
```

## Agents

### Worker Agent
- Email processing and categorization
- Information extraction
- Quality validation

### COO Agent
- Workflow management
- Team assignment
- Priority assessment

### Strategist Agent
- Strategic analysis
- Business insights
- Recommendations

## Teams

- Sales Team (4-24 hours SLA)
- Support Team (2-8 hours SLA)
- HR Team (24-48 hours SLA)
- Finance Team (24-48 hours SLA)
- Operations Team (24-48 hours SLA)
- Executive Team (2-4 hours SLA)
- Admin Team (24-72 hours SLA)

## Monitoring

View real-time metrics:

```bash
relevance-ai monitor --workspace d7b62b
```

## Support

For issues or questions, contact Relevance AI support.

---

**Status**: Production Ready ✅
**Last Updated**: 2026-01-06
