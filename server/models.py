from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Customer(db.Model, SerializerMixin):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    reviews = relationship(
        "Review",
        back_populates="customer",
        cascade="all, delete-orphan"
    )

    items = association_proxy("reviews", "item")

    serialize_rules = ("-reviews.customer",)


class Item(db.Model, SerializerMixin):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)   # ✅ REQUIRED BY TESTS

    reviews = relationship(
        "Review",
        back_populates="item",
        cascade="all, delete-orphan"
    )

    customers = association_proxy("reviews", "customer")

    serialize_rules = ("-reviews.item",)


class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)

    customer_id = db.Column(db.Integer, ForeignKey("customers.id"))
    item_id = db.Column(db.Integer, ForeignKey("items.id"))

    customer = relationship("Customer", back_populates="reviews")
    item = relationship("Item", back_populates="reviews")

    serialize_rules = ("-customer.reviews", "-item.reviews")
