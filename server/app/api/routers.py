from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.data import models, schemas, db
from app.services.jobs import enqueue_request

router = APIRouter()

# -------------------------
# Users
# -------------------------
@router.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, session: AsyncSession = Depends(db.get_db)):
    new_user = models.User(**user.dict())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user

@router.get("/users/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, session: AsyncSession = Depends(db.get_db)):
    result = await session.execute(select(models.User).where(models.User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# -------------------------
# Brokers
# -------------------------
@router.post("/brokers/", response_model=schemas.Broker)
async def create_broker(broker: schemas.BrokerCreate, session: AsyncSession = Depends(db.get_db)):
    new_broker = models.Broker(**broker.dict())
    session.add(new_broker)
    await session.commit()
    await session.refresh(new_broker)
    return new_broker

@router.get("/brokers/", response_model=list[schemas.Broker])
async def list_brokers(session: AsyncSession = Depends(db.get_db)):
    result = await session.execute(select(models.Broker))
    brokers = result.scalars().all()
    return brokers

# -------------------------
# Requests
# -------------------------
@router.post("/requests/", response_model=schemas.RequestLog)
async def create_request(request: schemas.RequestLogBase, session: AsyncSession = Depends(db.get_db)):
    new_request = models.RequestLog(**request.dict())
    session.add(new_request)
    await session.commit()
    await session.refresh(new_request)
    
    # Enqueue async job for worker
    enqueue_request(new_request.id)
    
    return new_request

@router.get("/requests/", response_model=list[schemas.RequestLog])
async def list_requests(session: AsyncSession = Depends(db.get_db)):
    result = await session.execute(select(models.RequestLog))
    requests = result.scalars().all()
    return requests
