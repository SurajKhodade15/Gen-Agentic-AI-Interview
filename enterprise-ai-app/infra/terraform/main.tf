terraform {
  required_version = ">= 1.6.0"
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.0" } }
}
provider "aws" { region = var.aws_region }

resource "aws_ecr_repository" "api" { name = "enterprise-ai-api" image_scanning_configuration { scan_on_push = true } }
resource "aws_cloudwatch_log_group" "api" { name = "/ecs/enterprise-ai" retention_in_days = 30 }
resource "aws_s3_bucket" "documents" { bucket_prefix = "enterprise-ai-documents-" }
resource "aws_s3_bucket_public_access_block" "documents" {
  bucket = aws_s3_bucket.documents.id
  block_public_acls = true; block_public_policy = true; ignore_public_acls = true; restrict_public_buckets = true
}
resource "aws_sqs_queue" "ingestion" { name = "enterprise-ai-ingestion" visibility_timeout_seconds = 300 }
resource "aws_secretsmanager_secret" "runtime" { name = "enterprise-ai/runtime" }

# Add VPC/private subnets, ALB, ECS service, CloudFront and Route53 in your organization module.
# Keeping them parameterized prevents accidentally provisioning public endpoints in a study account.
output "ecr_url" { value = aws_ecr_repository.api.repository_url }
output "documents_bucket" { value = aws_s3_bucket.documents.bucket }
