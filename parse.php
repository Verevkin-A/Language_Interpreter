<?php
/**
 * IPPcode22 parser
 * @author Aleksandr Verevkin (xverev00), VUT FIT IPP 2021/2022
 */

ini_set('display_errors', 'stderr');
// class with utilities
final class Utils
{
    // errors
    const PARAM_ERR = 10;
    const HEADER_ERR = 21;
    const OPCODE_ERR = 22;
    const LEX_SYN_ERR = 23;
    // method for print error message and exit program with given return code
    function error(int $err, string $msg) {
        fwrite(STDERR, "Error: " . $msg . "\n");
        exit($err);
    }
    // method that check if symbol is variable or type representation
    function check_symb(string $operand, DOMDocument $xml, int $arg_num) {
        $type = explode("@", $operand, 2);
        if ($type[0] == "GF" || $type[0] == "LF" || $type[0] == "TF") {
            $arg = $xml->createElement("arg$arg_num", htmlspecialchars($operand));
            $arg->setAttribute("type", "var");
        } else {
            $arg = $xml->createElement("arg$arg_num", htmlspecialchars($type[1]));
            $arg->setAttribute("type", $type[0]);
        }
        return $arg;
    }
}
// help message
const HELP = <<<EOD
            The script of filter type reads the source code in IPPcode22, 
            checks the lexical and syntactic correctness of the code and 
            prints to standard output XML representation of the program. 
            
            Usage: php8.1 parse.php < file [--help]
              --help prints short help message\n
EOD;
// regex representation of identifiers
const SPEC_CHAR = "_\-$&%*!?";
const HEADER = "%^\.IPPcode22$%i";
const FRAMES = "(GF|LF|TF)";
const NIL = "(nil@nil)";
const BOOL = "(bool@(true|false))";
const DECIMAL = "([0-9]+)";
const OCTAL = "(0[oO]?[0-7]+)";
const HEXADECIMAL = "(0[xX][0-9a-fA-F]+)";
const INT = "(int@(\+|\-)?(" . DECIMAL . "|" . OCTAL . "|" . HEXADECIMAL . "))";
const STRING = "((string)@((\\\\[0-9]{3})|[^\s\#\\\\])*)";
const TYPE = "~^(bool|int|string)$~";
const CONSTANT = "(" . NIL . "|" . BOOL . "|" . INT . "|" . STRING . ")";
const IDENTIFIER_SOLO = "([A-Za-z" . SPEC_CHAR . "][0-9A-Za-z" . SPEC_CHAR . "]*)";
const IDENTIFIER = "~^" . IDENTIFIER_SOLO . "$~";
const VARIABLE_SOLO = "(" . FRAMES . "@" . IDENTIFIER_SOLO . ")";
const VARIABLE = "~^" . VARIABLE_SOLO . "$~";
const SYMBOL = "~^(" . CONSTANT . "|" . VARIABLE_SOLO . ")$~";
$utils = new Utils();
# check for arguments
switch ($argc) {
    case 1:
        break;
    case 2:
        if ($argv[1] == "--help") {
            echo HELP;
            exit;
        } else {
            $utils->error(UTILS::PARAM_ERR, "unknown parameter");
        }
    default:
        $utils->error(UTILS::PARAM_ERR, "wrong count of parameters");
}
// create output xml document
$xml = new DOMDocument("1.0", "UTF-8");
$xml->formatOutput = true;

$xml_program = $xml->createElement("program");
$xml_program = $xml->appendChild($xml_program);
$xml_lang = $xml->createAttribute("language");
$xml_lang->value = "IPPcode22";
$xml_program->appendChild($xml_lang);

$ln = 0;
$header = false;
// go through input file, line by line
while ($line = fgets(STDIN)) {
    $line = trim(explode("#", $line)[0]);
    if ($line == "") {
        continue;
    }
    // check input for .ippcode22 header
    if (!$header) {
        if(preg_match(HEADER, $line)) {
            $header = true;
            continue;
        } else {
            $utils->error(UTILS::HEADER_ERR, "input file should start with '.IPPcode22' header");
        }
    }
    // split line into an operand and operands
    $line_args = preg_split("/\s+/", $line);
    $ln++;
    $xmlInstruction = $xml->createElement("instruction");
    $xmlInstruction->setAttribute("order", $ln);
    $xmlInstruction->setAttribute("opcode", strtoupper($line_args[0]));
    // check first line argument on operand
    switch (strtoupper($line_args[0])) {
        // no operands
        case "CREATEFRAME":
        case "PUSHFRAME":
        case "POPFRAME":
        case "RETURN":
        case "BREAK":
            if (count($line_args) != 1) {
                $utils->error(UTILS::LEX_SYN_ERR, "wrong count of operands");
            }
            break;
        // <var>
        case "DEFVAR":
        case "POPS":
            if (count($line_args) != 2) {
                $utils->error(UTILS::LEX_SYN_ERR, "wrong count of operands");
            }
            if (!preg_match(VARIABLE, $line_args[1])) {
                $utils->error(UTILS::LEX_SYN_ERR, "variable identifier");
            }
            $arg1 = $xml->createElement("arg1", htmlspecialchars($line_args[1]));
            $arg1->setAttribute("type", "var");
            $xmlInstruction->appendChild($arg1);
            break;
        // <label>
        case "CALL":
        case "LABEL":
        case "JUMP":
            if (count($line_args) != 2) {
                $utils->error(UTILS::LEX_SYN_ERR, "wrong count of operands");
            }
            if (!preg_match(IDENTIFIER, $line_args[1])) {
                $utils->error(UTILS::LEX_SYN_ERR, "label identifier");
            }
            $arg1 = $xml->createElement("arg1", htmlspecialchars($line_args[1]));
            $arg1->setAttribute("type", "label");
            $xmlInstruction->appendChild($arg1);
            break;
        // <symb>
        case "PUSHS":
        case "WRITE":
        case "EXIT":
        case "DPRINT":
            if (count($line_args) != 2) {
                $utils->error(UTILS::LEX_SYN_ERR, "wrong count of operands");
            }
            if (!preg_match(SYMBOL, $line_args[1])) {
                $utils->error(UTILS::LEX_SYN_ERR, "symbol identifier");
            }
            $arg1 = $utils->check_symb($line_args[1], $xml, 1);
            $xmlInstruction->appendChild($arg1);
            break;
        // <var> <symb>
        case "MOVE":
        case "INT2CHAR":
        case "STRLEN":
        case "TYPE":
        case "NOT":
            if (count($line_args) != 3) {
                $utils->error(UTILS::LEX_SYN_ERR, "wrong count of operands");
            }
            if (!preg_match(VARIABLE, $line_args[1])) {
                $utils->error(UTILS::LEX_SYN_ERR, "variable identifier");
            }
            if (!preg_match(SYMBOL, $line_args[2])) {
                $utils->error(UTILS::LEX_SYN_ERR, "symbol identifier");
            }
            $arg1 = $xml->createElement("arg1", htmlspecialchars($line_args[1]));
            $arg1->setAttribute("type", "var");
            $arg2 = $utils->check_symb($line_args[2], $xml, 2);
            $xmlInstruction->appendChild($arg1);
            $xmlInstruction->appendChild($arg2);
            break;
        // <var> <type>
        case "READ":
            if (count($line_args) != 3) {
                $utils->error(UTILS::LEX_SYN_ERR, "wrong count of operands");
            }
            if (!preg_match(VARIABLE, $line_args[1])) {
                $utils->error(UTILS::LEX_SYN_ERR, "variable identifier");
            }
            if (!preg_match(TYPE, $line_args[2])) {
                $utils->error(UTILS::LEX_SYN_ERR, "type identifier");
            }
            $arg1 = $xml->createElement("arg1", htmlspecialchars($line_args[1]));
            $arg1->setAttribute("type", "var");
            $arg2 = $xml->createElement("arg2", htmlspecialchars($line_args[2]));
            $arg2->setAttribute("type", "type");
            $xmlInstruction->appendChild($arg1);
            $xmlInstruction->appendChild($arg2);
            break;
        // <var> <symb1> <symb2>
        case "ADD":
        case "SUB":
        case "MUL":
        case "IDIV":
        case "LT":
        case "GT":
        case "EQ":
        case "AND":
        case "OR":
        case "STRI2INT":
        case "CONCAT":
        case "GETCHAR":
        case "SETCHAR":
            if (count($line_args) != 4) {
                $utils->error(UTILS::LEX_SYN_ERR, "wrong count of operands");
            }
            if (!preg_match(VARIABLE, $line_args[1])) {
                $utils->error(UTILS::LEX_SYN_ERR, "variable identifier");
            }
            if (!preg_match(SYMBOL, $line_args[2])) {
                $utils->error(UTILS::LEX_SYN_ERR, "symbol identifier");
            }
            if (!preg_match(SYMBOL, $line_args[3])) {
                $utils->error(UTILS::LEX_SYN_ERR, "symbol identifier");
            }
            $arg1 = $xml->createElement("arg1", htmlspecialchars($line_args[1]));
            $arg1->setAttribute("type", "var");
            $arg2 = $utils->check_symb($line_args[2], $xml, 2);
            $arg3 = $utils->check_symb($line_args[3], $xml, 3);
            $xmlInstruction->appendChild($arg1);
            $xmlInstruction->appendChild($arg2);
            $xmlInstruction->appendChild($arg3);
            break;
        // <label> <symb1> <symb2>
        case "JUMPIFEQ":
        case "JUMPIFNEQ":
            if (count($line_args) != 4) {
                $utils->error(UTILS::LEX_SYN_ERR, "wrong count of operands");
            }
            if (!preg_match(IDENTIFIER, $line_args[1])) {
                $utils->error(UTILS::LEX_SYN_ERR, "label identifier");
            }
            if (!preg_match(SYMBOL, $line_args[2])) {
                $utils->error(UTILS::LEX_SYN_ERR, "symbol identifier");
            }
            if (!preg_match(SYMBOL, $line_args[3])) {
                $utils->error(UTILS::LEX_SYN_ERR, "symbol identifier");
            }
            $arg1 = $xml->createElement("arg1", htmlspecialchars($line_args[1]));
            $arg1->setAttribute("type", "label");
            $arg2 = $utils->check_symb($line_args[2], $xml, 2);
            $arg3 = $utils->check_symb($line_args[3], $xml, 3);
            $xmlInstruction->appendChild($arg1);
            $xmlInstruction->appendChild($arg2);
            $xmlInstruction->appendChild($arg3);
            break;
        default:
            $utils->error(UTILS::OPCODE_ERR, "unknown opcode");
    }
    $xml_program->appendChild($xmlInstruction);
}
echo $xml->saveXML();
exit;
