"""Seed local Qdrant after `docker compose up -d qdrant`."""
from qdrant_client.models import PointStruct
from app.services.retriever import QdrantRetriever

DOCS = [
    "Expense reports must be submitted within 30 days of purchase.",
    "Employees may work remotely up to three days per week with manager approval.",
    "Customer data must not be copied into unapproved third-party systems.",
]

retriever = QdrantRetriever()
retriever.ensure_collection()
retriever.client.upsert(
    retriever.cfg.qdrant_collection,
    points=[PointStruct(id=i + 1, vector=retriever.embed(text), payload={"text": text, "source": "employee-handbook"}) for i, text in enumerate(DOCS)],
)
print(f"Seeded {len(DOCS)} documents into {retriever.cfg.qdrant_collection}")
