grammar MIDLGrammarRules;
import MIDLLexerRules;
//*号是0或多次，而+号是1或者多次，但是这里测试的结果是*是至少1次，+才是0到多次
specification : definition+;
definition : type_decl ';' | module ';';
module : 'module' ID '{' definition+ '}';
type_decl : struct_type | 'struct' ID;
struct_type : 'struct' ID '{' member_list '}';
member_list : (type_spec declarators ';')*;
type_spec : scoped_name | base_type_spec | struct_type;
scoped_name : '::'? ID ('::' ID)*;
base_type_spec : floating_pt_type | integer_type | 'char' | 'string' | 'boolean';
floating_pt_type : 'float' | 'double' | 'long double';
integer_type : signed_int | unsigned_int;
signed_int : ('short' | 'int16')
            | ('long' | 'int32')
            | ('long' 'long' | 'int64')
            | 'int8';
unsigned_int : ('unsigned' 'short' | 'unit16')
            | ('unsigned' 'long' | 'unit32')
            |('unsigned' 'long' 'long' | 'unit64')
            |'unit8';
declarators : declarator (',' declarator)*;
declarator : simple_declarator | array_declarator;
simple_declarator : ID ('=' or_expr)?;
array_declarator : ID '[' or_expr ']' ('=' exp_list)?;
exp_list : '[' or_expr (',' or_expr)* ']';
or_expr : xor_expr ('|' xor_expr)*;
xor_expr : and_expr ('^' and_expr)*;
and_expr : shift_expr ('&' shift_expr)*;
shift_expr : add_expr (('>>'|'<<') add_expr)*;
add_expr : mult_expr (('+'|'-') mult_expr)*;
mult_expr : unary_expr (('*'|'/'|'%') unary_expr)*;
unary_expr : ('-'|'+'|'~')? literal;
literal : INTEGER | FLOATING_PT | CHAR | STRING | BOOLEAN;