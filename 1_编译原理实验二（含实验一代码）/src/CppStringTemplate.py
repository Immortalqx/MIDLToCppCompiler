'''
字符串格式化操作符，需要程序员明确转换类型参数，
比如到底是转成字符串、整数还是其他什么类型。
新式的字符串模板的优势是不用去记住所有相关细节，
而是像shell风格的脚本语言里面那样使用美元符号($).
由于新式的字符串引进Template对象，
Template对象有两个方法：substitute()、safe_substitute()。
substitute()更为严谨，在key缺少的情况下会报一个KeyError的异常。
safe_substitute()在缺少key的情况下，直接原封不动的把字符串显示出来。
'''
# 导入Template对象
from string import Template
from ASTree import TreeNode
from SymbolTable import SymbolTable


class CppStringTemplate():
    START = """
#ifndef ${name}_h
#define ${name}_h

#ifndef rti_me_cpp_hxx
#include "rti_me_cpp.hxx"
#endif

#ifdef NDDS_USER_DLL_EXPORT
#if (defined(RTI_WIN32) || defined(RTI_WINCE))
/* If the code is building on Windows, start exporting symbols. */
#undef NDDSUSERDllExport
#define NDDSUSERDllExport __declspec(dllexport)
#endif
#else
#undef NDDSUSERDllExport
#define NDDSUSERDllExport
#endif
    """

    CODE = """
struct ${classname}Seq;
class ${classname}TypeSupport;
class ${classname}DataWriter;
class ${classname}DataReader;

class ${classname}
{
  public:
    typedef struct ${classname}Seq Seq;
    typedef ${classname}TypeSupport TypeSupport;
    typedef ${classname}DataWriter DataWriter;
    typedef ${classname}DataReader DataReader;

	${CDR_INIT}
};

extern const char *${classname}TYPENAME;

REDA_DEFINE_SEQUENCE_STRUCT(${classname}Seq, ${classname});

REDA_DEFINE_SEQUENCE_IN_C(${classname}Seq, ${classname});

NDDSUSERDllExport extern RTI_BOOL
${classname}_initialize(${classname}* sample)
{
    ${CDR_SENTENCES}
       
    return RTI_TRUE;
}

NDDSUSERDllExport extern RTI_BOOL
${classname}_finalize(${classname}* sample)
{
    UNUSED_ARG(sample);
    return RTI_TRUE;

}

"""
    # 有声明
    CDR_INIT_A = """
CDR_${type} ${ID}=${exp};

"""
    # 无声明
    CDR_INIT_B = """
    CDR_${type} ${ID};

    """

    CDR_SENTENCE = """
CDR_Primitive_init_${type}(&sample->${ID});

"""

    END = """
#ifdef NDDS_USER_DLL_EXPORT
#if (defined(RTI_WIN32) || defined(RTI_WINCE))
/* If the code is building on Windows, stop exporting symbols. */
#undef NDDSUSERDllExport
#define NDDSUSERDllExport
#endif
#endif

#endif
    """

    def __init__(self, node: TreeNode, table: SymbolTable, filename: str):
        # 开始部分,只有一个
        self.start_tmp = Template(CppStringTemplate.START)
        # 代码部分，要注意有可能有多个并列的struct或者module
        self.code_tmp = Template(CppStringTemplate.START)
        # 声明部分A，可能有多个声明
        self.cdr_init_a_tmp = Template(CppStringTemplate.CDR_INIT_A)
        # 声明部分B，可能有多个声明
        self.cdr_init_b_tmp = Template(CppStringTemplate.CDR_INIT_B)
        # 初始化部分，每个声明对应一个初始化
        self.cdr_sentence_tmp = Template(CppStringTemplate.CDR_SENTENCE)
        # 结束部分,也只有一个
        self.end_tmp = Template(CppStringTemplate.END)
        # 最后生成的代码
        self.code_string = ""

        # 生成代码的开头部分
        self.__init_start__(filename)
        # 生成代码的中间部分
        self.__init_code__(node, table)
        # 生成代码的结尾部分
        self.__init_end__()

    def __init_start__(self, filename):
        substitute = self.start_tmp.substitute(name=filename)
        self.code_string += substitute

    # 根据符号表和抽象语法树来进行代码生成
    def __init_code__(self, node: TreeNode, table: SymbolTable):
        # 对于每一个struct或module
        for child in table.children:
            cdr_init_code = ""
            cdr_init_sentence = ""
            for symbol in child.symbols:
                cdr_init_code += self.cdr_init_b_tmp.substitute(type=symbol.type, ID=symbol.id)
                cdr_init_sentence += self.cdr_init_b_tmp.substitute(type=symbol.type, ID=symbol.id)
            self.code_string += self.code_tmp.substitute(classname=child.namespace, CDR_INIT=cdr_init_code,
                                                         CDR_SENTENCE=cdr_init_sentence)
        table.display()
        pass

    def __init_end__(self):
        self.code_string += CppStringTemplate.END

    def display(self):
        print(self.code_string)
