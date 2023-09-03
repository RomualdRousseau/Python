import openai

from tree_sitter import Language, Parser

from code import Code

JAVA_LANGUAGE = Language("build/grammar.so", "java")
JAVA_DOC_FRAMEWORK = "JAVADOC"
JAVA_TEST_FRAMEWORK = "JUNIT"

PROMPT_DOCUMENT = f"""
Comment the function below using {JAVA_DOC_FRAMEWORK}.
Include a summary of what the method do and then summarize.
Include also the list of parameters and return value.
Do not put the coments in the method body but only in the {JAVA_DOC_FRAMEWORK} section.
"""

PROMPT_UNIT_TEST = f"""
Generate unit tests for the function below using {JAVA_TEST_FRAMEWORK} framework.
Extract all generated methods and remove everything else.
Do not include the import and class definition.
"""

openai.api_type = "azure"
openai.api_base = "https://openaidafa.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = "a0dfae22426046e99380333303428a4e"

code = Code()
code.load_from_file("data/helloworld.java")

parser = Parser()
parser.set_language(JAVA_LANGUAGE)
tree = parser.parse(lambda _, p: code.get_bytes_at(p))

cursor = tree.walk()

# Go to the class
cursor.goto_first_child()
while cursor.node.type != "class_declaration":
    cursor.goto_next_sibling()
cursor.goto_first_child()
while cursor.node.type != "class_body":
    cursor.goto_next_sibling()

# Go to the first method
cursor.goto_first_child()
while cursor.node.type != "method_declaration":
    cursor.goto_next_sibling()

prompt = "\n".join(
    [
        PROMPT_UNIT_TEST,
        code.get_block_between(
            cursor.node.start_point, cursor.node.end_point, show_line_numbers=False
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
print(response["choices"][0]["message"]["content"])
# print(code.get_block_between(cursor.node.start_point, cursor.node.end_point, show_line_numbers=False))
# print()

# Go to the second method
cursor.goto_next_sibling()
while cursor.node.type != "method_declaration":
    cursor.goto_next_sibling()

prompt = "\n".join(
    [
        PROMPT_UNIT_TEST,
        code.get_block_between(
            cursor.node.start_point, cursor.node.end_point, show_line_numbers=False
        ),
    ]
)
response = openai.ChatCompletion.create(
    engine="gpt_docs",
    messages=[{"role": "user", "content": prompt}],
    temperature=0,
    max_tokens=800,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None,
)
print(response["choices"][0]["message"]["content"])
# print(code.get_block_between(cursor.node.start_point, cursor.node.end_point, show_line_numbers=False))
# print()
