import sys
from antlr4 import CommonTokenStream, FileStream
from MIDL.MIDLGrammarRulesLexer import MIDLGrammarRulesLexer
from MIDL.MIDLGrammarRulesParser import MIDLGrammarRulesParser
from MIDLVisitor import MIDLVisitor


def main(argv):
    # 读取文件
    input_stream = FileStream(argv[1] + ".idl")
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
    tree_node, table_node = MIDLVisitor().visit(tree)
    a = tree_node.get_structure()
    b = tree_node.get_AST_with_structure()

    print("==========原始输入==========")
    print(input_stream)
    print("==========符号表内容===========")
    table_node.display()
    print("==========抽象语法树结构===========")
    print(a)
    print("==========抽象语法树内容===========")
    print(b)
    # print("==========代码生成===========")
    # from CppStringTemplate import CppStringTemplate
    #
    # code_make = CppStringTemplate(tree_node, table_node, "test")
    # code_make.display()


if __name__ == '__main__':
    # main(sys.argv)
    test("/home/immortalqx/JetBrainsProjects/PycharmProjects/编译原理实验二/test/case0/test.idl")
