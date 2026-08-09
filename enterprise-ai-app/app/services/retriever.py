from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from app.core.config import get_settings

class QdrantRetriever:
    """Local reference embedding; production should use Bedrock Titan embeddings."""
    def __init__(self) -> None:
        self.cfg = get_settings()
        self.client = QdrantClient(url=self.cfg.qdrant_url)

    @staticmethod
    def embed(text: str) -> list[float]:
        values = [0.0] * 16
        for i, byte in enumerate(text.lower().encode("utf-8")):
            values[i % 16] += byte / 255
        norm = sum(x * x for x in values) ** 0.5 or 1
        return [x / norm for x in values]

    def ensure_collection(self) -> None:
        if not self.client.collection_exists(self.cfg.qdrant_collection):
            self.client.create_collection(self.cfg.qdrant_collection, vectors_config=VectorParams(size=16, distance=Distance.COSINE))

    def search(self, question: str) -> list[dict]:
        results = self.client.query_points(collection_name=self.cfg.qdrant_collection, query=self.embed(question), limit=4).points
        return [{"id": str(p.id), "text": p.payload.get("text", ""), "score": p.score} for p in results]
