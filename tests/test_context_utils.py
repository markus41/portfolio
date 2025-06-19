from src.utils.context import summarise_messages


def test_summarise_messages_no_trim():
    msgs = [{"role": "user", "content": "hello world"}]
    out = summarise_messages(msgs, max_tokens=10)
    assert out == msgs

def test_summarise_messages_trimmed():
    msgs = [{"role": "user", "content": "word " * 20}] * 6
    out = summarise_messages(msgs, max_tokens=50, summary_tokens=5)
    assert out[0]["role"] == "system"
    assert "Summary" in out[0]["content"]
    assert len(out) < len(msgs)
