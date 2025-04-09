from sqlalchemy.orm import Session
from app.models import Product, Order, OrderItem


def get_all_products(db: Session):
    return db.query(Product).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def create_order(db: Session, total: float) -> Order:
    new_order = Order(total=total)
    db.add(new_order)
    db.flush()  # To get new_order.id before committing
    return new_order


def create_order_item(db: Session, order_id: int, product_id: int, quantity: int, price: float):
    order_item = OrderItem(
        order_id=order_id,
        product_id=product_id,
        quantity=quantity,
        price=price
    )
    db.add(order_item)


def update_product_stock(db: Session, product: Product, quantity: int):
    product.stock -= quantity
