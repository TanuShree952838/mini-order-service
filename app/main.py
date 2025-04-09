from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db

from app import schemas, services, repository

app = FastAPI()


@app.get("/products", response_model=list[schemas.ProductOut])
def get_products(db: Session = Depends(get_db)):
    return repository.get_all_products(db)


@app.post("/orders")
def submit_order(order: schemas.OrderSchema, db: Session = Depends(get_db)):
    try:
        subtotal = 0
        order_items = []

        for item in order.items:
            product = repository.get_product_by_id(db, item.product_id)
            if not product:
                raise HTTPException(status_code=404, detail=f"Product ID {item.product_id} not found.")
            if product.stock < item.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for '{product.name}'.")

            item_total = services.calculate_item_total(product.price, item.quantity)
            subtotal += item_total
            order_items.append((product, item.quantity, item_total))

        shipping = services.apply_shipping(subtotal)
        total = subtotal + shipping

        new_order = repository.create_order(db, total=total)

        for product, quantity, item_total in order_items:
            repository.create_order_item(
                db=db,
                order_id=new_order.id,
                product_id=product.id,
                quantity=quantity,
                price=item_total
            )
            repository.update_product_stock(db, product, quantity)

        db.commit()
        return {"order_id": new_order.id, "total": total}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
