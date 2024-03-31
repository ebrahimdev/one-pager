from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(128), index=True, unique=True)
    description = db.Column(db.String(1024))
    price = db.Column(db.String(64))
    imageResourceUrl = db.Column(db.String(256))
    storeName = db.Column(db.String(128))
    status = db.Column(db.String(64), default='fetched')
    
    def __repr__(self):
        return '<Product {}>'.format(self.name)
