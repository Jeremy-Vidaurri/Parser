# Parser
A program made to convert a text document into a context free grammar tree. 

Utilizes the following rules:
*  \<program> -> <stmt_list> $$
*  \<stmt list> -> <stmt> <stmt_list> | epsilon
*  \<stmt> -> id assign <expr> | read id | write <expr>
*  \<expr> -> <term> <term_tail>
*  \<term tail> -> <add_op> <term> <term_tail> | epsilon
*  \<term> -> <factor> <factor_tail>
*  \<factor_tail> -> <mult_op> <factor> <factor_tail> | epsilon
*  \<factor> -> lparen <expr> rparen | id | number
*  \<add_op> -> plus | minus
*  \<mult_op> -> times | div

## Running the Parser
To run the parser, place the parser.py in the same folder as the input text file. Then in command line, use the command `Python parser.py input.txt` where `input.txt` is the name of the input text file.


## Contributions
* [Jeremy Vidaurri](https://github.com/Jeremy-Vidaurri)
* Ryan Villarreal
