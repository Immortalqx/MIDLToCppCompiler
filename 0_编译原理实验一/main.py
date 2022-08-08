import sys
from antlr4 import CommonTokenStream, FileStream
from MIDL.MIDLGrammarRulesLexer import MIDLGrammarRulesLexer
from MIDL.MIDLGrammarRulesParser import MIDLGrammarRulesParser
from src.MIDLVisitor import MIDLVisitor


def main(argv):
    # 读取文件
    input_stream = FileStream(argv[1] + ".in")
    # 将输入文件交给词法分析器
    lexer = MIDLGrammarRulesLexer(input_stream)
    # 将词法分析器传递给token生成一个个单词
    tokens = CommonTokenStream(lexer)
    # 将单词传递给语法分析器
    parser = MIDLGrammarRulesParser(tokens)
    # 调用specification语法生成AST
    tree = parser.specification()
    # 调用visitor遍历生成的AST
    tree_node = MIDLVisitor().visit(tree)
    # 保存到SyntaxOut.txt中
    # file = open("SyntaxOut.txt", 'w')
    file = open(argv[1] + ".ast", 'w')
    file.write("====================抽象语法树的结构====================\n")
    file.write(tree_node.get_structure())
    file.write("====================抽象语法树的内容====================\n")
    file.write(tree_node.get_AST())
    file.close()


def test(filename):
    # 读取文件
    input_stream = FileStream(filename)
    # 将输入文件交给词法分析器
    lexer = MIDLGrammarRulesLexer(input_stream)
    # 将词法分析器传递给token生成一个个单词
    tokens = CommonTokenStream(lexer)
    # 将单词传递给语法分析器
    parser = MIDLGrammarRulesParser(tokens)
    # 调用specification语法生成AST
    tree = parser.specification()
    # 调用visitor遍历生成的AST
    tree_node = MIDLVisitor().visit(tree)
    a = tree_node.get_structure()
    b = tree_node.get_AST()
    print(a)
    print(b)


if __name__ == '__main__':
    main(sys.argv)
