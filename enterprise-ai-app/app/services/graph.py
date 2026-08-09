from typing import TypedDict
from langgraph.graph import END, START, StateGraph
from app.services.retriever import QdrantRetriever
from app.services.bedrock import BedrockChat

class GraphState(TypedDict):
    question: str
    tenant_id: str
    history: list[dict]
    sources: list[dict]
    answer: str

def build_graph():
    retriever, model = QdrantRetriever(), BedrockChat()
    def retrieve(state: GraphState): return {"sources": retriever.search(state["question"], state["tenant_id"])}
    def generate(state: GraphState):
        history = "\n".join(f"{x['role']}: {x['content']}" for x in state["history"][-8:])
        return {"answer": model.answer(f"History:\n{history}\n\nQuestion: {state['question']}", state["sources"])}
    graph = StateGraph(GraphState)
    graph.add_node("retrieve", retrieve)
    graph.add_node("generate", generate)
    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    return graph.compile()
