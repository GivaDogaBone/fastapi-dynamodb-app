import aioboto3
from app.config import settings


async def get_dynamodb_client():
    session = aioboto3.Session()
    async with session.resource('dynamodb', region_name=settings.AWS_REGION) as dynamodb:
        yield dynamodb