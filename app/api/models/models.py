from typing import Optional
from pydantic import BaseModel

# Define your data models and schemas here
# For now, using generic examples

class ItemCreate(BaseModel):
    """
    Data model for creating a new item.
    
    This model is used when a new item is being created and doesn't have an ID yet. By separating the creation model
    from the general item model, it ensures that the ID is not provided or altered during the creation process.
    """
    name: str
    description: str

class Item(ItemCreate):
    """
    Data model for an existing item.
    
    This model extends the ItemCreate model by including an ID attribute. It's used when an item is being 
    fetched, updated, or deleted. The separation ensures that the ID is always present for existing items,
    making it clear when an item is new (without an ID) versus when it's an existing item (with an ID).
    """
    id: str