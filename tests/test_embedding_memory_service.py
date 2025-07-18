from src.memory_service.embedding import EmbeddingMemoryService


def test_similarity_ranking():
    svc = EmbeddingMemoryService()
    svc.store("", {"text": "the quick brown fox"})
    svc.store("", {"text": "the fast brown fox"})
    svc.store("", {"text": "lorem ipsum"})

    res = svc.fetch("quick fox", top_k=2)
    assert res[0]["text"] == "the quick brown fox"
    assert res[1]["text"] == "the fast brown fox"
    assert len(res) == 2


def test_empty_result():
    svc = EmbeddingMemoryService()
    assert svc.fetch("anything") == []
