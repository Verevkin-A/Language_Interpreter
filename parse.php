<?php
ini_set('display_errors', 'stderr');

include "parser_ext/Ret_Codes.php";

const HELP = <<<EOD
            The script of filter type reads the source code in IPP-code22, 
            checks the lexical and syntactic correctness of the code and 
            prints to standard output XML representation of the program. 
            
            Usage: php8.1 parse.php < file [--help]
              --help prints short help message\n
EOD;
const SPEC_CHAR = "_\-$&%*!?";
const HEADER = "%^\.IPPcode22$%i";
const FRAMES = "(GF|LF|TF)";
const NIL = "(nil@nil)";
const BOOL = "(bool@(true|false))";
const INT = "(int@((\+|\-)?[0-9]+))";
CONST STRING = "((string)@((\\\\[0-9]{3})|[^\s\#\\\\])*)";
const CONSTANT = "(" . NIL . "|" . BOOL . "|" . INT . "|" . STRING . ")";
const IDENTIFIER_SOLO = "([A-Za-z" . SPEC_CHAR . "][0-9A-Za-z" . SPEC_CHAR . "]*)";
const IDENTIFIER = "~^" . IDENTIFIER_SOLO . "$~";
const VARIABLE_SOLO = "(" . FRAMES . "@" . IDENTIFIER_SOLO . ")";
const VARIABLE = "~^" . VARIABLE_SOLO . "$~";
const SYMBOL = "~^(" . CONSTANT . "|" . VARIABLE_SOLO . ")$~";
switch ($argc) {
    case 1:
        break;
    case 2:
        if ($argv[1] == "--help") {
            echo HELP;
            exit;
        } else {
            fwrite(STDERR, "Error: unknown parameter\n");
            exit(Ret_Codes::PARAM_ERR);
        }
    default:
        fwrite(STDERR, "Error: wrong count of parameters\n");
        exit(Ret_Codes::PARAM_ERR);
}

$xml = new DOMDocument("1.0", "UTF-8");
$xml->formatOutput = true;

$xml_program = $xml->createElement("program");
$xml_program = $xml->appendChild($xml_program);

$xml_lang = $xml->createAttribute("language");
$xml_lang->value = "IPPcode22";
$xml_program->appendChild($xml_lang);


$ln = 0;
$header = false;
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
            fwrite(STDERR, "Input file should start with '.IPPcode22' header\n");
            exit(Ret_Codes::HEADER_ERR);
        }
    }
    $line_args = explode(" ", $line);
    $ln++;
    $xmlInstruction = $xml->createElement("instruction");
    $xmlInstruction->setAttribute("order", $ln);
    $xmlInstruction->setAttribute("opcode", strtoupper($line_args[0]));

    switch (strtoupper($line_args[0])) {
        # no operands
        case "CREATEFRAME":
        case "PUSHFRAME":
        case "POPFRAME":
        case "RETURN":
        case "BREAK":
            if (count($line_args) != 1) {
                fwrite(STDERR, "Error: wrong count of operands\n");
                exit(Ret_Codes::LEX_SYN_ERR);
            }
            break;
        # <var>
        case "DEFVAR":
        case "POPS":
            if (count($line_args) != 2) {
                fwrite(STDERR, "Error: wrong count of operands\n");
                exit(Ret_Codes::LEX_SYN_ERR);
            }
            if (!preg_match(VARIABLE, $line_args[1])) {
                fwrite(STDERR, "Error: variable identifier\n");
                exit(Ret_Codes::LEX_SYN_ERR);
            }
            $arg1 = $xml->createElement("arg1", htmlspecialchars($line_args[1]));
            $arg1->setAttribute("type", "var");
            $xmlInstruction->appendChild($arg1);
            break;
        # <label>
        case "CALL":
        case "LABEL":
        case "JUMP":
            if (count($line_args) != 2) {
                fwrite(STDERR, "Error: wrong count of operands\n");
                exit(Ret_Codes::LEX_SYN_ERR);
            }
            if (!preg_match(IDENTIFIER, $line_args[1])) {
                fwrite(STDERR, "Error: label identifier\n");
                exit(Ret_Codes::LEX_SYN_ERR);
            }
            $arg1 = $xml->createElement("arg1", htmlspecialchars($line_args[1]));
            $arg1->setAttribute("type", "label");
            $xmlInstruction->appendChild($arg1);
            break;
        # <symb>
        case "PUSHS":
        case "WRITE":
        case "EXIT":
        case "DPRINT":
            if (count($line_args) != 2) {
                fwrite(STDERR, "Error: wrong count of operands\n");
                exit(Ret_Codes::LEX_SYN_ERR);
            }
            if (!preg_match(SYMBOL, $line_args[1])) {
                fwrite(STDERR, "Error: symbol identifier\n");
                exit(Ret_Codes::LEX_SYN_ERR);
            }
            $arg1 = $xml->createElement("arg1", htmlspecialchars($line_args[1]));
            $type = explode("@", $line_args[1])[0];
            if ($type == "GF" || $type == "LF" || $type == "TF") {
                $type = "var";
            }
            $arg1->setAttribute("type", $type);
            $xmlInstruction->appendChild($arg1);
            break;
        # <var> <symb>
        case "MOVE":
        case "INT2CHAR":
        case "STRLEN":
        case "TYPE":
            if (count($line_args) != 3) {
                fwrite(STDERR, "Error: wrong count of operands\n");
                exit(Ret_Codes::LEX_SYN_ERR);
            }
            if (!preg_match(VARIABLE, $line_args[1])) {
                fwrite(STDERR, "Error: variable identifier\n");
                exit(Ret_Codes::LEX_SYN_ERR);
            }
            if (!preg_match(SYMBOL, $line_args[2])) {
                fwrite(STDERR, "Error: symbol identifier\n");
                exit(Ret_Codes::LEX_SYN_ERR);
            }
            $arg1 = $xml->createElement("arg1", htmlspecialchars($line_args[1]));
            $arg1->setAttribute("type", "var");
            $arg2 = $xml->createElement("arg2", htmlspecialchars($line_args[2]));
            $type = explode("@", $line_args[2])[0];
            if ($type == "GF" || $type == "LF" || $type == "TF") {
                $type = "var";
            }
            $arg2->setAttribute("type", $type);
            $xmlInstruction->appendChild($arg1);
            $xmlInstruction->appendChild($arg2);
            break;
        # <var> <type>
        case "READ":
//            echo "<var> <type>";
            break;
        # <var> <symb1> <symb2>
        case "ADD":
        case "SUB":
        case "MUL":
        case "IDIV":
        case "LT":
        case "GT":
        case "EQ":
        case "AND":
        case "OR":
        case "NOT":
        case "STRI2INT":
        case "CONCAT":
        case "GETCHAR":
        case "SETCHAR":
            if (count($line_args) != 4) {
                fwrite(STDERR, "Error: wrong count of operands\n");
                exit(Ret_Codes::LEX_SYN_ERR);
            }
            if (!preg_match(VARIABLE, $line_args[1])) {
                fwrite(STDERR, "Error: variable identifier\n");
                exit(Ret_Codes::LEX_SYN_ERR);
            }
            if (!preg_match(SYMBOL, $line_args[2])) {
                fwrite(STDERR, "Error: symbol identifier\n");
                exit(Ret_Codes::LEX_SYN_ERR);
            }
            if (!preg_match(SYMBOL, $line_args[3])) {
                fwrite(STDERR, "Error: symbol identifier\n");
                exit(Ret_Codes::LEX_SYN_ERR);
            }
            $arg1 = $xml->createElement("arg1", htmlspecialchars($line_args[1]));
            $arg1->setAttribute("type", "var");
            $arg2 = $xml->createElement("arg2", htmlspecialchars($line_args[2]));
            $type = explode("@", $line_args[2])[0];
            if ($type == "GF" || $type == "LF" || $type == "TF") {
                $type = "var";
            }
            $arg2->setAttribute("type", $type);
            $arg3 = $xml->createElement("arg3", htmlspecialchars($line_args[3]));
            $type = explode("@", $line_args[3])[0];
            if ($type == "GF" || $type == "LF" || $type == "TF") {
                $type = "var";
            }
            $arg3->setAttribute("type", $type);
            $xmlInstruction->appendChild($arg1);
            $xmlInstruction->appendChild($arg2);
            $xmlInstruction->appendChild($arg3);
            break;
        # <label> <symb1> <symb2>
        case "JUMPIFEQ":
        case "JUMPIFNEQ":
            if (count($line_args) != 4) {
                fwrite(STDERR, "Error: wrong count of operands\n");
                exit(Ret_Codes::LEX_SYN_ERR);
            }
            if (!preg_match(IDENTIFIER, $line_args[1])) {
                fwrite(STDERR, "Error: identifier\n");
                exit(Ret_Codes::LEX_SYN_ERR);
            }
            if (!preg_match(SYMBOL, $line_args[2])) {
                fwrite(STDERR, "Error: symbol identifier\n");
                exit(Ret_Codes::LEX_SYN_ERR);
            }
            if (!preg_match(SYMBOL, $line_args[3])) {
                fwrite(STDERR, "Error: symbol identifier\n");
                exit(Ret_Codes::LEX_SYN_ERR);
            }
            $arg1 = $xml->createElement("arg1", htmlspecialchars($line_args[1]));
            $arg1->setAttribute("type", "label");
            $arg2 = $xml->createElement("arg2", htmlspecialchars($line_args[2]));
            $type = explode("@", $line_args[2])[0];
            if ($type == "GF" || $type == "LF" || $type == "TF") {
                $type = "var";
            }
            $arg2->setAttribute("type", $type);
            $arg3 = $xml->createElement("arg3", htmlspecialchars($line_args[3]));
            $type = explode("@", $line_args[3])[0];
            if ($type == "GF" || $type == "LF" || $type == "TF") {
                $type = "var";
            }
            $arg3->setAttribute("type", $type);
            $xmlInstruction->appendChild($arg1);
            $xmlInstruction->appendChild($arg2);
            $xmlInstruction->appendChild($arg3);
            break;
        default:
            fwrite(STDERR, "Error: unknown opcode\n");
            exit(Ret_Codes::OPCODE_ERR);
    }

    $xml_program->appendChild($xmlInstruction);
}

echo $xml->saveXML();

exit;
