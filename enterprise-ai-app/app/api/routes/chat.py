import uuid
from fastapi import APIRouter, Depends
from app.core.security import current_user
from app.schemas.chat import ChatRequest, ChatResponse, Source
from app.services.graph import build_graph
from app.services.redis_store import RedisConversationStore
from app.middleware.rate_limit import enforce_rate_limit

router = APIRouter(prefix="/v1", tags=["chat"])
graph = build_graph()

@router.post("/chat", response_model=ChatResponse, dependencies=[Depends(enforce_rate_limit)])
def chat(request: ChatRequest, user: dict = Depends(current_user)):
    tenant_id = user.get("tenant_id", user["sub"])
    conversation_id = request.conversation_id or str(uuid.uuid4())
    memory = RedisConversationStore()
    result = graph.invoke({"question": request.question, "tenant_id": tenant_id, "history": memory.history(tenant_id, conversation_id), "sources": [], "answer": ""}, config={"configurable": {"user_id": user["sub"]}})
    memory.append(tenant_id, conversation_id, "user", request.question)
    memory.append(tenant_id, conversation_id, "assistant", result["answer"])
    return ChatResponse(answer=result["answer"], sources=[Source(**x) for x in result["sources"]], conversation_id=conversation_id)
