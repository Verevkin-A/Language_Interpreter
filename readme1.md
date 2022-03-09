Documentation of Project Implementation for 1 task of IPP 2021/2022<br/>
Name and surname: Aleksandr Verevkin<br/>
Login: xverev00<br/>

## Source code analysis
Source code is read line by line from standard input.
Lines dynamically checked for required header `.IPPcode22`,
existing opcodes and corresponding operands.
After inspection, source code, if it's syntax-correct, will be
printed on standard output as his XML representation.

## Regex
Verification, if operands are matched with opcode, is handled with
`regular expressions`. Each type of operand is defined by regex
in form of php constant at the start of the script.

## Utilities class
Class `Utils` represent helping constants and functions.
Class contains return codes, program error exit handling,
arguments check and  creating corresponding output element 
for variable or constant.

## Output XML representation
Output XML code is created using php built-in 
`DOM(Document Object Model)` parser. Parser helping to create
elements for instructions and arguments, tree-based structure
for easier understanding.
