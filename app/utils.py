from typing import Text


def clean_data(text: Text) -> Text:
    return text.replace('"', '&quot;').replace("'", '&quot;')
