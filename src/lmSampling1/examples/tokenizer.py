from functools import cache
from huggingface_hub import hf_hub_download
from tokenizers import Tokenizer


def tokenize(string: str) -> tuple[list[int], list[str]]:
    tok = _tokenizer()
    ids = tok.encode(string, add_special_tokens=False).ids
    return ids, [tok.decode([i]) for i in ids]

MODEL = "Motif-Technologies/Motif-3"

def _tokenizer():
    return Tokenizer.from_file(hf_hub_download(MODEL, "tokenizer.json"))

def vocab() -> list[str]:
    tok = _tokenizer()
    return tok.decode_batch([[i] for i in range(tok.get_vocab_size())])


if __name__ == "__main__":
    print(len(vocab()))