# Enterprise component checklist

| Area | Included in this project | AWS production service / control |
|---|---|---|
| Edge and DNS | Deployment design | Route 53, CloudFront, WAF, ACM |
| API compute | FastAPI Docker image, ECS task definition | ALB, ECS Fargate, ECR, autoscaling |
| Identity | Local JWT sample; OIDC replacement notes | Cognito or enterprise IdP + JWKS |
| Agent workflow | LangGraph retrieve → generate graph | LangGraph + Bedrock |
| Model reliability | Bedrock retry hook | Bedrock quotas, guardrails, fallback model |
| Knowledge store | Tenant-filtered Qdrant code | Qdrant private service or OpenSearch Serverless |
| Document ingestion | S3 processor and SQS worker | S3, EventBridge, SQS, malware scan, Textract |
| Session state | Redis conversation history | ElastiCache Redis, backups, TLS |
| API protection | Redis limiter, CORS, JWT | WAF, Shield, throttling, private subnets |
| Secrets | Secrets Manager client/task secret injection | KMS-encrypted Secrets Manager + IAM roles |
| Observability | JSON logs, Prometheus endpoint, LangSmith env | CloudWatch Logs/alarms/X-Ray + LangSmith |
| Delivery | GitHub Actions workflow, task definition | OIDC, ECR scan, ECS blue/green via CodeDeploy |
| Governance | Tenancy notes in code/docs | Audit CloudTrail, Macie, retention, PII redaction |

## Deliberately externalized controls

Some controls cannot responsibly be “turned on” with sample application code: network account boundaries, IAM organization policies, KMS key ownership, WAF managed rules, malware-scanning vendors, SIEM integration, model-risk approval, and disaster-recovery testing. The project identifies their placement so they can be discussed in an enterprise interview and implemented by the platform/security teams.
