from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.helper.config import get_settings
from src.routes.data import router as asset_router
from src.routes.nlpquery import router as nlp_router


app = FastAPI(
    title="DarkAtlas Asset Management",
    version="1.0.0"
)



@app.on_event("startup")
async def startup_span():
    settings = get_settings()

    postgres = settings.DATABASE_URL
    app.db_engine = create_async_engine(postgres)
    app.db_client = sessionmaker(
        app.db_engine, class_=AsyncSession, expire_on_commit=False
    )




@app.on_event("shutdown")
async def shutdown_span():
    await app.db_engine.dispose()

app.include_router(asset_router)
app.include_router(nlp_router)