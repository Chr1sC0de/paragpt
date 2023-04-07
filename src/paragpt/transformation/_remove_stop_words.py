import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)


def remove_stop_words(string: str) -> str:
    stop_words = set(stopwords.words("english"))
    all_words = word_tokenize(string)

    filtered_text = [word for word in all_words if word not in stop_words]
    filtered_text = " ".join(filtered_text)

    filtered_text = re.sub(
        " (uhm|uh|um|ahh|ah) ", "", filtered_text, flags=re.IGNORECASE
    )

    return filtered_text
