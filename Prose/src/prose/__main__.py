import re

from prose.llm.llm import LLM
from prose.domain.file import File
from prose.dao.file_repository import FileRepository
from prose.parser.code import Code
from prose.parser.parser_java import ParserJava

file_repo = FileRepository()

if __name__ == "__main__":
    file = File("helloworld.java", "data/helloworld.java")

    code = Code()
    code.load(file.path)

    parser = ParserJava()
    parser.parse(code, file)

    llm = LLM()
    for method in file.methods:
        print(method)
        llm.commentify(code, method)
        llm.testify(code, method, filter=lambda s: re.sub(r"```.*\n?", "", s))

    file_repo.upsert(file)
    file_repo.save("prose.json")
