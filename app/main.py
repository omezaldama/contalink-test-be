from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import settings
from app.services.top_days_service import TopSalesDaysNotificationService



scheduler = AsyncIOScheduler()


def morning_job():
    TopSalesDaysNotificationService().send_top_days_email()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    scheduler.add_job(
        morning_job,
        CronTrigger(hour=12, minute=7)
    )
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(docs_url=None, redoc_url=None, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
