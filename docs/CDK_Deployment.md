# Deploying FastAPI OpenAI Chatbot with AWS ECS Fargate & CDK

This guide explains how to deploy your FastAPI-based OpenAI chatbot as a scalable containerized application using AWS ECS Fargate and AWS CDK (Cloud Development Kit).

---

## Table of Contents
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Preparing the FastAPI App for ECS](#preparing-the-fastapi-app-for-ecs)
- [Setting Up the Container Directory](#setting-up-the-container-directory)
- [Writing the CDK Stack](#writing-the-cdk-stack)

---

## Prerequisites
- AWS CLI configured (`aws configure`)
- AWS CDK installed (`npm install -g aws-cdk`)
- Docker installed and running
- Python 3.8+
- Node.js (for CDK)
- Your FastAPI app ready

---

## Project Structure

Recommended structure:

```
/your-project-root
  /cdk
    /docker
      app.py
      models/
      services/
      requirements.txt
      Dockerfile
    cdk_stack.py
    app.py (CDK entrypoint)
```

---

## Preparing the FastAPI App for ECS

1. **Update your FastAPI app** to be container-ready:
   ```python
   # app.py - No changes needed for ECS deployment
   # Your existing FastAPI app works as-is with containers
   from fastapi import FastAPI, HTTPException
   from fastapi.middleware.cors import CORSMiddleware
   from services.ai.openai_service import OpenAIService
   # ... rest of your existing imports and code ...

   app = FastAPI(
       title="Summer Smiles Chatbot API",
       description="FastAPI chatbot with ECS Fargate deployment",
       version="1.0.0"
   )

   # ... rest of your existing FastAPI code ...

   # Add this for container health checks
   @app.get("/health")
   async def health_check():
       """Health check endpoint for ECS"""
       return {"status": "healthy", "service": "Summer Smiles Chatbot API"}

   if __name__ == "__main__":
       import uvicorn
       uvicorn.run(app, host="0.0.0.0", port=8000)
   ```

---

## Setting Up the Container Directory

1. **Create `/cdk/docker/requirements.txt`**:
   ```
   fastapi==0.104.1
   uvicorn[standard]==0.24.0
   openai==1.3.0
   python-dotenv==1.0.0
   pydantic==2.5.0
   # Add any other dependencies your app needs
   ```

2. **Create `/cdk/docker/Dockerfile`**:
   ```dockerfile
   # Use Python 3.11 slim image for smaller size
   FROM python:3.11-slim

   # Set working directory
   WORKDIR /app

   # Install system dependencies if needed
   RUN apt-get update && apt-get install -y \
       && rm -rf /var/lib/apt/lists/*

   # Copy requirements first for better Docker layer caching
   COPY requirements.txt .

   # Install Python dependencies
   RUN pip install --no-cache-dir -r requirements.txt

   # Copy application code
   COPY . .

   # Create non-root user for security
   RUN useradd --create-home --shell /bin/bash app \
       && chown -R app:app /app
   USER app

   # Expose port
   EXPOSE 8000

   # Health check
   HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
       CMD curl -f http://localhost:8000/health || exit 1

   # Run the application
   CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

3. **Copy your FastAPI application files** into `/cdk/docker/`:
   - `app.py`
   - `models/` directory
   - `services/` directory  
   - Any other application modules

---

## Writing the CDK Stack

1. **Install CDK libraries**:
   ```sh
   pip install aws-cdk-lib constructs
   ```

2. **Create `cdk_stack.py` in `/cdk`**:
   ```python
   from aws_cdk import (
       Stack,
       Duration,
       aws_ec2 as ec2,
       aws_ecs as ecs,
       aws_ecs_patterns as ecs_patterns,
       aws_logs as logs,
       aws_secretsmanager as secretsmanager,
       aws_elasticloadbalancingv2 as elbv2,
   )
   from constructs import Construct

   class FastApiEcsStack(Stack):
       """
       CDK Stack for deploying FastAPI chatbot on ECS Fargate
       Components:
       - VPC with public/private subnets
       - ECS Fargate service with auto-scaling
       - Application Load Balancer
       - CloudWatch logging
       - Secrets Manager for API keys
       """

       def __init__(self, scope: Construct, id: str, **kwargs):
           super().__init__(scope, id, **kwargs)

           # Create VPC with public and private subnets
           vpc = ec2.Vpc(
               self, "ChatbotVpc",
               max_azs=2,  # Use 2 availability zones for high availability
               nat_gateways=1,  # NAT gateway for private subnet internet access
           )

           # Create ECS cluster
           cluster = ecs.Cluster(
               self, "ChatbotCluster",
               vpc=vpc,
               cluster_name="summer-smiles-chatbot"
           )

           # Create CloudWatch log group
           log_group = logs.LogGroup(
               self, "ChatbotLogGroup",
               log_group_name="/ecs/summer-smiles-chatbot",
               retention=logs.RetentionDays.ONE_MONTH
           )

           # Create Secrets Manager secret for OpenAI API key
           openai_secret = secretsmanager.Secret(
               self, "OpenAiApiKey",
               description="OpenAI API key for Summer Smiles chatbot",
               generate_secret_string=secretsmanager.SecretStringGenerator(
                   secret_string_template='{"OPENAI_API_KEY": ""}',
                   generate_string_key="OPENAI_API_KEY",
                   exclude_characters=' %+~`#$&*()|[]{}:;<>?!\'/@"\\',
               )
           )

           # Create Fargate service with Application Load Balancer
           fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
               self, "ChatbotService",
               cluster=cluster,
               memory_limit_mib=2048,  # 2GB memory
               cpu=1024,  # 1 vCPU
               desired_count=2,  # Start with 2 instances for HA
               task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                   image=ecs.ContainerImage.from_asset("docker"),  # Build from local Dockerfile
                   container_port=8000,
                   environment={
                       "ENVIRONMENT": "production",
                   },
                   secrets={
                       "OPENAI_API_KEY": ecs.Secret.from_secrets_manager(openai_secret, "OPENAI_API_KEY")
                   },
                   log_driver=ecs.LogDrivers.aws_logs(
                       stream_prefix="chatbot",
                       log_group=log_group
                   )
               ),
               public_load_balancer=True,  # Internet-facing load balancer
               listener_port=443,  # HTTPS
               protocol=elbv2.ApplicationProtocol.HTTPS,
               redirect_http=True,  # Redirect HTTP to HTTPS
               domain_zone=None,  # Set this if you have a custom domain
               certificate=None,  # Set this if you have an SSL certificate
           )

           # Configure health check
           fargate_service.target_group.configure_health_check(
               path="/health",
               healthy_http_codes="200",
               healthy_threshold_count=2,
               unhealthy_threshold_count=3,
               timeout=Duration.seconds(10),
               interval=Duration.seconds(30),
           )

           # Configure auto-scaling
           scaling = fargate_service.service.auto_scale_task_count(
               min_capacity=1,
               max_capacity=10
           )

           # Scale based on CPU utilization
           scaling.scale_on_cpu_utilization(
               "CpuScaling",
               target_utilization_percent=70,
               scale_in_cooldown=Duration.minutes(5),
               scale_out_cooldown=Duration.minutes(1),
           )

           # Scale based on memory utilization
           scaling.scale_on_memory_utilization(
               "MemoryScaling", 
               target_utilization_percent=80,
               scale_in_cooldown=Duration.minutes(5),
               scale_out_cooldown=Duration.minutes(1),
           )

           # Output the load balancer URL
           self.load_balancer_url = fargate_service.load_balancer.load_balancer_dns_name
   ``` 