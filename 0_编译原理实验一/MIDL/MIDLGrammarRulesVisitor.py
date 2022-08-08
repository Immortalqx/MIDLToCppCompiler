# Generated from MIDLGrammarRules.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MIDLGrammarRulesParser import MIDLGrammarRulesParser
else:
    from MIDLGrammarRulesParser import MIDLGrammarRulesParser

# This class defines a complete generic visitor for a parse tree produced by MIDLGrammarRulesParser.

class MIDLGrammarRulesVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MIDLGrammarRulesParser#specification.
    def visitSpecification(self, ctx:MIDLGrammarRulesParser.SpecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#definition.
    def visitDefinition(self, ctx:MIDLGrammarRulesParser.DefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#module.
    def visitModule(self, ctx:MIDLGrammarRulesParser.ModuleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#type_decl.
    def visitType_decl(self, ctx:MIDLGrammarRulesParser.Type_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#struct_type.
    def visitStruct_type(self, ctx:MIDLGrammarRulesParser.Struct_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#member_list.
    def visitMember_list(self, ctx:MIDLGrammarRulesParser.Member_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#type_spec.
    def visitType_spec(self, ctx:MIDLGrammarRulesParser.Type_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#scoped_name.
    def visitScoped_name(self, ctx:MIDLGrammarRulesParser.Scoped_nameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#base_type_spec.
    def visitBase_type_spec(self, ctx:MIDLGrammarRulesParser.Base_type_specContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#floating_pt_type.
    def visitFloating_pt_type(self, ctx:MIDLGrammarRulesParser.Floating_pt_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#integer_type.
    def visitInteger_type(self, ctx:MIDLGrammarRulesParser.Integer_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#signed_int.
    def visitSigned_int(self, ctx:MIDLGrammarRulesParser.Signed_intContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#unsigned_int.
    def visitUnsigned_int(self, ctx:MIDLGrammarRulesParser.Unsigned_intContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#declarators.
    def visitDeclarators(self, ctx:MIDLGrammarRulesParser.DeclaratorsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#declarator.
    def visitDeclarator(self, ctx:MIDLGrammarRulesParser.DeclaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#simple_declarator.
    def visitSimple_declarator(self, ctx:MIDLGrammarRulesParser.Simple_declaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#array_declarator.
    def visitArray_declarator(self, ctx:MIDLGrammarRulesParser.Array_declaratorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#exp_list.
    def visitExp_list(self, ctx:MIDLGrammarRulesParser.Exp_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#or_expr.
    def visitOr_expr(self, ctx:MIDLGrammarRulesParser.Or_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#xor_expr.
    def visitXor_expr(self, ctx:MIDLGrammarRulesParser.Xor_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#and_expr.
    def visitAnd_expr(self, ctx:MIDLGrammarRulesParser.And_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#shift_expr.
    def visitShift_expr(self, ctx:MIDLGrammarRulesParser.Shift_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#add_expr.
    def visitAdd_expr(self, ctx:MIDLGrammarRulesParser.Add_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#mult_expr.
    def visitMult_expr(self, ctx:MIDLGrammarRulesParser.Mult_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#unary_expr.
    def visitUnary_expr(self, ctx:MIDLGrammarRulesParser.Unary_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MIDLGrammarRulesParser#literal.
    def visitLiteral(self, ctx:MIDLGrammarRulesParser.LiteralContext):
        return self.visitChildren(ctx)



del MIDLGrammarRulesParser