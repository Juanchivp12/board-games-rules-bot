from datetime import datetime
from typing import Any
from pgvector.sqlalchemy import VECTOR # Imports pgvector's SQLAlchemy column type. SQAlchemy doesn't know what a vector column is
from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Document(Base):
    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(primary_key=True) # Primary key
    game: Mapped[str] = mapped_column(String(100), index=True) # Game name
    title: Mapped[str] = mapped_column(String(255)) # title of rulebook
    source_filename: Mapped[str] = mapped_column(String(255)) # name of pdf
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now()) # created at timestamp

    chunks: Mapped[list["Chunk"]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan") # If document deleted through app, its chunks are deleted too

class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(primary_key=True) # Primary key
    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id", # Must refer to a real document ID in documents table
                   ondelete="CASCADE"), #Delete related chunks if their document is deleted
        index=True,
    )
    game: Mapped[str] = mapped_column(String(100), index=True) # Stores name game on every chunk again so that when we search for embeddings, postgreSQL can filter to *game* chunks without joining the tables
    section: Mapped[str] = mapped_column(String(50)) # Citation labels
    text: Mapped[str] = mapped_column(Text) # Actual chunk of rulebook text
    embedding: Mapped[list[float]] = mapped_column(VECTOR(1024)) # Chunk's embedding

    document: Mapped["Document"] = relationship(back_populates="chunks")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(primary_key=True) # Primary key
    session_id: Mapped[str] = mapped_column(String(100), index=True) # ID representing one conversation
    role: Mapped[str] = mapped_column(String(20)) # Who created the message initially (user or assistant)
    content: Mapped[str] = mapped_column(Text) # Actual question or answer
    sources: Mapped[list[dict[str, Any]] | None] = mapped_column(
        JSONB,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )