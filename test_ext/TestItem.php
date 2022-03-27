<?php
/**
 * IPPcode22 single test instance
 * @author Aleksandr Verevkin (xverev00), VUT FIT IPP 2021/2022
 */

require_once "TestResult.php";

final class TestItem
{
    protected string $php = "php";  # TODO php8.1
    protected string $python = "python3.8";
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

    public function run_test(): TestResult {
        // initialize new test case result
        $res = new TestResult(dirname($this->src), $this->name);
        if ($this->args->both || $this->args->parse_only) {
            $this->run_parser_test($res);
        }
        if ($this->args->both || $this->args->int_only) {
            $this->run_interpret_test($res);
        }
        return $res;
    }

    public function run_parser_test(TestResult $res) {
        // execute parser
        $command = "$this->php " . $this->args->parse . " < $this->src > $res->parse_stdout_path 2> $res->stderr_path";
        exec($command, result_code: $res->returned_code);
        // check if expected and actual returned codes are different
        if ($res->returned_code != $res->expected_code) {
            return;
        }
        // if code return error there is no point in output comparison
        if ($res->expected_code != 0) {
            return;
        }
        // compare output with jexam
        if ($this->args->parse_only) {
            $comp_command = "java -jar " . $this->args->jexam . " $this->out $res->parse_stdout_path delta.xml " . $this->args->options;
            exec($comp_command, result_code: $jexam_output);
            $res->output_same = !$jexam_output;     # jexam returns 0 in case of no difference
            @unlink("delta.xml");
        }
    }

    private function run_interpret_test(TestResult $res) {
        // execute interpret
        $source = $this->args->both ? $res->parse_stdout_path : $this->src;
        $input = dirname($this->src). "/$this->name.in";
        $command = "$this->python " . $this->args->interpret . " --source=$source --input=$input > $res->int_stdout_path 2> $res->stderr_path";
        exec($command, result_code: $res->returned_code);
        // check if expected and actual returned codes are different
        if ($res->returned_code != $res->expected_code) {
            return;
        }
        // if code return error there is no point in output comparison
        if ($res->expected_code != 0) {
            return;
        }
        // compare with expected output
        $output = dirname($this->src). "/$this->name.out";
        $comp_command = "diff $res->int_stdout_path $output";
        exec($comp_command, result_code: $diff_ret);
        $res->output_same = !$diff_ret;     # diff returns 0 in case of no difference
    }
}
