from MIDL.MIDLGrammarRulesParser import MIDLGrammarRulesParser
from MIDL.MIDLGrammarRulesVisitor import MIDLGrammarRulesVisitor


class TreeNode:
    def __init__(self, type_: str, str_=""):
        self.type_ = type_  # 该节点对应的规则的名称
        self.str_ = str_  # 该节点对应的终结符（如果不是终结符就取""）

        self.level = 0  # 该节点在抽象语法树中的深度
        self.child = []  # 该节点的孩子节点们

    def add_child(self, child):
        """
        添加孩子节点
        :param child: 孩子节点
        """
        if child is None:
            return
        self.child.append(child)

    def add_end_child(self, child):
        """
        在该节点最底层的孩子节点中添加孩子节点
        这个函数只用于处理member_list-> { type_spec declarators “;” }规则
        :param child:孩子节点
        """
        if child is None:
            return
        if len(self.child) == 0:
            self.add_child(child)
        else:
            self.child[-1].add_end_child(child)

    def set_child_level(self):
        """
        设置每一个孩子节点的深度
        """
        for child in self.child:
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
        structure += str(self.type_) + "\n"
        for child in self.child:
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
                AST += "  "
            AST += str(self.str_) + "\n"
        for child in self.child:
            AST += child.get_AST(last_level)
        return AST


# This class defines a complete generic visitor for a parse tree produced by MIDLGrammarRulesParser.
class MIDLVisitor(MIDLGrammarRulesVisitor):
    def __init__(self):
        self.ast = None

    def display(self):
        self.ast.display()

    # Visit a parse tree produced by MIDLGrammarRulesParser#specification.
    def visitSpecification(self, ctx: MIDLGrammarRulesParser.SpecificationContext):
        self.ast = TreeNode("Specification")
        for definition in ctx.definition():
            # 这里已经取得child了，不能够再visit child!只能够visit！
            self.ast.add_child(self.visit(definition))
        return self.ast

    # Visit a parse tree produced by MIDLGrammarRulesParser#definition.
    def visitDefinition(self, ctx: MIDLGrammarRulesParser.DefinitionContext):
        definition_node = TreeNode("Definition")
        # 不是很理解为什么这里要这么指定！！！
        if ctx.type_decl() is not None:
            definition_node.add_child(self.visit(ctx.type_decl()))
        elif ctx.module() is not None:
            definition_node.add_child(self.visit(ctx.module()))
        return definition_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#module.
    def visitModule(self, ctx: MIDLGrammarRulesParser.ModuleContext):
        module_node = TreeNode("Module")
        node = TreeNode("Terminator module", "module")
        node.add_child(TreeNode("Terminator ID", ctx.ID()))
        for definition in ctx.definition():
            node.add_child(self.visit(definition))
        module_node.add_child(node)
        return module_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#type_decl.
    def visitType_decl(self, ctx: MIDLGrammarRulesParser.Type_declContext):
        type_decl_node = TreeNode("Type_decl")
        if ctx.struct_type() is not None:
            type_decl_node.add_child(self.visit(ctx.struct_type()))
        else:
            node = TreeNode("Terminator struct", "struct")
            node.add_child(TreeNode("Terminator ID", ctx.ID()))
            type_decl_node.add_child(node)
        return type_decl_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#struct_type.
    def visitStruct_type(self, ctx: MIDLGrammarRulesParser.Struct_typeContext):
        struct_type_node = TreeNode("Struct_type")
        node = TreeNode("Terminator struct", "struct")
        node.add_child(TreeNode("Terminator ID", ctx.ID()))
        node.add_child(self.visit(ctx.member_list()))
        struct_type_node.add_child(node)
        return struct_type_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#member_list.
    def visitMember_list(self, ctx: MIDLGrammarRulesParser.Member_listContext):
        member_list_node = TreeNode("Member_list")
        # TODO 最后的问题可能就在这里了！！！
        # FIXME 这里必然有问题，要修改！！！type_spec与declarators不知道怎么弄
        #  目前只是一前一后的顺序做出来的
        # for i in range(len(ctx.type_spec())):
        #     member_list_node.add_child(self.visit(ctx.type_spec()[i]))
        #     member_list_node.add_child(self.visit(ctx.declarators()[i]))
        for i in range(len(ctx.type_spec())):
            type_spec_node = self.visit(ctx.type_spec()[i])
            type_spec_node.add_end_child(self.visit(ctx.declarators()[i]))
            member_list_node.add_child(type_spec_node)
        return member_list_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#type_spec.
    def visitType_spec(self, ctx: MIDLGrammarRulesParser.Type_specContext):
        type_spec_node = TreeNode("Type_spec")
        type_spec_node.add_child(self.visitChildren(ctx))
        return type_spec_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#scoped_name.
    def visitScoped_name(self, ctx: MIDLGrammarRulesParser.Scoped_nameContext):
        scoped_name_node = TreeNode("Scoped_name")
        # TODO 怎么把"::"加回来！！！
        # FIXME 这里应该是有问题的！
        #  这里暂时是把“::”省略了
        # for id in ctx.ID():
        #     scoped_name_node.add_child(TreeNode("Terminator ID", id))
        # scoped_name_node.add_child(self.visitChildren(ctx))
        text = ctx.getText()
        node = TreeNode("Terminator ID", ctx.ID()[0])
        if text.startswith("::"):
            node.add_child(TreeNode("Terminator ::", "::"))
        for i in range(1, len(ctx.ID())):
            dot_node = TreeNode("Terminator ::", "::")
            dot_node.add_child(TreeNode("Terminator ID", ctx.ID()[i]))
            node.add_child(dot_node)
        scoped_name_node.add_child(node)
        return scoped_name_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#base_type_spec.
    def visitBase_type_spec(self, ctx: MIDLGrammarRulesParser.Base_type_specContext):
        base_type_spec_node = TreeNode("Base_type_spec")
        if ctx.floating_pt_type() is not None:
            base_type_spec_node.add_child(self.visit(ctx.floating_pt_type()))
        elif ctx.integer_type() is not None:
            base_type_spec_node.add_child(self.visit(ctx.integer_type()))
        else:
            base_type_spec_node.add_child(TreeNode("Terminator " + ctx.getText(), ctx.getText()))
        return base_type_spec_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#floating_pt_type.
    def visitFloating_pt_type(self, ctx: MIDLGrammarRulesParser.Floating_pt_typeContext):
        floating_pt_type_node = TreeNode("Floating_pt_type")
        floating_pt_type_node.add_child(TreeNode("Terminator " + ctx.getText(), ctx.getText()))
        return floating_pt_type_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#integer_type.
    def visitInteger_type(self, ctx: MIDLGrammarRulesParser.Integer_typeContext):
        integer_type_node = TreeNode("Integer_type")
        integer_type_node.add_child(self.visitChildren(ctx))
        return integer_type_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#signed_int.
    def visitSigned_int(self, ctx: MIDLGrammarRulesParser.Signed_intContext):
        signed_int_node = TreeNode("Signed_int")
        signed_int_node.add_child(TreeNode("Terminator " + ctx.getText(), ctx.getText()))
        return signed_int_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#unsigned_int.
    def visitUnsigned_int(self, ctx: MIDLGrammarRulesParser.Unsigned_intContext):
        unsigned_int_node = TreeNode("Unsigned_int")
        unsigned_int_node.add_child(TreeNode("Terminator " + ctx.getText(), ctx.getText()))
        return unsigned_int_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#declarators.
    def visitDeclarators(self, ctx: MIDLGrammarRulesParser.DeclaratorsContext):
        declarators_node = TreeNode("Declarators")
        for declarator in ctx.declarator():
            declarators_node.add_child(self.visit(declarator))
        return declarators_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#declarator.
    def visitDeclarator(self, ctx: MIDLGrammarRulesParser.DeclaratorContext):
        declarator_node = TreeNode("Declarator")
        declarator_node.add_child(self.visitChildren(ctx))
        return declarator_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#simple_declarator.
    def visitSimple_declarator(self, ctx: MIDLGrammarRulesParser.Simple_declaratorContext):
        simple_declarator_node = TreeNode("Simple_declarator")
        node = TreeNode("Terminator ID", ctx.ID())
        if ctx.or_expr() is not None:
            equal_node = TreeNode("Terminator =", "=")
            equal_node.add_child(self.visit(ctx.or_expr()))
            node.add_child(equal_node)
        simple_declarator_node.add_child(node)
        return simple_declarator_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#array_declarator.
    def visitArray_declarator(self, ctx: MIDLGrammarRulesParser.Array_declaratorContext):
        array_declarator_node = TreeNode("Array_declarator")
        node = TreeNode("Terminator ID", ctx.ID())
        node.add_child(self.visit(ctx.or_expr()))
        if ctx.exp_list() is not None:
            equal_node = TreeNode("Terminator =", "=")
            equal_node.add_child(self.visit(ctx.exp_list()))
            node.add_child(equal_node)
        array_declarator_node.add_child(node)
        return array_declarator_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#exp_list.
    def visitExp_list(self, ctx: MIDLGrammarRulesParser.Exp_listContext):
        exp_list_node = TreeNode("Exp_list")
        # FIXME 是否要括号和逗号？？？
        #  目前还是不加，感觉没必要
        for or_expr in ctx.or_expr():
            exp_list_node.add_child(self.visit(or_expr))
        return exp_list_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#or_expr.
    def visitOr_expr(self, ctx: MIDLGrammarRulesParser.Or_exprContext):
        or_expr_node = TreeNode("Or_expr")
        # FIXME 是否要“|”，怎么加进去。这种类似的好像最不好处理？？？？
        #  也不能够写成两种结构，这是写不出来的！
        node = self.visit(ctx.xor_expr()[0])
        for i in range(1, len(ctx.xor_expr())):
            p_node = TreeNode("Terminator |", "|")
            p_node.add_child(self.visit(ctx.xor_expr()[i]))
            node.add_child(p_node)
        or_expr_node.add_child(node)
        return or_expr_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#xor_expr.
    def visitXor_expr(self, ctx: MIDLGrammarRulesParser.Xor_exprContext):
        xor_expr_node = TreeNode("Xor_expr")
        # FIXME 是否要“^”，怎么加进去
        # for and_expr in ctx.and_expr():
        #     xor_expr_node.add_child(self.visit(and_expr))
        node = self.visit(ctx.and_expr()[0])
        for i in range(1, len(ctx.and_expr())):
            p_node = TreeNode("Terminator ^", "^")
            p_node.add_child(self.visit(ctx.and_expr()[i]))
            node.add_child(p_node)
        xor_expr_node.add_child(node)
        return xor_expr_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#and_expr.
    def visitAnd_expr(self, ctx: MIDLGrammarRulesParser.And_exprContext):
        and_expr_node = TreeNode("And_expr")
        # FIXME 是否要“&”，怎么加进去
        # for shift_expr in ctx.shift_expr():
        #     and_expr_node.add_child(self.visit(shift_expr))
        node = self.visit(ctx.shift_expr()[0])
        for i in range(1, len(ctx.shift_expr())):
            p_node = TreeNode("Terminator &", "&")
            p_node.add_child(self.visit(ctx.shift_expr()[i]))
            node.add_child(p_node)
        and_expr_node.add_child(node)
        return and_expr_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#shift_expr.
    def visitShift_expr(self, ctx: MIDLGrammarRulesParser.Shift_exprContext):
        shift_expr_node = TreeNode("Shift_expr")
        # TODO !!!!!!这样是可行的吗？？？
        # FIXME 是否要“>>”或“<<”，怎么加进去
        text = ctx.getText()
        node = self.visit(ctx.add_expr()[0])
        for i in range(1, len(ctx.add_expr())):
            if "<<" in text:
                p_node = TreeNode("Terminator <<", "<<")
                p_node.add_child(self.visit(ctx.add_expr()[i]))
                node.add_child(p_node)
                text = text.replace("<<", "", 1)
            elif ">>" in text:
                p_node = TreeNode("Terminator >>", ">>")
                p_node.add_child(self.visit(ctx.add_expr()[i]))
                node.add_child(p_node)
                text = text.replace(">>", "", 1)
            else:
                node.add_child(self.visit(ctx.add_expr()[i]))
        shift_expr_node.add_child(node)
        return shift_expr_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#add_expr.
    def visitAdd_expr(self, ctx: MIDLGrammarRulesParser.Add_exprContext):
        add_expr_node = TreeNode("Add_expr")
        # FIXME 是否要“+”或“-”，怎么加进去
        text = ctx.getText()
        node = self.visit(ctx.mult_expr()[0])
        for i in range(1, len(ctx.mult_expr())):
            if "+" in text:
                p_node = TreeNode("Terminator +", "+")
                p_node.add_child(self.visit(ctx.mult_expr()[i]))
                node.add_child(p_node)
                text = text.replace("+", "", 1)
            elif "-" in text:
                p_node = TreeNode("Terminator -", "-")
                p_node.add_child(self.visit(ctx.mult_expr()[i]))
                node.add_child(p_node)
                text = text.replace("-", "", 1)
            else:
                node.add_child(self.visit(ctx.mult_expr()[i]))
        add_expr_node.add_child(node)
        return add_expr_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#mult_expr.
    def visitMult_expr(self, ctx: MIDLGrammarRulesParser.Mult_exprContext):
        mult_expr_node = TreeNode("Mult_expr")
        # FIXME 是否要“*”或“/”或“%”，怎么加进去
        text = ctx.getText()
        node = self.visit(ctx.unary_expr()[0])
        for i in range(1, len(ctx.unary_expr())):
            if "*" in text:
                p_node = TreeNode("Terminator *", "*")
                p_node.add_child(self.visit(ctx.unary_expr()[i]))
                node.add_child(p_node)
                text = text.replace("*", "", 1)
            elif "/" in text:
                p_node = TreeNode("Terminator /", "/")
                p_node.add_child(self.visit(ctx.unary_expr()[i]))
                node.add_child(p_node)
                text = text.replace("/", "", 1)
            elif "%" in text:
                p_node = TreeNode("Terminator %", "%")
                p_node.add_child(self.visit(ctx.unary_expr()[i]))
                node.add_child(p_node)
                text = text.replace("%", "", 1)
            else:
                node.add_child(self.visit(ctx.unary_expr()[i]))
        mult_expr_node.add_child(node)
        return mult_expr_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#unary_expr.
    def visitUnary_expr(self, ctx: MIDLGrammarRulesParser.Unary_exprContext):
        unary_expr_node = TreeNode("Unary_expr")
        # FIXME 这里需要把[“-”| “+” | “~”]写进去
        text = ctx.getText()
        if "-" in text:
            p_node = TreeNode("Terminator -", "-")
            p_node.add_child(self.visitChildren(ctx))
            unary_expr_node.add_child(p_node)
        elif "+" in text:
            p_node = TreeNode("Terminator +", "+")
            p_node.add_child(self.visitChildren(ctx))
            unary_expr_node.add_child(p_node)
        elif "~" in text:
            p_node = TreeNode("Terminator ~", "~")
            p_node.add_child(self.visitChildren(ctx))
            unary_expr_node.add_child(p_node)
        else:
            unary_expr_node.add_child(self.visitChildren(ctx))
        return unary_expr_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#literal.
    def visitLiteral(self, ctx: MIDLGrammarRulesParser.LiteralContext):
        literal_node = TreeNode("Literal")
        literal_node.add_child(TreeNode("Terminator Literal", ctx.getText()))
        return literal_node


del MIDLGrammarRulesParser
