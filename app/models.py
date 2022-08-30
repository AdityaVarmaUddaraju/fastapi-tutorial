from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, func
from sqlalchemy.orm import relationship

from .database import Base

class Posts(Base):
    __tablename__  = "posts"

    id = Column(Integer, primary_key = True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True')
    timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("Users", back_populates="posts")

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), server_default=func.now())

    posts = relationship("Posts", back_populates="owner")

class Vote(Base):
    __tablename__ = 'votes'

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)