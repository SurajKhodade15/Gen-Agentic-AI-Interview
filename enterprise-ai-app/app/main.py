from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.api.routes import auth, chat
from app.services.retriever import QdrantRetriever
from app.services.redis_store import RedisConversationStore

@asynccontextmanager
async def lifespan(_: FastAPI):
    configure_logging()
    QdrantRetriever().ensure_collection()
    yield

app = FastAPI(title="Enterprise AI API", version="2.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=get_settings().allowed_origins.split(","), allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth.router)
app.include_router(chat.router)
app.mount("/metrics", make_asgi_app())

@app.get("/healthz", tags=["operations"])
def healthz(): return {"status": "ok"}

@app.get("/readyz", tags=["operations"])
def readyz(): return {"status": "ready", "redis": RedisConversationStore().healthy()}
