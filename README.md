## FastAPI Project
Here is a **complete FastAPI project setup** that includes **Poetry** for package management, **Pytest-Asyncio** for asynchronous testing, **Swagger UI** for API documentation, **AWS DynamoDB** for the database, **Docker** for containerization, **GitHub Actions** for CI/CD, and **AWS Elastic Beanstalk** for deployment.

---

### **Project Structure**

Here’s the structure of the project:

```
fastapi-dynamodb-project
├── app
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   ├── services.py
│   ├── dependencies.py
│   ├── config.py
│   └── __init__.py
├── tests
│   ├── test_app.py
│   └── __init__.py
├── .github
│   └── workflows
│       └── ci-cd.yml
├── poetry.lock
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── .elasticbeanstalk
│   └── config.yml
├── README.md
├── requirements.txt
└── .env
```

---

### **Step-by-Step Setup**

#### 1. **Initialize Poetry Project**
1. Create a new Poetry project:
```shell script
poetry new fastapi-dynamodb-project
cd fastapi-dynamodb-project
```
2. Add dependencies:
```shell script
poetry add fastapi uvicorn boto3 aioboto3 python-dotenv
poetry add pytest pytest-asyncio httpx --group dev
```

---

#### 2. **FastAPI App Code**

Create AWS DynamoDB
```shell script
aws dynamodb create-table --table-name fastapi-dynamodb-table --attribute-definitions AttributeName=id,AttributeType=S --key-schema AttributeName=id,KeyType=HASH --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 --region us-east-1
```

Verify the table's region
```shell script
aws dynamodb list-tables --region your-region-here
```

- **`requirements.txt`: Requirements**
```txt
fastapi==0.100.0
uvicorn[standard]==0.23.1
boto3==1.28.57
aioboto3==11.3.2
python-dotenv==1.0.0

# Development and testing dependencies
pytest==7.2.3
pytest-asyncio==0.21.0
httpx==0.24.1
```

- **`.env`: .env**
```txt
# Application Settings
APP_ENV=development
APP_NAME=FastAPI-DynamoDB-App
APP_VERSION=1.0.0

# AWS Configuration
AWS_REGION=us-east-1
DYNAMODB_TABLE_NAME=fastapi-dynamodb-table

# Other Settings (if needed)
DEBUG=True
```

- **`pyproject.toml`: `pyproject.toml`**
```txt
[tool.poetry]
name = "fastapi-dynamodb-app"
version = "1.0.0"
description = "A FastAPI project integrated with AWS DynamoDB."
authors = ["Your Name <your-email@example.com>"]
license = "MIT"
readme = "README.md"
homepage = "https://github.com/yourusername/fastapi-dynamodb-app"
repository = "https://github.com/yourusername/fastapi-dynamodb-app"
keywords = ["fastapi", "dynamodb", "aws", "api", "python"]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.100.0"
uvicorn = {extras = ["standard"], version = "^0.23.1"}
boto3 = "^1.28.57"
aioboto3 = "^11.3.2"
python-dotenv = "^1.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.2.3"
pytest-asyncio = "^0.21.0"
httpx = "^0.24.1"
black = "^23.9.1"
isort = "^5.12.0"
flake8 = "^6.1.0"

[build-system]
requires = ["poetry-core>=1.5.0"]
build-backend = "poetry.core.masonry.api"
```

- **`app/config.py`: Environment Configuration**
```python
import os
  from dotenv import load_dotenv

  load_dotenv()

  class Settings:
      AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
      DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "fastapi-dynamodb-table")

  settings = Settings()
```

- **`app/models.py`: Define Data Models**
```python
from pydantic import BaseModel

  class Item(BaseModel):
      id: str
      name: str
      description: str | None = None
```

- **`app/dependencies.py`: Dependency for DynamoDB**
```python
import aioboto3
  from app.config import settings

  async def get_dynamodb_client():
      session = aioboto3.Session()
      async with session.resource('dynamodb', region_name=settings.AWS_REGION) as dynamodb:
          yield dynamodb
```

- **`app/services.py`: Business Logic Layer**
```python
from app.config import settings

  async def create_item(dynamodb, item_data):
      table = await dynamodb.Table(settings.DYNAMODB_TABLE_NAME)
      await table.put_item(Item=item_data)
      return item_data

  async def get_item(dynamodb, item_id):
      table = await dynamodb.Table(settings.DYNAMODB_TABLE_NAME)
      response = await table.get_item(Key={'id': item_id})
      return response.get('Item', None)
```

- **`app/routes.py`: API Endpoints**
```python
from fastapi import APIRouter, Depends, HTTPException
  from app.models import Item
  from app.dependencies import get_dynamodb_client
  from app.services import create_item, get_item

  router = APIRouter()

  @router.get("/")
  async def root():
      return {"message": "Welcome to the FastAPI DynamoDB project!"}

  @router.post("/item/", response_model=Item)
  async def create_new_item(item: Item, dynamodb=Depends(get_dynamodb_client)):
      return await create_item(dynamodb, item.dict())

  @router.get("/item/{item_id}", response_model=Item)
  async def read_item(item_id: str, dynamodb=Depends(get_dynamodb_client)):
      result = await get_item(dynamodb, item_id)
      if not result:
          raise HTTPException(status_code=404, detail="Item not found")
      return result
```

- **`app/main.py`: Application Entry Point**
```python
from fastapi import FastAPI
  from app.routes import router

  app = FastAPI(title="FastAPI with DynamoDB")

  app.include_router(router)
```

---

#### 3. **Testing**

- **`tests/test_app.py`:**
```python
import pytest
  from httpx import AsyncClient
  from app.main import app

  @pytest.mark.asyncio
  async def test_root_endpoint():
      async with AsyncClient(app=app, base_url="http://test") as ac:
          response = await ac.get("/")
      assert response.status_code == 200
      assert response.json() == {"message": "Welcome to the FastAPI DynamoDB project!"}
```

---

#### 4. **Dockerize**

- **`Dockerfile`:**
```dockerfile
FROM python:3.11-slim

  WORKDIR /app

  COPY pyproject.toml poetry.lock /app/
  RUN pip install poetry && poetry install --no-dev

  COPY . /app

  CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- **`docker-compose.yml`:**
```yaml
version: "3.8"
  services:
    app:
      build: .
      ports:
        - "8000:8000"
      environment:
        AWS_REGION: "us-east-1"
        DYNAMODB_TABLE_NAME: "fastapi-dynamodb-table"
```

---

#### 5. **GitHub Actions**

- **`.github/workflows/ci-cd.yml`:**
```yaml
name: CI/CD for FastAPI DynamoDB

  on:
    push:
      branches:
        - main
    pull_request:
      branches:
        - main

  jobs:
    test:
      runs-on: ubuntu-latest

      steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - name: Install Poetry
        run: pip install poetry
      - name: Install Dependencies
        run: poetry install
      - name: Run Tests
        run: poetry run pytest

    deploy:
      runs-on: ubuntu-latest
      needs: test

      steps:
      - uses: actions/checkout@v3
      - name: Deploy to Elastic Beanstalk
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_REGION: "us-east-1"
        run: |
          pip install awsebcli
          eb init -p docker fastapi-dynamodb --region us-east-1
          eb deploy
```

---

#### 6. **Deploy on AWS Elastic Beanstalk**

- **`.elasticbeanstalk/config.yml`:**
```yaml
platform: docker
  branch-defaults:
    default:
      environment: fastapi-dynamodb
  environment-defaults:
    fastapi-dynamodb:
      branch: null
  global:
    application_name: fastapi-dynamodb
```

Deploy using AWS CLI:
```shell script
eb init -p docker fastapi-dynamodb --region us-east-1
eb create fastapi-dynamodb-env
```

---

### Run Locally

1. Start the FastAPI server:
```shell script
poetry run uvicorn app.main:app --reload
```
2. Access Swagger UI at `http://127.0.0.1:8000/docs`.

---

This project setup ensures a robust pipeline for building, testing, and deploying your application! Let me know if you need further assistance.
