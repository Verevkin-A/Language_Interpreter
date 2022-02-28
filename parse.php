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
    $splitted = explode(" ", $line);
    foreach ($splitted as $word) {
        echo $word;
    }

//    echo $line;
}








exit;
