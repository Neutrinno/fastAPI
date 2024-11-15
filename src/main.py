from sqlalchemy import select, Result
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from src.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
from src.models import Transaction
from src.schemas import TransactionsCreate, TransactionsRead

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(url=DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

app = FastAPI(title='Information system for accounting household expenses')

async def get_db():
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

@app.get("/")
async def hello():
    return {"message": "Здарова, заебал!"}

@app.get("/transactions", response_model=list[TransactionsRead])
async def get_transactions(session: AsyncSession = Depends(get_db)):
    query = select(Transaction).order_by(Transaction.id)
    result: Result = await session.execute(query)
    all_transactions = result.scalars().all()
    return all_transactions

@app.get("/transactions/{transaction_id}", response_model=TransactionsRead)
async def get_transaction(transaction_id: int,  session: AsyncSession = Depends(get_db)):
    return await session.get(Transaction, transaction_id)

@app.post("/transactions/create", response_model=TransactionsRead)
async def create_transactions(
    new_transition: TransactionsCreate, 
    session: AsyncSession = Depends(get_db)
):
    transaction = Transaction(**new_transition.dict())
    session.add(transaction)
    await session.commit()
    await session.refresh(transaction)
    return transaction

