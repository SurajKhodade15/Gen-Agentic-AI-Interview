# Enterprise AI API (FastAPI + LangGraph + AWS)

A production-oriented RAG reference application that keeps the code approachable. It provides JWT-protected chat, a LangGraph retrieval/generation workflow, Qdrant vector search, Amazon Bedrock generation, structured logging, Prometheus metrics, LangSmith tracing hooks, and ECS-ready deployment assets.

## Architecture

```text
User → Route 53 → CloudFront (+ WAF) → ALB → ECS Fargate (FastAPI container)
                                              ├─ JWT / Cognito or Entra ID
                                              ├─ LangGraph: retrieve → generate
                                              ├─ Qdrant (vectors; private endpoint)
                                              ├─ Bedrock Runtime (LLM / embeddings)
                                              ├─ S3 (source documents)
                                              ├─ Secrets Manager (runtime secrets)
                                              ├─ CloudWatch Logs/Metrics/Alarms
                                              └─ LangSmith (traces; optional)

GitHub Actions or CodePipeline → ECR → ECS rolling deployment
```

### Azure-to-AWS learning map

| Azure | AWS counterpart used here |
|---|---|
| Azure Front Door | Route 53 + CloudFront + WAF |
| Application Gateway | Application Load Balancer |
| Container Apps | ECS Fargate + ECR |
| Azure AI Search | Qdrant / Amazon OpenSearch vector engine |
| Azure OpenAI | Amazon Bedrock |
| Key Vault | Secrets Manager |
| Application Insights | CloudWatch + LangSmith |

## Local startup

1. Copy `.env.example` to `.env`; set `JWT_SECRET`. AWS credentials and a Bedrock-enabled model are required only for `/v1/chat`.
2. Start: `docker compose up --build -d`.
3. Seed documents: `docker compose exec api python scripts/seed_qdrant.py`.
4. Obtain demo token: `POST /auth/token` with `{"username":"demo","password":"demo-password"}`.
5. Call `POST /v1/chat` with `Authorization: Bearer <token>` and `{"question":"When are expenses due?"}`.

OpenAPI documentation is at `http://localhost:8000/docs`; health is `/healthz`; Prometheus scrape endpoint is `/metrics`.

## Production deployment flow

1. Create an ECR repository, ECS cluster/service, ALB target group, Route 53 alias and CloudFront distribution. Restrict the ALB security group to CloudFront origin-facing traffic.
2. Create a Secrets Manager secret for runtime configuration; permit the ECS task role to read it and to invoke the selected Bedrock model. Give least-privilege S3 access to the document bucket.
3. Update [infra/ecs/task-definition.json](infra/ecs/task-definition.json) placeholders. Use a private Qdrant deployment or replace its implementation with Amazon OpenSearch Serverless.
4. Configure GitHub OIDC role `AWS_DEPLOY_ROLE_ARN`, then push to `main`. The workflow builds, pushes to ECR, and requests an ECS rolling deployment. The equivalent CodePipeline stages are Source → Build (CodeBuild) → Deploy (ECS).
5. Add CloudWatch alarms for ALB 5xx, ECS CPU/memory, API latency, and Bedrock throttling. Enable LangSmith through its standard environment variables.

## Security notes

The demo username/password endpoint is deliberately local-only. In production, replace it with Cognito or enterprise OIDC validation, validate issuer/audience/JWKS, use Secrets Manager rather than `.env`, and never expose Qdrant publicly. Rate limiting, WAF rules, document ingestion malware scanning, PII redaction, tenant filters, and prompt-injection evaluation are recommended before real use.

## Project layout

```text
app/api/routes       HTTP boundary
app/core             settings, security, structured logs
app/services         Bedrock, Qdrant, LangGraph, Secrets Manager
infra/ecs            deployable ECS task definition
.github/workflows    GitHub Actions ECR/ECS pipeline
scripts              local knowledge base seeding
```
