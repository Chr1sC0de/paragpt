import pandas as pd
from typing import List


def _get_embedding(snippet: str, embedding_model: str) -> List[int]:
    from openai.embeddings_utils import get_embedding
    return get_embedding(snippet, engine=embedding_model)


def tokenize_and_embed(
    string_list: List[str],
    embedding_model: str = "text-embedding-ada-002",
    embedding_encoding: str = "cl100k_base",
    embedding_name="embedding",
    n_token_name="n_tokens",
) -> pd.DataFrame:

    import tiktoken
    from functools import partial
    from pandarallel import pandarallel

    encoding_model = tiktoken.get_encoding(embedding_encoding)

    df = pd.DataFrame({"snippet": string_list})

    df[n_token_name] = df.snippet.apply(lambda x: len(encoding_model.encode(x)))

    pandarallel.initialize(progress_bar=False)

    df[embedding_name] = df.snippet.parallel_apply(
        partial(_get_embedding, embedding_model=embedding_model)
    )

    return df
