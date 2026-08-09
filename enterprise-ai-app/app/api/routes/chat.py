import uuid
from fastapi import APIRouter, Depends
from app.core.security import current_user
from app.schemas.chat import ChatRequest, ChatResponse, Source
from app.services.graph import build_graph

router = APIRouter(prefix="/v1", tags=["chat"])
graph = build_graph()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, user: dict = Depends(current_user)):
    result = graph.invoke({"question": request.question, "sources": [], "answer": ""}, config={"configurable": {"user_id": user["sub"]}})
    return ChatResponse(answer=result["answer"], sources=[Source(**x) for x in result["sources"]], conversation_id=request.conversation_id or str(uuid.uuid4()))
