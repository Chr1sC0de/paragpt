import re
import numpy as np
import pathlib as pt
import pandas as pd
try:
    import paragpt as sg
except ModuleNotFoundError:
    import sys
    import pathlib as pt
    sys.path.append((pt.Path(__file__).parent/"src").as_posix())
    import paragpt as sg
from numpy import vectorize
from functools import partial
import paragpt.transformation as T
from triple_quote_clean import TripleQuoteCleaner

tqc = TripleQuoteCleaner()


train_of_thought = [
    {
        "role": "assistant",
        "content": "let's think through how we can generate the required paraphrase",
    },
    {
        "role": "assistant",
        "content": tqc
        ** """
            To paraphrase the above conversation, I will maintain the conversation format, keeping the full
            names of the participants. I will compress the information by focusing on the key details,
            requirements, todos, and salient information. I will remove repetitive elements, rephrase
            sentences for clarity, and use more concise language while ensuring the overall meaning and
            intent of the conversation remain intact.
        """,
    },
    {
        "role": "assistant",
        "content": "what should I expect the output to look like...",
    },
    {
        "role": "assistant",
        "content": tqc
        ** """
            The output text will be a paraphrased version of the original conversation in a conversation format,
            with each person's full name maintained. It will be shorter and more concise, with repetitive
            elements removed and sentences rephrased for clarity. The key details, requirements, todos, and
            salient information will be preserved to ensure the overall meaning and intent of the conversation
            remain intact.

            assistant_1: Let's begin the paraphrasing process
            assistant_2: The paraphrased version of the conversation provided ..

        """,
    },
]

_system_prompt = (
    tqc
    ** """
        You are a helpful ai assistant working in the data space within the Australian Energy Market.
        You are currently assisting the data science and data engineering team
    """
)

extractor = sg.utils.Pipeline(sg.extraction.read_text)


def load(
    string: str,
    paraphraser_model: str = "gpt-3.5-turbo",
    system_prompt: str = _system_prompt,
    stage_1_cache=None,
    stage_2_cache=None,
    max_tokens_per_chunk=1500,
    start_chunking=2800
) -> str:
    transformer = sg.utils.Pipeline(
        T.clean_teams_vtt,
        sg.cache.DataFrame(stage_1_cache, T.tokenize_and_embed),
        sg.utils.Conditional(
            operation=partial(T.group_by_embedding, group_weight=max_tokens_per_chunk),
            elseop=lambda x: x.snippet.to_list(),
            checker=lambda x: x.n_tokens.sum() > start_chunking,
        ),
        sg.cache.String(
            stage_2_cache,
            lambda x: (
                "\n".join(
                    sg.utils.Parallelize(
                        partial(
                            T.paraphrase,
                            model=paraphraser_model,
                            system_prompt=system_prompt,
                            train_of_thought=train_of_thought,
                        )
                    )(x)
                )
            ),
        ),
        lambda x: re.sub("\n+", "\n", x, flags=re.M),
    )

    transformed = transformer(string)

    return transformed


if __name__ == "__main__":
    file_path = pt.Path("./sample2.vtt")
    paraphraser_model = "gpt-3.5-turbo"
    # stage_1_cache = "stage1.parquet"
    # stage_2_cache = "stage2.md"
    stage_1_cache = None
    stage_2_cache = None
    content = extractor(file_path)
    output = load(
        content,
        paraphraser_model=paraphraser_model,
        stage_1_cache=stage_1_cache,
        stage_2_cache=stage_2_cache,
    )

    print(output)
