<?php
/**
 * IPPcode22 single test instance
 * @author Aleksandr Verevkin (xverev00), VUT FIT IPP 2021/2022
 */

require_once "TestResult.php";

final class TestItem
{
    protected string $php = "php";  # TODO php8.1
    // test case info and paths to files
    public string $name;
    public string $src;
    public string $in;
    public string $out;
    public string $rc;

    protected ParseArgs $args;

    public function __construct(string $name, ParseArgs $args) {
        $this->name = $name;
        $this->args = $args;
    }

    public function set_test(): bool {
        // check if .src file present
        if (!isset($this->src)) {
            return false;
        }
        // check for other file extensions and create them if needed
        if (!isset($this->in)) {
            touch(dirname($this->src) . "/$this->name.in");
        }
        if(!isset($this->out)) {
            touch(dirname($this->src) . "/$this->name.out");
        }
        if (!isset($this->rc)) {
            file_put_contents(dirname($this->src) . "/$this->name.rc", "0");
        }
        return true;
    }

    public function run_parser_test(): TestResult {
        $res = new TestResult(dirname($this->src), $this->name);
        $command = "$this->php " . $this->args->parse . " < $this->src > $res->stdout_path 2> $res->stderr_path";
        exec($command, result_code: $res->returned_code);

        if ($res->returned_code != $res->expected_code) {
            return $res;
        }
        if ($res->expected_code != 0) {
            return $res;
        }

        if ($this->args->parse_only) {
            $comp_command = "java -jar " . $this->args->jexam . " $this->out $res->stdout_path delta.xml " . $this->args->options;
        } else {
            $comp_command = "diff $this->out $res->stdout_path";

        }
        exec($comp_command, result_code: $res->output_same);
        @unlink("delta.xml");

        return $res;
    }

    private function run_interpret_test() {

    }
}
