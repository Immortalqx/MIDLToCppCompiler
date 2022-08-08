lexer grammar MIDLLexerRules;
// 因为是从上到下匹配的，如果BOOLEAN 在 LITTER后面，会导致'TRUE'等都被识别成LETTER
BOOLEAN : 'TRUE' | 'true' | 'FALSE' | 'false' ;
FLOAT_TYPE_SUFFIX : 'f' | 'F' | 'd' | 'D';
UNDERLINE : '_';
INTEGER_TYPE_SUFFIX : 'l' | 'L';

INTEGER : ('0' | [1-9] [0-9]*) INTEGER_TYPE_SUFFIX?;
EXPONENT : ('e' | 'E') ('+' | '-')? [0-9]+;
FLOATING_PT:  [0-9]+ '.' [0-9]* EXPONENT? FLOAT_TYPE_SUFFIX?
   			| '.' [0-9]+ EXPONENT? FLOAT_TYPE_SUFFIX?
   			| [0-9]+ EXPONENT FLOAT_TYPE_SUFFIX?
   			| [0-9]+ EXPONENT? FLOAT_TYPE_SUFFIX
   			;

ESCAPE_SEQUENCE : '\\'('b' | 't' | 'n' | 'f' | 'r' | '"' | '\'' | '\\' );
CHAR : '\''(ESCAPE_SEQUENCE | (~'\\'|~'\''))'\'';
STRING : '"'(ESCAPE_SEQUENCE | (~'\\'|~'"'))*'"';

ID : LETTER (UNDERLINE?(LETTER | DIGIT))*;
LETTER : [a-z] | [A-Z];
DIGIT : [0-9];

WS : [ \t\r\n]+ -> skip;