import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "fastapi-dynamodb-table")


settings = Settings()