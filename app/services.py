from app.config import settings

async def update_item(dynamodb, item_id, update_data):
    table = await dynamodb.Table(settings.DYNAMODB_TABLE_NAME)
    expression = "SET " + ", ".join([f"#{key} = :{key}" for key in update_data.keys()])
    expression_names = {f"#{key}": key for key in update_data.keys()}
    expression_values = {f":{key}": value for key, value in update_data.items()}
    await table.update_item(
        Key={'id': item_id},
        UpdateExpression=expression,
        ExpressionAttributeNames=expression_names,
        ExpressionAttributeValues=expression_values,
    )
    return {'message': 'Item updated successfully'}

async def create_item(dynamodb, item_data):
    table = await dynamodb.Table(settings.DYNAMODB_TABLE_NAME)
    await table.put_item(Item=item_data)
    return item_data

async def get_item(dynamodb, item_id):
    table = await dynamodb.Table(settings.DYNAMODB_TABLE_NAME)
    response = await table.get_item(Key={'id': item_id})
    return response.get('Item', None)

async def delete_item(dynamodb, item_id):
    table = await dynamodb.Table(settings.DYNAMODB_TABLE_NAME)
    await table.delete_item(Key={'id': item_id})
    return {'message': 'Item deleted successfully'}
