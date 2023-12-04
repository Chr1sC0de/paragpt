from typing import List
import re


def brush_up_vtt(text: str) -> str:
    text = text.replace("WEBVTT", "")
    text = re.sub("^\d+\n", "", text, flags=re.M)
    text = re.sub("\d+:\d+:\d.+?\n", "", text, flags=re.M)
    text = re.sub("\n+", "\n", text, flags=re.M)
    text = text.strip("\n")
    text = text.replace("\n", " ")
    return text


def clean_teams_vtt(text: str) -> List[str]:
    original_text = text
    original_text_len = len(text)
    text = brush_up_vtt(text)
    found = re.findall("<v .+?>.+?</v>", text)
    speaker_text = [re.findall("<v (.+?)>(.+?)</v>", line)[0] for line in found]
    conversation = []
    previous_speaker = None

    for speaker, text in speaker_text:
        if previous_speaker != speaker:
            conversation.append(f"{speaker}: {text}")
        else:
            conversation[-1] += " %s" % text

        previous_speaker = speaker

    if (len(conversation) == 0) and original_text_len > 0:
        conversation = original_text.split("\n\n")

    return conversation
