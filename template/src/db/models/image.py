from sqlalchemy import Column, Integer, String, Float, JSON
from db.session import Base

class ImageRecord(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    url = Column(String)
    # Storing embeddings in DB - depending on DB could be JSON, Array, or pgvector
    features = Column(JSON)
    caption = Column(String, nullable=True)
