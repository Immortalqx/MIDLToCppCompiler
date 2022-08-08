from MIDL.MIDLGrammarRulesParser import MIDLGrammarRulesParser
from MIDL.MIDLGrammarRulesVisitor import MIDLGrammarRulesVisitor

from ASTree import *
from SymbolTable import SymbolTable


# This class defines a complete generic visitor for a parse tree produced by MIDLGrammarRulesParser.
class MIDLVisitor(MIDLGrammarRulesVisitor):
    def __init__(self):
        self.ast = None
        self.root_symbol_table = SymbolTable()
        self.current_symbol_table = self.root_symbol_table

    def add_symbol(self, id):
        # 下面必须要转化一下，不然存进去不是字符串，就会出问题
        self.current_symbol_table.add_symbol(str(id))

    # Visit a parse tree produced by MIDLGrammarRulesParser#specification.
    def visitSpecification(self, ctx: MIDLGrammarRulesParser.SpecificationContext):
        self.ast = TreeNode("Specification")
        for definition in ctx.definition():
            # 这里已经取得child了，不能够再visit children!只能够visit！
            self.ast.add_child(self.visit(definition))

        # 后面需要去除
        # print("============显示符号表============")
        # self.current_symbol_table.display()
        return self.ast, self.root_symbol_table

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
        # 添加抽象语法树节点
        module_node = TreeNode("Module")
        node = TreeNode("Terminator module", "module")
        node.add_child(TreeNode("Terminator ID", ctx.ID()))
        # 把module的ID加入当前的符号表
        self.add_symbol(ctx.ID())
        # 遇到module就创建module的作用域
        symbol_table = SymbolTable("module " + str(ctx.ID()))
        self.current_symbol_table.add_child(symbol_table)
        # 进入module的作用域，在里面进行各种操作！
        self.current_symbol_table = symbol_table
        for definition in ctx.definition():
            node.add_child(self.visit(definition))
        module_node.add_child(node)
        # 退出module的作用域，恢复当前的符号表！
        self.current_symbol_table = self.current_symbol_table.parent
        return module_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#type_decl.
    def visitType_decl(self, ctx: MIDLGrammarRulesParser.Type_declContext):
        type_decl_node = TreeNode("Type_decl")
        if ctx.struct_type() is not None:
            type_decl_node.add_child(self.visit(ctx.struct_type()))
        else:
            # 添加抽象语法树的节点
            node = TreeNode("Terminator struct", "struct")
            node.add_child(TreeNode("Terminator ID", ctx.ID()))
            type_decl_node.add_child(node)
            # 添加ID到当前符号表
            self.add_symbol(ctx.ID())
            # 由于这个struct是没有实现的，所以没有作用域，但这里要特殊标记一下！
            symbol_table = SymbolTable("struct " + str(ctx.ID()))
            self.current_symbol_table.add_child(symbol_table)
        return type_decl_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#struct_type.
    def visitStruct_type(self, ctx: MIDLGrammarRulesParser.Struct_typeContext):
        # 添加抽象语法树的节点
        struct_type_node = TreeNode("Struct_type")
        node = TreeNode("Terminator struct", "struct")
        node.add_child(TreeNode("Terminator ID", ctx.ID()))
        # 添加ID到当前的符号表
        self.add_symbol(ctx.ID())
        # 创建新的作用域
        symbol_table = SymbolTable("struct " + str(ctx.ID()))
        self.current_symbol_table.add_child(symbol_table)
        # 进入作用域
        self.current_symbol_table = symbol_table
        node.add_child(self.visit(ctx.member_list()))
        struct_type_node.add_child(node)
        # 退出作用域
        self.current_symbol_table = self.current_symbol_table.parent

        return struct_type_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#member_list.
    def visitMember_list(self, ctx: MIDLGrammarRulesParser.Member_listContext):
        member_list_node = TreeNode("Member_list")
        # FIXME 这里可能是有问题的。
        #  为了符合我设计的抽象语法树，我把declarators加到type_spec最末尾的孩子节点上了。
        # for i in range(len(ctx.type_spec())):
        #     member_list_node.add_child(self.visit(ctx.type_spec()[i]))
        #     member_list_node.add_child(self.visit(ctx.declarators()[i]))
        for i in range(len(ctx.type_spec())):
            type_spec_node = self.visit(ctx.type_spec()[i])
            type_spec_node.add_child(self.visit(ctx.declarators()[i]))
            # type_spec_node.add_end_child(self.visit(ctx.declarators()[i]))
            member_list_node.add_child(type_spec_node)
            type_spec_node.check_type()
        return member_list_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#type_spec.
    def visitType_spec(self, ctx: MIDLGrammarRulesParser.Type_specContext):
        type_spec_node = Type_specNode("Type_spec")
        type_spec_node.add_child(self.visitChildren(ctx))
        type_spec_node.check_type()
        return type_spec_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#scoped_name.
    def visitScoped_name(self, ctx: MIDLGrammarRulesParser.Scoped_nameContext):
        scoped_name_node = TreeNode("Scoped_name")
        # 首先获取文本，并且生成抽象语法树节点
        text = ctx.getText()
        node = TreeNode("Terminator ID", ctx.ID()[0])
        if text.startswith("::"):
            node.add_child(TreeNode("Terminator ::", "::"))
        for i in range(1, len(ctx.ID())):
            dot_node = TreeNode("Terminator ::", "::")
            dot_node.add_child(TreeNode("Terminator ID", ctx.ID()[i]))
            node.add_child(dot_node)
        scoped_name_node.add_child(node)
        # 再从上往下依次判断ID符号是否被定义（开头就“::”的情况我不懂什么意思，暂时没处理！）
        #  由于这里是type类型的，所以不应该插入到符号表中！！！
        self.root_symbol_table.check_namespace(ctx.getText().split("::"), ctx.getText())  # 自顶向下查找一遍
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
        declarators_node = DeclaratorsNode("Declarators")
        for declarator in ctx.declarator():
            declarators_node.add_child(self.visit(declarator))
        declarators_node.check_type()
        return declarators_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#declarator.
    def visitDeclarator(self, ctx: MIDLGrammarRulesParser.DeclaratorContext):
        declarator_node = TreeNode("Declarator")
        declarator_node.add_child(self.visitChildren(ctx))
        return declarator_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#simple_declarator.
    def visitSimple_declarator(self, ctx: MIDLGrammarRulesParser.Simple_declaratorContext):
        simple_declarator_node = Simple_declaratorNode("Simple_declarator")
        node = TreeNode("Terminator ID", ctx.ID())
        self.add_symbol(ctx.ID())
        if ctx.or_expr() is not None:
            equal_node = TreeNode("Terminator =", "=")
            equal_node.add_child(self.visit(ctx.or_expr()))
            node.add_child(equal_node)
        simple_declarator_node.add_child(node)
        simple_declarator_node.check_type()
        return simple_declarator_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#array_declarator.
    def visitArray_declarator(self, ctx: MIDLGrammarRulesParser.Array_declaratorContext):
        array_declarator_node = Array_declaratorNode("Array_declarator")
        node = TreeNode("Terminator ID", ctx.ID())
        self.add_symbol(ctx.ID())
        node.add_child(self.visit(ctx.or_expr()))
        if ctx.exp_list() is not None:
            equal_node = TreeNode("Terminator =", "=")
            equal_node.add_child(self.visit(ctx.exp_list()))
            node.add_child(equal_node)
        array_declarator_node.add_child(node)
        array_declarator_node.check_type()
        return array_declarator_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#exp_list.
    def visitExp_list(self, ctx: MIDLGrammarRulesParser.Exp_listContext):
        exp_list_node = Exp_listNode("Exp_list")
        for or_expr in ctx.or_expr():
            exp_list_node.add_child(self.visit(or_expr))
        exp_list_node.check_type()
        return exp_list_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#or_expr.
    def visitOr_expr(self, ctx: MIDLGrammarRulesParser.Or_exprContext):
        or_expr_node = Or_exprNode("Or_expr")
        node = self.visit(ctx.xor_expr()[0])
        for i in range(1, len(ctx.xor_expr())):
            p_node = TreeNode("Terminator |", "|")
            p_node.add_child(self.visit(ctx.xor_expr()[i]))
            node.add_child(p_node)
        or_expr_node.add_child(node)
        or_expr_node.check_type()
        return or_expr_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#xor_expr.
    def visitXor_expr(self, ctx: MIDLGrammarRulesParser.Xor_exprContext):
        xor_expr_node = Xor_exprNode("Xor_expr")
        node = self.visit(ctx.and_expr()[0])
        for i in range(1, len(ctx.and_expr())):
            p_node = TreeNode("Terminator ^", "^")
            p_node.add_child(self.visit(ctx.and_expr()[i]))
            node.add_child(p_node)
        xor_expr_node.add_child(node)
        xor_expr_node.check_type()
        return xor_expr_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#and_expr.
    def visitAnd_expr(self, ctx: MIDLGrammarRulesParser.And_exprContext):
        and_expr_node = And_exprNode("And_expr")
        node = self.visit(ctx.shift_expr()[0])
        for i in range(1, len(ctx.shift_expr())):
            p_node = TreeNode("Terminator &", "&")
            p_node.add_child(self.visit(ctx.shift_expr()[i]))
            node.add_child(p_node)
        and_expr_node.add_child(node)
        and_expr_node.check_type()
        return and_expr_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#shift_expr.
    def visitShift_expr(self, ctx: MIDLGrammarRulesParser.Shift_exprContext):
        shift_expr_node = Shift_exprNode("Shift_expr")
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
        shift_expr_node.check_type()
        return shift_expr_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#add_expr.
    def visitAdd_expr(self, ctx: MIDLGrammarRulesParser.Add_exprContext):
        add_expr_node = Add_exprNode("Add_expr")
        text = ctx.getText()
        node = self.visit(ctx.mult_expr()[0])
        add_expr_node.add_child(node)
        for i in range(1, len(ctx.mult_expr())):
            if "+" in text:
                p_node = TreeNode("Terminator +", "+")
                p_node.add_child(self.visit(ctx.mult_expr()[i]))
                add_expr_node.add_child(p_node)
                text = text.replace("+", "", 1)
            elif "-" in text:
                p_node = TreeNode("Terminator -", "-")
                p_node.add_child(self.visit(ctx.mult_expr()[i]))
                add_expr_node.add_child(p_node)
                text = text.replace("-", "", 1)
            else:
                add_expr_node.add_child(self.visit(ctx.mult_expr()[i]))
        add_expr_node.check_type()
        return add_expr_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#mult_expr.
    def visitMult_expr(self, ctx: MIDLGrammarRulesParser.Mult_exprContext):
        mult_expr_node = Mult_exprNode("Mult_expr")
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
        mult_expr_node.check_type()
        return mult_expr_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#unary_expr.
    def visitUnary_expr(self, ctx: MIDLGrammarRulesParser.Unary_exprContext):
        unary_expr_node = Unary_exprNode("Unary_expr")
        text = ctx.getText()
        if "-" in text:
            p_node = TreeNode("Terminator -", "-")
            unary_expr_node.add_child(p_node)
            unary_expr_node.add_child(self.visitChildren(ctx))
        elif "+" in text:
            p_node = TreeNode("Terminator +", "+")
            unary_expr_node.add_child(p_node)
            unary_expr_node.add_child(self.visitChildren(ctx))
        elif "~" in text:
            p_node = TreeNode("Terminator ~", "~")
            unary_expr_node.add_child(p_node)
            unary_expr_node.add_child(self.visitChildren(ctx))
        else:
            unary_expr_node.add_child(self.visitChildren(ctx))
        unary_expr_node.check_type()
        return unary_expr_node

    # Visit a parse tree produced by MIDLGrammarRulesParser#literal.
    def visitLiteral(self, ctx: MIDLGrammarRulesParser.LiteralContext):
        # literal_node = TreeNode("Literal")
        # literal_node.add_child(TreeNode("Terminator Literal", ctx.getText()))
        literal_node = LiteralNode("Terminator Literal", ctx.getText())
        literal_node.check_type()
        return literal_node


del MIDLGrammarRulesParser
