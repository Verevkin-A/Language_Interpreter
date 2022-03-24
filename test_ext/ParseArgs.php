<?php
/**
 * IPPcode22 program parameters parsing
 * @author Aleksandr Verevkin (xverev00), VUT FIT IPP 2021/2022
 */

require_once "TestUtils.php";

final class ParseArgs
{
    // arguments default values
    public string $dir = ".";
    public bool $recursive = false;
    public string $parse = "parse.php";
    public string $interpret = "interpret.py";
    public bool $parse_only = false;
    public bool $int_only = false;
    public string $jexam = "/pub/courses/ipp/jexamxml/jexamxml.jar";
    public string $options = "/pub/courses/ipp/jexamxml/options";
    public bool $noclean = false;
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

    protected int $argc;
    protected array $args;
    protected TestUtils $utils;

    public function __construct(int $argc) {
        // declare utils
        $this->utils = new TestUtils();
        $this->argc = $argc;
        // get program arguments
        $long_opt = array("help", "directory:", "recursive", "parse-script:", "int-script:",
            "parse-only", "int-only", "jexampath:", "noclean");
        $this->args = getopt("", $long_opt);
        $this->check_params();
        $this->set_params();
    }

    private function process_path(string $path): string {
        if (!($processed_path = realpath($path))) {
            $this->utils->error($this->utils::BAD_DIR, "file or directory doesn't exist (" . $path . ")");
        }
        return $processed_path;
    }

    protected function check_help() {
        if (key_exists("help", $this->args)) {
            if (count($this->args) == 1) {
                echo $this::HELP;
                exit;
            } else {
                $this->utils->error($this->utils::PARAM_ERR, "help parameter can't be combined with others");
            }
        }
    }

    protected function check_params() {
        // check for help parameter
        $this->check_help();
        // check for undefined program arguments
        if (count($this->args) != $this->argc - 1) {
            $this->utils->error($this->utils::PARAM_ERR, "unknown parameter");
        }
        // check for forbidden combinations
        if (key_exists("parse-only", $this->args) &&
            (key_exists("int-only", $this->args) || key_exists("int-script", $this->args))) {
            $this->utils->error($this->utils::PARAM_ERR, "'parse-only' can't be combined with interpret parameters");
        }
        if (key_exists("int-only", $this->args) &&
            (key_exists("parse-only", $this->args) || key_exists("parse-script", $this->args))) {
            $this->utils->error($this->utils::PARAM_ERR, "'int-only' can't be combined with parse parameters");
        }
    }

    public function set_params() {
        // set boolean parameters
        $this->recursive = key_exists("recursive", $this->args);
        $this->parse_only = key_exists("parse-only", $this->args);
        $this->int_only = key_exists("int-only", $this->args);
        $this->noclean = key_exists("noclean", $this->args);
        // set path parameters
        if(key_exists("directory", $this->args)) {
            $this->dir = $this->process_path($this->args["directory"]);
        }
        if(key_exists("parse-script", $this->args)) {
            $this->parse = $this->process_path($this->args["parse-script"]);
        }
        if(key_exists("int-script", $this->args)) {
            $this->interpret = $this->process_path($this->args["int-script"]);
        }
        if(key_exists("jexampath", $this->args)) {
            $path = $this->process_path($this->args["jexampath"]);
            $this->jexam = $this->process_path($path . "/jexamxml.jar");
            $this->options = $this->process_path($path . "/options");
        }
    }
}
