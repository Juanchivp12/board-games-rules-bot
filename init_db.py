import asyncio
from sqlalchemy import text
from database import Base, engine
import models

async def init_db():
    async with engine.begin() as connection:
        await connection.execute(
            text("CREATE EXTENSION IF NOT EXISTS vector")
        )
        await connection.run_sync(Base.metadata.create_all) # Create every table registered under Base

    await engine.dispose()
    print("Database tables created")

if __name__ == "__main__":
    asyncio.run(init_db())