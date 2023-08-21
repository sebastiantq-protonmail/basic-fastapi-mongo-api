from fastapi import APIRouter, HTTPException, Depends, Response, status
from bson import ObjectId
from typing import List

# Configuration, models and authentication modules imports
from app.api.config import db
from app.api.config.exceptions import bugReportsInstance
from app.api.config.env import JIRA_PROJECT_ID
from app.api.models.models import ItemCreate, Item
from app.api.auth.auth import auth_handler

router = APIRouter()

"""
The following document contains a basic CRUD of 'Items', 
you can change the Item's model according to your requirements and add new endpoints for new operations.

Good luck <3
ST.
"""

# Centralized error handler
def handle_error(e: Exception):
    bugReportsInstance.bugReports(JIRA_PROJECT_ID, "[DEVELOPER]", str(e))
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post('/items/', response_model=Item, status_code=status.HTTP_201_CREATED, tags=["CRUD"])
def create_item(item: ItemCreate, auth=Depends(auth_handler.authenticate)):
    """Create a new item in the database.
    
    Args:
    - item (ItemCreate): Item to be created.
    
    Returns:
    - Item: Created item with its ID.
    """
    try:
        new_item = db.database.items.insert_one(item.dict())
        item.id = str(new_item.inserted_id)
        return item
    except Exception as e:
        handle_error(e)

@router.get('/items/', response_model=List[Item], tags=["CRUD"])
def list_items(auth=Depends(auth_handler.authenticate)):
    """Fetch all items from the database.
    
    Returns:
    - List[Item]: List of items.
    """
    try:
        items = list(db.database.items.find())
        for item in items: item["_id"] = str(item["_id"])
        return items
    except Exception as e:
        handle_error(e)

@router.get('/items/{item_id}/', response_model=Item, tags=["CRUD"])
def get_item(item_id: str, auth=Depends(auth_handler.authenticate)):
    """Fetch a single item from the database using its ID.
    
    Args:
    - item_id (str): ID of the item to be fetched.
    
    Returns:
    - Item: Fetched item.
    
    Raises:
    - HTTPException: If the item is not found.
    """
    try:
        item = db.database.items.find_one({"_id": ObjectId(item_id)})
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        item["_id"] = str(item["_id"])
        return item
    except HTTPException:
        # This is to ensure HTTPException is not caught in the generic Exception
        raise
    except Exception as e:
        handle_error(e)

@router.put('/items/{item_id}/', response_model=Item, tags=["CRUD"])
def update_item(item_id: str, item_update: ItemCreate, auth=Depends(auth_handler.authenticate)):
    """Update an item in the database.
    
    Args:
    - item_id (str): ID of the item to be updated.
    - item_update (ItemCreate): New data for the item.
    
    Returns:
    - Item: Updated item.
    
    Raises:
    - HTTPException: If the item is not found.
    """
    try:
        updated_item = db.database.items.find_one_and_update({"_id": ObjectId(item_id)}, {"$set": item_update.dict()}, return_document=True)
        if not updated_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        updated_item["_id"] = str(updated_item["_id"])
        return updated_item
    except HTTPException:
        # This is to ensure HTTPException is not caught in the generic Exception
        raise
    except Exception as e:
        handle_error(e)

@router.patch('/items/{item_id}/', response_model=Item, tags=["CRUD"])
def patch_item(item_id: str, item_update: ItemCreate, auth=Depends(auth_handler.authenticate)):
    """Partially update an item in the database.
    
    Args:
    - item_id (str): ID of the item to be updated.
    - item_update (ItemCreate): New data for the item.
    
    Returns:
    - Item: Updated item.
    
    Raises:
    - HTTPException: If the item is not found.
    """
    try:
        updated_item = db.database.items.find_one_and_update({"_id": ObjectId(item_id)}, {"$set": item_update.dict()}, return_document=True)
        if not updated_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        updated_item["_id"] = str(updated_item["_id"])
        return updated_item
    except Exception as e:
        handle_error(e)

@router.delete('/items/{item_id}/', response_model=Item, tags=["CRUD"])
def delete_item(item_id: str, response: Response, auth=Depends(auth_handler.authenticate)):
    """Delete an item from the database.
    
    Args:
    - item_id (str): ID of the item to be deleted.
    
    Returns:
    - Item: Deleted item.
    
    Raises:
    - HTTPException: If the item is not found.
    """
    try:
        deleted_item = db.database.items.find_one_and_delete({"_id": ObjectId(item_id)})
        if deleted_item:
            response.status_code = status.HTTP_200_OK
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        # ALWAYS convert the ObjectId to str before return
        deleted_item["_id"] = str(deleted_item["_id"])
        return deleted_item
    except HTTPException:
        # This is to ensure HTTPException is not caught in the generic Exception
        raise
    except Exception as e:
        handle_error(e)

