from app import db
from app.models import Product

def add_product(name, description, price, imageResourceUrl, storeName, status):
    new_product = Product(
        productName=name,
        description=description,
        price=price,
        imageResourceUrl=imageResourceUrl,
        storeName=storeName,
        status=status
    )
    db.session.add(new_product)
    try:
        db.session.commit()
        return new_product
    except Exception as e:
        db.session.rollback()
        print(e)
        return None