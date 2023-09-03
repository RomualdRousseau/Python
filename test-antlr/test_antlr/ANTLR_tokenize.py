from io import StringIO
from antlr4 import *
from JavaLexer import JavaLexer
from JavaParser import JavaParser
from JavaParserListener import JavaParserListener

class Test(JavaParserListener):
    
    def exitMethodBody(self, ctx):
        
        def recursive(node):
            if node.getChildCount() == 0:
                print(node.getText())
            else:
                for child in node.getChildren():
                    recursive(child)
                    
        recursive(ctx)


code = open('helloworld.java', 'r').read()
codeStream = InputStream(code)
lexer = JavaLexer(codeStream)

stream = CommonTokenStream(lexer)
parser = JavaParser(stream)
parser.addParseListener(Test())
parser.compilationUnit()