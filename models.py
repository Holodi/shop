from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.future import engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Cart(Base):
    __tablename__ = 'cart'
    user_login = Column(String(50), ForeignKey('user.login'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    user = relationship('User', back_populates='cart')
    item = relationship('Item', back_populates='cart')


class Category(Base):
    __tablename__ = 'category'
    cat_id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    items = relationship('Item', back_populates='category')


class Comparison(Base):
    __tablename__ = 'comparison'
    cmp_id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    name = Column(String(50), nullable=False)

    item = relationship('Item', back_populates='comparison')


class Favorites(Base):
    __tablename__ = 'favorites'
    list_id = Column(Integer, primary_key=True)
    items = Column(String(255), nullable=False)

    user = relationship('User', back_populates='favorites')


class Feedback(Base):
    __tablename__ = 'feedback'
    feedback_id = Column(Integer, primary_key=True)
    itm_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    text = Column(String(255))
    rating = Column(Integer)
    user_login = Column(String(50), ForeignKey('user.login'), nullable=False)

    item = relationship('Item', back_populates='feedbacks')
    user = relationship('User', back_populates='feedbacks')


class Items(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    status = Column(Integer, ForeignKey('itm_status.stat_id'), nullable=False)
    category = Column(Integer, ForeignKey('category.cat_id'), nullable=False)
    review = Column(Integer, ForeignKey('review.cat_id'), nullable=False)

    status = relationship('ItemStatus', back_populates='items')
    category = relationship('Category', back_populates='items')
    cart = relationship('Cart', back_populates='item')
    comparison = relationship('Comparison', back_populates='item')
    feedbacks = relationship('Feedback', back_populates='item')


class ItemStatus(Base):
    __tablename__ = 'itm_status'
    stat_id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    items = relationship('Items', back_populates='status')


class Order(Base):
    __tablename__ = 'ord'
    order_id = Column(Integer, primary_key=True)
    user_login = Column(String(50), ForeignKey('user.login'), nullable=False)
    address = Column(String(255), nullable=False)
    order_total_price = Column(Float, nullable=False)
    status = Column(Integer, ForeignKey('order_status.stat_id'), nullable=False)

    user = relationship('User', back_populates='orders')


class OrderItems(Base):
    __tablename__ = 'order_items'
    order_id = Column(Integer, ForeignKey('order.order_id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), primary_key=True)


class OrderStatus(Base):
    __tablename__ = 'order_status'
    stat_id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    orders = relationship('Order', back_populates='status')


class Review(Base):
    __tablename__ = 'review'
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    text = Column(String(255))
    rating = Column(Integer)
    review_id = Column(Integer, primary_key=True)

    item = relationship('Items', back_populates='reviews')
    user = relationship('User', back_populates='reviews')


class User(Base):
    __tablename__ = 'user'
    login = Column(String(50), primary_key=True)
    orders = relationship('Order', back_populates='user')
    waitlist = relationship('Waitlist', back_populates='user')
    wishlist = relationship('Wishlist', back_populates='user')
    feedbacks = relationship('Feedback', back_populates='user')
    cart = relationship('Cart', back_populates='user')
    favorites = relationship('Favorites', back_populates='user')
    reviews = relationship('Review', back_populates='user')


class Waitlist(Base):
    __tablename__ = 'waitlist'
    user_login = Column(String(50), ForeignKey('user.login'), primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'), primary_key=True)


class Wishlist(Base):
    __tablename__ = 'wishlist'
    list_id = Column(Integer, primary_key=True)
    list_name = Column(String(50), nullable=False)
    user_login = Column(String(50), ForeignKey('user.login'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)


Base.metadata.create_all(bind=engine)

