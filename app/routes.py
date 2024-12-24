from fastapi import APIRouter, Depends, HTTPException
from app.models import Item
from app.dependencies import get_dynamodb_client
from app.services import create_item, get_item, delete_item, update_item
router = APIRouter()
@router.get("/")
async def root():
    return {"message": "Welcome to the FastAPI DynamoDB project!"}
@router.post("/item/", response_model=Item)
async def create_new_item(item: Item, dynamodb=Depends(get_dynamodb_client)):
    return await create_item(dynamodb, item.dict())
@router.delete("/item/{item_id}")
async def delete_item_by_id(item_id: str, dynamodb=Depends(get_dynamodb_client)):
    result = await delete_item(dynamodb, item_id)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
@router.get("/item/{item_id}", response_model=Item)
async def read_item(item_id: str, dynamodb=Depends(get_dynamodb_client)):
    result = await get_item(dynamodb, item_id)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result
@router.put("/item/{item_id}", response_model=Item)
async def update_item_by_id(item_id: str, item: Item, dynamodb=Depends(get_dynamodb_client)):
    updated_item = await update_item(dynamodb, item_id, item.dict())
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item
