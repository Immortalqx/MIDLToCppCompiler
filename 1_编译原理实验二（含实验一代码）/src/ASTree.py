import re
from DType import DType


# 抽象语法树
class TreeNode:
    def __init__(self, type_: str, str_=""):
        self.type_ = type_  # 该节点对应的规则的名称
        self.str_ = str_  # 该节点对应的终结符（如果不是终结符就取""）

        self.level = 0  # 该节点在抽象语法树中的深度
        self.children = []  # 该节点的孩子节点们

        self.dType_ = None

    def add_child(self, child):
        """
        添加孩子节点
        :param child: 孩子节点
        """
        if child is None:
            return
        self.children.append(child)

    def add_end_child(self, child):
        """
        在该节点最底层的孩子节点中添加孩子节点
        这个函数只用于处理member_list-> { type_spec declarators “;” }规则
        :param child:孩子节点
        """
        if child is None:
            return
        if len(self.children) == 0:
            self.add_child(child)
        else:
            self.children[-1].add_end_child(child)

    def set_child_level(self):
        """
        设置每一个孩子节点的深度
        """
        for child in self.children:
            child.level = self.level + 1
            child.set_child_level()

    def get_structure(self):
        """
        获取抽象语法树的结构
        """
        structure = ""
        self.set_child_level()
        for i in range(self.level):
            structure += "\t"
        if self.dType_ is not None:
            structure += str(self.type_) + " " + str(self.dType_) + "\n"
        else:
            structure += str(self.type_) + "\n"
        for child in self.children:
            structure += child.get_structure()
        return structure

    def get_AST(self, last_level=0):
        """
        获取抽象语法树的内容
        """
        AST = ""
        self.set_child_level()
        if self.type_.startswith("Terminator"):
            if self.level > last_level:
                last_level += 1
            elif self.level < last_level:
                last_level -= 1
            for i in range(last_level + 1):
                AST += "\t"
            AST += str(self.str_) + "\n"
        for child in self.children:
            AST += child.get_AST(last_level)
        return AST

    def get_AST_with_structure(self, last_level=0):
        """
        获取抽象语法树的内容
        """
        AST = ""
        self.set_child_level()
        if self.type_.startswith("Terminator"):
            AST += str(self.type_.split(" ")[1]) + " " + str(self.str_) + "\n"
        for child in self.children:
            AST += child.get_AST_with_structure(last_level)
        return AST


# 定义一系列的类型检查相关的类
class LiteralNode(TreeNode):
    def __init__(self, type_: str, str_=""):
        super().__init__(type_, str_)

        self.dType_ = None

    def check_type(self):
        BOOLEAN = "TRUE|true|FALSE|false$"
        INTEGER = "(0|[1-9][0-9]*)[l|L]?$"
        FLOATING_PT = "[0-9]+.[0-9]*$|.[0-9]+$"
        str_ = self.str_
        if re.match(INTEGER, str_):
            self.dType_ = DType.UINT64  # 默认整数是int64类型的
        elif re.match(FLOATING_PT, str_):
            self.dType_ = DType.FLOAT  # 默认的浮点数是float类型的
        elif len(str_) == 3:
            self.dType_ = DType.CHAR  # char
        elif re.match(BOOLEAN, str_):
            self.dType_ = DType.BOOLEAN  # boolean
        else:
            self.dType_ = DType.STRING  # string

    # def check_type(self):
    #     BOOLEAN = "TRUE|true|FALSE|false$"
    #     STRING = "([\\(b|t|n|f|r|\"|\'|\\)]|(^\\|^\"))*$"
    #     CHAR = "([\\(b|t|n|f|r|\"|\'|\\)]|(^\\|^\'))*$"
    #     INTEGER = "(0|[1-9][0-9]*)[l|L]?$"
    #     FLOATING_PT = "[0-9]+.[0-9]*[[e|E][+|-]?[0-9]+]?[f|F|d|D]?" \
    #                   "|.[0-9]+[[e|E][+|-]?[0-9]+]?[f|F|d|D]?" \
    #                   "|[0-9]+[[e|E][+|-]?[0-9]+][f|F|d|D]?" \
    #                   "|[0-9]+[[e|E][+|-]?[0-9]+]?[f|F|d|D]"
    #
    #     if re.match(BOOLEAN, self.str_):
    #         self.dType_ = "BOOLEAN"
    #     elif re.match(INTEGER, self.str_):
    #         self.dType_ = "INTEGER"
    #     elif re.match(FLOATING_PT, self.str_):
    #         self.dType_ = "FLOATING_PT"
    #     elif re.match(CHAR, self.str_):
    #         self.dType_ = "CHAR"
    #     elif re.match(STRING, self.str_):
    #         self.dType_ = "STRING"


class Unary_exprNode(TreeNode):
    def __init__(self, type_: str, str_=""):
        super().__init__(type_, str_)

        self.dType_ = None

    def check_type(self):
        if len(self.children) == 1:  # 没有符号就保持一致
            self.dType_ = self.children[0].dType_
        else:  # 考虑正确性以及是否转成signed类型
            dType_ = self.children[1].dType_
            if self.children[0].str_ == "~":  # 单独处理~运算
                if DType.is_BOOLEAN(dType_):  # bool类型支持运算
                    self.dType_ = DType.BOOLEAN
                else:
                    print(self.children[1].str_)
                    print("错误：" + dType_ + "类型不支持~运算！")
                    exit(-1)
            # 对于+、-运算
            elif DType.is_text(dType_) or DType.is_BOOLEAN(dType_):  # CHAR、STRING、BOOLEAN都不支持这种运算
                print(self.children[1].str_)
                print(dType_ + "类型不支持-、+运算！")
                exit(-1)
            elif self.children[0].str_ == "-" and DType.is_unsigned_int(dType_):  # 如果-遇上了无符号数
                self.dType_ = DType.to_signed_int(dType_)
            else:  # 其他情况都应该是和子节点一致的类型！
                self.dType_ = dType_
        # if self.str_.startswith("-"):  # 只有-号才能够实际的改变类型为SIGNED！
        #     if self.children[1].dType_ == "FLOATING_PT":
        #         self.dType_ = "SIGNED_" + "FLOATING_PT"
        #     elif self.children[1].dType_ != "STRING":
        #         self.dType_ = "SIGNED_" + "INTEGER"
        # else:
        #     self.dType_ = self.children[0].dType_  # 没有+-~，那么0就是literal


class Mult_exprNode(TreeNode):
    def __init__(self, type_: str, str_=""):
        super().__init__(type_, str_)

        self.dType_ = None

    def check_type(self):
        if len(self.children) == 1:
            self.dType_ = self.children[0].dType_
        else:
            for child in self.children:
                if child.dType_ == DType.STRING:
                    print(child.str_)
                    print("错误：STRING类型不支持*、/、%运算！")
                    exit(-1)
                elif child.dType_ == DType.CHAR or child.dType_ == DType.BOOLEAN:
                    print("警告：" + child.dType_ + "类型被用于*、/、%运算！")
                    if self.dType_ is None:
                        self.dType_ = DType.UINT8
                elif DType.is_float_pt(child.dType_):  # 只要是有浮点数类型参与运算就是浮点数类型！
                    self.dType_ = child.dType_
                elif DType.is_signed_int(child.dType_):
                    self.dType_ = child.dType_
                # 此时只剩下无符号整形
                if not DType.is_float_pt(self.dType_) and not DType.is_signed_int(self.dType_):
                    # TODO 这里似乎需要更细致的处理
                    self.dType_ = child.dType_


class Add_exprNode(TreeNode):
    def __init__(self, type_: str, str_=""):
        super().__init__(type_, str_)

        self.dType_ = None

    def check_type(self):
        if len(self.children) == 1:
            self.dType_ = self.children[0].dType_
        else:
            for i in range(0, len(self.children)):
                child = self.children[i].children[0]
                if child.dType_ == DType.STRING:
                    print(child.str_)
                    print("错误：STRING类型不支持+、-运算！")
                    exit(-1)
                elif child.dType_ == DType.CHAR or child.dType_ == DType.BOOLEAN:
                    print("警告：" + child.dType_ + "类型被用于+、-运算！")
                    if self.dType_ is None:
                        self.dType_ = DType.UINT8
                elif DType.is_float_pt(child.dType_):  # 只要是有浮点数类型参与运算就是浮点数类型！
                    self.dType_ = child.dType_
                elif DType.is_signed_int(child.dType_):
                    self.dType_ = child.dType_
                # 此时只剩下无符号整形
                if not DType.is_float_pt(self.dType_) and not DType.is_signed_int(self.dType_):
                    # TODO 这里似乎需要更细致的处理
                    self.dType_ = child.dType_


class Shift_exprNode(TreeNode):
    def __init__(self, type_: str, str_=""):
        super().__init__(type_, str_)

        self.dType_ = None

    def check_type(self):
        if len(self.children) == 1:
            self.dType_ = self.children[0].dType_
        else:
            for child in self.children:
                if child.dType_ == DType.STRING or DType.is_float_pt(child.dType_):
                    print(child.str_)
                    print("错误：" + child.dType_ + "类型不支持>>或<<运算！")
                    exit(-1)
                elif child.dType_ == DType.CHAR or child.dType_ == DType.BOOLEAN:
                    print("警告：" + child.dType_ + "类型被用于>>或<<运算！")
                    if self.dType_ is None:
                        self.dType_ = DType.UINT8
                elif DType.is_signed_int(child.dType_):
                    self.dType_ = child.dType_
                # 此时只剩下无符号整形
                if not DType.is_signed_int(self.dType_):
                    # TODO 这里似乎需要更细致的处理
                    self.dType_ = child.dType_


class And_exprNode(TreeNode):
    def __init__(self, type_: str, str_=""):
        super().__init__(type_, str_)

        self.dType_ = None

    def check_type(self):
        if len(self.children) == 1:
            self.dType_ = self.children[0].dType_
        else:
            for child in self.children:
                if child.dType_ == DType.STRING or DType.is_float_pt(child.dType_) or DType.is_signed_int(child.dType_):
                    print(child.str_)
                    print("错误：" + child.dType_ + "类型不支持&运算！")
                    exit(-1)
                elif child.dType_ == DType.CHAR or child.dType_ == DType.BOOLEAN:
                    print("警告：" + child.dType_ + "类型被用于&运算！")
                    if self.dType_ is None:
                        self.dType_ = DType.UINT8
                elif DType.is_unsigned_int(child.dType_):
                    self.dType_ = child.dType_
                elif child.dType_ == self.dType_:
                    continue


class Xor_exprNode(TreeNode):
    def __init__(self, type_: str, str_=""):
        super().__init__(type_, str_)

        self.dType_ = None

    def check_type(self):
        if len(self.children) == 1:
            self.dType_ = self.children[0].dType_
        else:
            for child in self.children:
                if child.dType_ == DType.STRING or DType.is_float_pt(child.dType_) or DType.is_signed_int(child.dType_):
                    print(child.str_)
                    print("错误：" + child.dType_ + "类型不支持^运算！")
                    exit(-1)
                elif child.dType_ == DType.CHAR or child.dType_ == DType.BOOLEAN:
                    print("警告：" + child.dType_ + "类型被用于^运算！")
                    if self.dType_ is None:
                        self.dType_ = DType.UINT8
                elif DType.is_unsigned_int(child.dType_):
                    self.dType_ = child.dType_
                elif child.dType_ == self.dType_:
                    continue


class Or_exprNode(TreeNode):
    def __init__(self, type_: str, str_=""):
        super().__init__(type_, str_)

        self.dType_ = None

    def check_type(self):
        if len(self.children) == 1:
            self.dType_ = self.children[0].dType_
        else:
            for child in self.children:
                if child.dType_ == DType.STRING or DType.is_float_pt(child.dType_) or DType.is_signed_int(child.dType_):
                    print(child.str_)
                    print("错误：" + child.dType_ + "类型不支持|运算！")
                    exit(-1)
                elif child.dType_ == DType.CHAR or child.dType_ == DType.BOOLEAN:
                    print("警告：" + child.dType_ + "类型被用于|运算！")
                    if self.dType_ is None:
                        self.dType_ = DType.UINT8
                elif DType.is_unsigned_int(child.dType_):
                    self.dType_ = child.dType_
                elif child.dType_ == self.dType_:
                    continue


class Exp_listNode(TreeNode):
    def __init__(self, type_: str, str_=""):
        super().__init__(type_, str_)

        self.dType_ = None

    def check_type(self):
        if len(self.children) == 1:  # 只有一个or_expr，那么就不是数组类型
            self.dType_ = self.children[0].dType_
        else:  # 否则就是多个or_exper，导致是数组类型
            temp = None  # 一个临时变量
            for child in self.children:
                if temp is None:
                    temp = child.dType_
                else:
                    if temp != child.dType_:
                        print("数组类型不统一")
                        exit(-1)
            self.dType_ = temp


class Array_declaratorNode(TreeNode):
    def __init__(self, type_: str, str_=""):
        super().__init__(type_, str_)
        self.dType_ = None

    def check_type(self):
        # 找到ID节点：
        node = self.children[0]
        # 首先，检查下标
        dType_ = node.children[0].dType_
        if DType.is_float_pt(dType_):
            print(node.children[0].str_)
            print("错误：" + dType_ + "类型不可以做索引！")
            exit(-1)
        elif dType_ == DType.CHAR or dType_ == DType.BOOLEAN:
            print("警告：" + dType_ + "类型被用作索引！")
        elif dType_ == DType.STRING:
            print(node.children[0].str_)
            print("错误：STRING类型不可以做索引！")
            exit(-1)
        elif DType.is_signed_int(dType_):
            print(node.children[0].str_)
            print("错误：下标不可以为负数！")
            exit(-1)

        if len(node.children) == 1:
            return
            # 获取数组的长度
        temp = node
        while len(temp.children) != 0:
            temp = temp.children[0]
        array_len = int(temp.str_)
        # 如果有赋值，给类型赋值，否则不复制，后续程序会忽略None类型
        node = node.children[1]  # 目前是等号节点
        node = node.children[0]  # 目前是Exp_list节点
        exp_len = len(node.children)
        if exp_len > 1:  # 如果有多个孩子节点
            if exp_len > array_len:
                print("错误：数组长度超过定义的长度！")
                exit(-1)
            elif exp_len < array_len:
                print("警告：数组长度小于定义的长度！")


class Simple_declaratorNode(TreeNode):
    def __init__(self, type_: str, str_=""):
        super().__init__(type_, str_)

        self.dType_ = None

    def check_type(self):
        # 找到ID节点
        node = self.children[0]
        if len(node.children) == 1:
            self.dType_ = node.children[0].children[0].dType_  # ID->=->or_expr


class DeclaratorsNode(TreeNode):
    def __init__(self, type_: str, str_=""):
        super().__init__(type_, str_)
        self.dType_ = None

    def check_type(self):
        # 对于只有一个变量被声明的情况：
        # 找到Simple_declarator节点
        if len(self.children) == 1:
            node = self.children[0]
            while node.dType_ is None and len(node.children) > 0:
                node = node.children[0]
            self.dType_ = node.dType_


class Type_specNode(TreeNode):
    def __init__(self, type_: str, str_=""):
        super().__init__(type_, str_)
        self.dType_ = None

    def check_type(self):
        # 找到自己应当支持的类型
        node = self.children[0]
        while len(node.children) != 0:
            node = node.children[0]

        spec_type = node.str_
        self.dType_ = spec_type

        if len(self.children) != 2:
            return

        declarator_type = self.children[1].dType_
        if spec_type == declarator_type:  # CHAR/STRING/BOOLEAN，以及其他情况
            return
        elif DType.is_signed_int(spec_type):
            if DType.is_signed_int(declarator_type) or DType.is_unsigned_int(declarator_type):
                return
        elif DType.is_unsigned_int(spec_type):
            if DType.is_unsigned_int(declarator_type):
                return
        elif DType.is_float_pt(spec_type):
            if DType.is_float_pt(declarator_type) or DType.is_signed_int(declarator_type) or DType.is_unsigned_int(
                    declarator_type):
                return
        if declarator_type is None:  # 这说明没有进行赋值操作！那肯定是可以的！！！
            return
        print("错误：不支持" + declarator_type + "类型到" + spec_type + "类型的转换！")
        exit(-1)
