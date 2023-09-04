from typing import Callable

import openai

from prose.parser.code import Code
from prose.domain.method import Method
from prose.parser.parser_java import JAVA_DOC_FRAMEWORK, JAVA_TEST_FRAMEWORK

PROMPT_DOCUMENT = f"""
Comment the function below using {JAVA_DOC_FRAMEWORK}.
Include a summary of what the method do and then summarize.
Include also the list of parameters and return value.
Do not put the coments in the method body but only in the {JAVA_DOC_FRAMEWORK} section.
Do not input the function body in the response.
"""

PROMPT_UNIT_TEST = f"""
Generate unit tests for the function below using {JAVA_TEST_FRAMEWORK} framework.
Extract all generated methods and remove everything else.
Do not include the import and class definition.
"""

class LLM:
    def __init__(self):
        openai.api_type = "azure"
        openai.api_base = "https://openaidafa.openai.azure.com/"
        openai.api_version = "2023-07-01-preview"
        openai.api_key = "a0dfae22426046e99380333303428a4e"

    def commentify(self, code: Code, method: Method, filter:Callable[[str], str] | None=None) -> None:
        prompt = "\n".join(
            [
                PROMPT_DOCUMENT,
                code.get_block_between(
                    method.start_point, method.end_point, show_line_numbers=False
                ),
            ]
        )
        response = openai.ChatCompletion.create(
            engine="chat_gpt",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
        )
        content = response["choices"][0]["message"]["content"]
        if filter is not None:
            content = filter(content)
        method.comment = content.splitlines()

    def testify(self, code: Code, method: Method, filter:Callable[[str], str] | None=None) -> None:
        prompt = "\n".join(
            [
                PROMPT_UNIT_TEST,
                code.get_block_between(
                    method.start_point, method.end_point, show_line_numbers=False
                ),
            ]
        )
        response = openai.ChatCompletion.create(
            engine="chat_gpt",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=800,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
        )
        content = response["choices"][0]["message"]["content"]
        if filter is not None:
            content = filter(content)
        method.test = content.splitlines()
