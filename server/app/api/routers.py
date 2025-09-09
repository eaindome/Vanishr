import logging
import traceback
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, and_
from app.data import models, schemas, db
from app.services.jobs import enqueue_request

# Configure logging
logger = logging.getLogger("api.routers")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

router = APIRouter()


@router.get(
    "/users/",
    response_model=list[schemas.User],
    tags=["Users"],
    description="List users with optional pagination and search.",
)
async def list_users(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return"),
    search: Optional[str] = Query(None, description="Search by name or email"),
    session: AsyncSession = Depends(db.get_db),
):
    try:
        query = select(models.User)
        if search:
            query = query.where(
                or_(
                    models.User.full_name.ilike(f"%{search}%"),
                    models.User.email.ilike(f"%{search}%"),
                )
            )
        query = query.offset(skip).limit(limit)
        result = await session.execute(query)
        users = result.scalars().all()
        return users
    except Exception as e:
        logger.error(f"Failed to list users: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to list users.")


# -------------------------
# Users
# -------------------------
@router.post(
    "/users/",
    response_model=schemas.User,
    tags=["Users"],
    description="Create a new user.",
)
async def create_user(
    user: schemas.UserCreate, session: AsyncSession = Depends(db.get_db)
):
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


@router.get(
    "/users/{user_id}",
    response_model=schemas.User,
    tags=["Users"],
    description="Get a user by their ID.",
)
async def get_user(user_id: int, session: AsyncSession = Depends(db.get_db)):
    try:
        result = await session.execute(
            select(models.User).where(models.User.id == user_id)
        )
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


@router.get(
    "/brokers/",
    response_model=list[schemas.Broker],
    tags=["Brokers"],
    description="List brokers with optional pagination and search.",
)
async def list_brokers(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return"),
    search: Optional[str] = Query(None, description="Search by broker name or notes"),
    opt_out_method: Optional[str] = Query(
        None, description="Filter by opt-out method (form, email, letter)"
    ),
    session: AsyncSession = Depends(db.get_db),
):
    try:
        query = select(models.Broker)
        if search:
            query = query.where(
                or_(
                    models.Broker.name.ilike(f"%{search}%"),
                    models.Broker.notes.ilike(f"%{search}%"),
                )
            )
        if opt_out_method:
            query = query.where(models.Broker.opt_out_method == opt_out_method)
        query = query.offset(skip).limit(limit)
        result = await session.execute(query)
        brokers = result.scalars().all()
        return brokers
    except Exception as e:
        logger.error(f"Failed to list brokers: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to list brokers.")


# -------------------------
# Brokers
# -------------------------
@router.post(
    "/brokers/",
    response_model=schemas.Broker,
    tags=["Brokers"],
    description="Create a new broker.",
)
async def create_broker(
    broker: schemas.BrokerCreate, session: AsyncSession = Depends(db.get_db)
):
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


# -------------------------
# Requests
# -------------------------
@router.post(
    "/requests/",
    response_model=schemas.RequestLog,
    tags=["Requests"],
    description="Create a new opt-out request.",
)
async def create_request(
    request: schemas.RequestLogBase, session: AsyncSession = Depends(db.get_db)
):
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


@router.get(
    "/requests/",
    response_model=list[schemas.RequestLog],
    tags=["Requests"],
    description="List requests with optional pagination and filtering.",
)
async def list_requests(
    skip: int = Query(0, ge=0, description="Number of records to skip for pagination"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    broker_id: Optional[int] = Query(None, description="Filter by broker ID"),
    status: Optional[str] = Query(
        None, description="Filter by request status (Pending, Completed, Failed)"
    ),
    session: AsyncSession = Depends(db.get_db),
):
    try:
        query = select(models.RequestLog)
        filters = []
        if user_id:
            filters.append(models.RequestLog.user_id == user_id)
        if broker_id:
            filters.append(models.RequestLog.broker_id == broker_id)
        if status:
            filters.append(models.RequestLog.status == status)
        if filters:
            query = query.where(and_(*filters))
        query = query.offset(skip).limit(limit)
        result = await session.execute(query)
        requests = result.scalars().all()
        return requests
    except Exception as e:
        logger.error(f"Failed to list requests: {e}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to list requests.")
