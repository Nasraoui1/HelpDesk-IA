HelpDesk IA - Northwind Industries

Automated IT HelpDesk back-office built with n8n, Baserow, and AI (Google Gemini Free Tier), designed for Northwind Industries (220 employees, 2 sites).

🚀 Quick Start (One-Command Deployment)

Make sure you have Docker and Docker Compose installed on your machine.

Clone the repository and navigate into the folder:

git clone <repository-url>
cd helpdesk-ia


Configure environment variables:
Copy the example environment file and fill in your API keys (e.g., Google Gemini API key):

cp .env.example .env


Start the complete stack:

docker compose up -d


Access the services:

n8n (Workflows): http://localhost:5678

Baserow (Database): http://localhost:8000

🛠️ Tech Stack

Workflow Automation: n8n (self-hosted via Docker)

Database & Back-office: Baserow (self-hosted official Docker image)

Artificial Intelligence: Google Gemini API (Free tier, structured outputs via JSON Schema)

Version Control: Git

✨ Features & Workflows

W1 - Request Form & AI Triage: Single entry point via native n8n Form Trigger. Normalizes requests, checks for duplicates (idempotency), performs AI-powered structured triage (category, priority P1-P4, confidence score, summary, required skills), handles automatic fallback/manual review, routes to available qualified technicians with load balancing, and sends automated notifications (with instant P1 alerts).

W2 - Assisted Reply & Human Validation: Searches the Knowledge Base, drafts AI-generated responses (strictly grounded in documentation), saves drafts as draft in Baserow, pauses for human validation, and sends responses only after approval while logging actions to the Audit Trail.

W3 & W4 - SLA Monitoring & Weekly Reports: Hourly schedule workflow for tracking SLA breaches and notifying technicians; Friday schedule workflow for weekly ticket aggregation, natural language report generation, and email dispatch.

W5 - Knowledge Base Assistant (Bonus): Interactive chat/webhook querying the Knowledge Base with source citations.

📦 Deliverables

Git Repository: Clean commit history, automated setup scripts, and .env.example.

workflows/*.json: Versioned n8n workflow exports (one file per workflow).

docs/ARCHITECTURE.md: System architecture schema and technical decision justification.

docs/PROMPTS.md: Versioned and documented AI prompts, model selection, and parameters.

seed/: Replayable Baserow initialization dataset and seed scripts.