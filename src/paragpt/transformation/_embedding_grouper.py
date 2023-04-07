import re
import math
import argparse
import numpy as np
import pandas as pd
import pathlib as pt
from typing import List
from collections import deque
from scipy.signal import argrelextrema
from sklearn.metrics.pairwise import cosine_similarity


def _rev_sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(0.5 * x))


def _activate_similarities(similarities: np.array, n_ticks: int = 9) -> np.array:
    n_ticks = min(n_ticks, similarities.shape[0])
    x = np.linspace(-10, 10, n_ticks)
    y = np.vectorize(_rev_sigmoid)
    activation_weights = np.pad(y(x), (0, similarities.shape[0] - n_ticks))
    diagonals = [
        similarities.diagonal(each) for each in range(0, similarities.shape[0])
    ]
    diagonals = [
        np.pad(each, (0, similarities.shape[0] - len(each))) for each in diagonals
    ]
    diagonals = np.stack(diagonals)
    diagonals = diagonals * activation_weights.reshape(-1, 1)
    activated_similarities = np.sum(diagonals, axis=0)
    return activated_similarities


def _grouper(
    df: pd.DataFrame,
    char: str,
    n_ticks: int = 100,
    embedding_name="embedding",
    snippet_name="snippet",
    n_token_name="n_tokens",
    order=2
) -> pd.DataFrame:
    embeddings: pd.Series
    snippets: pd.Series

    embeddings = df[embedding_name]
    snippets = df[snippet_name]

    similarities = cosine_similarity(np.array(embeddings.to_list()))
    activated_similarities = _activate_similarities(similarities, n_ticks=n_ticks)
    minmimas = argrelextrema(activated_similarities, np.less, order=order)[0].tolist()
    minmimas = deque(minmimas)

    if not (len(df) in minmimas):
        minmimas.append(len(snippets))

    group_assignment = []
    snippet_index_iterator = iter(enumerate(snippets))

    current_minima = minmimas.popleft()

    for i in df.index:
        if i == current_minima:
            current_minima = minmimas.popleft()
        group_assignment.append(current_minima)

    df["group"] = group_assignment

    group_by = df.groupby("group")

    grouped_snippets = group_by[snippet_name].apply(lambda x: "\n".join(x)).reset_index(drop=True)
    grouped_tokens = group_by[n_token_name].sum().reset_index(drop=True)

    snippet_n_tokens = pd.DataFrame({
        snippet_name: grouped_snippets,
        n_token_name: grouped_tokens
    })

    return snippet_n_tokens


def group_by_embedding(df: pd.DataFrame, order=2, group_weight=1200) -> List[str]:
    snippet_n_tokens = _grouper(df.copy(), "\n", order=order)
    new_groupings = []
    current_group = 0
    current_weight = 0
    for weight in snippet_n_tokens["n_tokens"]:
        current_weight+=weight
        if current_weight > group_weight:
            current_weight = 0
            new_groupings.append(current_group)
            current_group += 1
        else:
            new_groupings.append(current_group)
    snippet_n_tokens["group"] = new_groupings
    output = snippet_n_tokens.groupby("group")["snippet"].apply(lambda x : "\n".join(x)).to_list()

    return output
