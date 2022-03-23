<?php

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
    }

    protected function check_help() {
//        var_dump($this->args);
        if (key_exists("help", $this->args)) {
            if (count($this->args) == 1) {
                echo $this::HELP;
                exit;
            } else {
                $this->utils->error($this->utils::PARAM_ERR, "help parameter can't be combined with others");
            }
        }
    }

    private function process_path(string $path) {
        if (!($path = realpath($path))) {
            $this->utils->error($this->utils::BAD_DIR, "file or directory doesn't exist");
        }
//        if (!file_exists($path)) {
//            $this->utils->error($this->utils::BAD_DIR, "file or directory doesn't exist");
//        }
        return $path;
    }

    protected function check_params() {
        // check for help parameter
        $this->check_help();
        // check for undefined program arguments
        if (count($this->args) != $this->argc - 1) {
            $this->utils->error($this->utils::PARAM_ERR, "unknown parameter");
        }
        // set boolean parameters
        $this->recursive = key_exists("recursive", $this->args);
        $this->parse_only = key_exists("parse-only", $this->args);
        $this->int_only = key_exists("int-only", $this->args);
        $this->noclean = key_exists("noclean", $this->args);

        if(key_exists("directory", $this->args)) {
            $this->dir = $this->process_path($this->args["directory"]);
        }
        if(key_exists("parse-only", $this->args)) {
            $this->parse = $this->process_path($this->args["parse-only"]);
        }
        if(key_exists("int-only", $this->args)) {
            $this->interpret = $this->process_path($this->args["int-only"]);
        }
        # TODO if exist jexam
    }
}
