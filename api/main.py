from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="FastAPI Demo", version="1.0.0")


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int = 1


class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    quantity: int
    total: float


items_db: dict[int, Item] = {}
item_counter = 0


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to FastAPI Demo"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/items", response_model=ItemResponse)
async def create_item(item: Item):
    """Create a new item"""
    global item_counter
    item_counter += 1
    items_db[item_counter] = item
    return ItemResponse(
        id=item_counter,
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
        total=item.price * item.quantity,
    )


@app.get("/items")
async def list_items():
    """List all items"""
    return [
        ItemResponse(
            id=item_id,
            name=item.name,
            description=item.description,
            price=item.price,
            quantity=item.quantity,
            total=item.price * item.quantity,
        )
        for item_id, item in items_db.items()
    ]


@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    """Get a specific item by ID"""
    if item_id not in items_db:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Item not found")
    item = items_db[item_id]
    return ItemResponse(
        id=item_id,
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
        total=item.price * item.quantity,
    )


@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    """Delete an item by ID"""
    if item_id not in items_db:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": f"Item {item_id} deleted successfully"}
