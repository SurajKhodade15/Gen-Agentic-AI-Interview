from typing import TypedDict
from langgraph.graph import END, START, StateGraph
from app.services.retriever import QdrantRetriever
from app.services.bedrock import BedrockChat

class GraphState(TypedDict):
    question: str
    sources: list[dict]
    answer: str

def build_graph():
    retriever, model = QdrantRetriever(), BedrockChat()
    def retrieve(state: GraphState): return {"sources": retriever.search(state["question"])}
    def generate(state: GraphState): return {"answer": model.answer(state["question"], state["sources"])}
    graph = StateGraph(GraphState)
    graph.add_node("retrieve", retrieve)
    graph.add_node("generate", generate)
    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    return graph.compile()
