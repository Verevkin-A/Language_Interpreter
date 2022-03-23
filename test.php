<?php
/**
 * IPPcode22 test script
 * @author Aleksandr Verevkin (xverev00), VUT FIT IPP 2021/2022
 */

// setting to show errors on stderr
ini_set('display_errors', 'stderr');

final class TestUtils
{
    // errors
    const PARAM_ERR = 10;
    const BAD_DIR = 41;

    /**
     * Print error message and exit program with given return code
     *
     * @param int $err error code
     * @param string $msg error message
     */
    function error(int $err, string $msg) {
        fwrite(STDERR, "Error: " . $msg . "\n");
        exit($err);
    }
}

final class ParseArgs
{
    // help message
    protected const HELP = <<<EOD
            usage: php8.1 test.php [--help] [--directory [~/src]] [--recursive] [--parse-script [~/src]]
            [--int-script [~/src]] [--parse-only] [--int-only] [--jexampath [~/src]] [--noclean]

            The script serve for testing of parse.php and interpret.py scripts.
            Script will go through directory with tests and will use them for automatic tests.

            options:
              --help            prints short help message
              --directory       directory for tests searching
              --recursive       tests also will be searched in subdirectories
              --parse-script    file with parse php script
              --int-script      file with interpret python script
              --parse-only      only parse php script will be tested
              --int-only        only interpret python script will be tested
              --jexampath       path to directory with jexamxml.jar
              --noclean         script help files won't be deleted\n
    EOD;
    protected array $options;
    protected TestUtils $utils;

    public function __construct() {
        // declare utils
        $this->utils = new TestUtils();
        // get program arguments
        $long_opt = array("help", "directory:", "recursive", "parse-script:", "int-script:",
            "parse-only", "int-only", "jexampath:", "noclean");
        $this->options = getopt("", $long_opt);
        // check for help parameter
        $this->check_help();
    }

    function check_help() {
        $opt_keys = array_keys($this->options);
        var_dump($this->options);
        if (in_array("help", $opt_keys)) {
            if (count($this->options) == 1) {
                echo $this::HELP;
                exit;
            } else {
                $this->utils->error($this->utils::PARAM_ERR, "help parameter can't be combined with others");
            }
        }

    }
}

$args_parser = new ParseArgs();

