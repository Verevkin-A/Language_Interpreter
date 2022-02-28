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

$xml_program->setAttribute("language", "IPPcode22");

//$xml = new DomDocument("1.0", "UTF-8");
//$xml->formatOutput = true;	// Better formatting
//
//$xml_program = $xml->createElement("program");
//$xml_program = $xml->appendChild($xml_program);
//
//$language_A = $xml->createAttribute("language");
//$language_A->value = "IPPcode22";
//$xml_program->appendChild($language_A);
//
//$xml_inst = $xml->createElement("instruction");
//$xml_program->appendChild($xml_inst);
//
//echo $xml->saveXML();
//exit(1);

$header = false;
while ($line = fgets(STDIN)) {
    $line = trim(explode("#", $line)[0]);
    if ($line == "") {
        continue;
    }
    // check input for .ippcode22 header
    if (!$header) {
        if(preg_match("%^\.IPPcode22$%i", $line)) {
            $header = true;
            continue;
        } else {
            fwrite(STDERR, "Input file should start with '.IPPcode22' header\n");
            exit(Ret_Codes::HEADER_ERR);
        }
    }
    $line_args = explode(" ", $line);
    switch ($line_args[0]) {
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
            break;
        # <label>
        case "CALL":
        case "LABEL":
        case "JUMP":
//            echo "<label>";
            break;
        # <symb>
        case "PUSHS":
        case "WRITE":
        case "EXIT":
        case "DPRINT":
//            echo "<symb>";
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
            break;
        # <label> <symb1> <symb2>
        case "JUMPIFEQ":
        case "JUMPIFNEQ":
//            echo "<label> <symb1> <symb2>";
            break;
        default:
            fwrite(STDERR, "Error: unknown opcode\n");
            exit(Ret_Codes::OPCODE_ERR);
    }


}

$xmlInstruction = $xml->createElement("instruction");
$xmlInstruction->setAttribute("order", "lol");
$xmlInstruction->setAttribute("opcode", "lol2");

$xmlArg1 = $xml->createElement("arg1", "lolzs");
$xmlArg1->setAttribute("type", "var");
$xmlInstruction->appendChild($xmlArg1);

$xml_program = $xml->appendChild($xmlInstruction);

echo $xml->saveXML();


exit;
