
import logging
import traceback
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.data import models, schemas, db
from app.services.jobs import enqueue_request

# Configure logging
logger = logging.getLogger("api.routers")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

router = APIRouter()

# -------------------------
# Users
# -------------------------
@router.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, session: AsyncSession = Depends(db.get_db)):
    try:
        new_user = models.User(**user.dict())
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        logger.info(f"User created: {new_user.id}")
        return new_user
    except Exception as e:
        logger.error(f"Failed to create user: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to create user.")

@router.get("/users/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, session: AsyncSession = Depends(db.get_db)):
    try:
        result = await session.execute(select(models.User).where(models.User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            logger.warning(f"User not found: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get user {user_id}: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to get user.")

# -------------------------
# Brokers
# -------------------------
@router.post("/brokers/", response_model=schemas.Broker)
async def create_broker(broker: schemas.BrokerCreate, session: AsyncSession = Depends(db.get_db)):
    try:
        new_broker = models.Broker(**broker.dict())
        session.add(new_broker)
        await session.commit()
        await session.refresh(new_broker)
        logger.info(f"Broker created: {new_broker.id}")
        return new_broker
    except Exception as e:
        logger.error(f"Failed to create broker: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to create broker.")

@router.get("/brokers/", response_model=list[schemas.Broker])
async def list_brokers(session: AsyncSession = Depends(db.get_db)):
    try:
        result = await session.execute(select(models.Broker))
        brokers = result.scalars().all()
        return brokers
    except Exception as e:
        logger.error(f"Failed to list brokers: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to list brokers.")

# -------------------------
# Requests
# -------------------------
@router.post("/requests/", response_model=schemas.RequestLog)
async def create_request(request: schemas.RequestLogBase, session: AsyncSession = Depends(db.get_db)):
    try:
        new_request = models.RequestLog(**request.dict())
        session.add(new_request)
        await session.commit()
        await session.refresh(new_request)
        enqueue_request(new_request.id)
        logger.info(f"Request created and enqueued: {new_request.id}")
        return new_request
    except Exception as e:
        logger.error(f"Failed to create request: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to create request.")

@router.get("/requests/", response_model=list[schemas.RequestLog])
async def list_requests(session: AsyncSession = Depends(db.get_db)):
    try:
        result = await session.execute(select(models.RequestLog))
        requests = result.scalars().all()
        return requests
    except Exception as e:
        logger.error(f"Failed to list requests: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to list requests.")
