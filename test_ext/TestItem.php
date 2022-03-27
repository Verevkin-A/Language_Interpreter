<?php
/**
 * IPPcode22 single test instance
 * @author Aleksandr Verevkin (xverev00), VUT FIT IPP 2021/2022
 */

require_once "TestResult.php";

/**
 * Class representing single testing item
 */
final class TestItem
{
    protected string $php = "php8.1";
    protected string $python = "python3.8";
    // test case info and paths to files
    public string $name;
    public string $src;
    public string $in;
    public string $out;
    public string $rc;

    protected ParseArgs $args;

    /**
     * TestItem constructor
     *
     * @param string $name name of the test
     * @param ParseArgs $args program arguments
     */
    public function __construct(string $name, ParseArgs $args) {
        $this->name = $name;
        $this->args = $args;
    }

    /**
     * Create missing files for test suit
     *
     * @return bool True in case of success, False otherwise
     */
    public function set_test(): bool {
        // check if .src file present
        if (!isset($this->src)) {
            // skip the test if .src file is missing
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

    /**
     * Run tests according to given parameters
     *
     * @return TestResult test result
     */
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

    /**
     * Execute tests on parser
     *
     * @param TestResult $res test instance
     */
    public function run_parser_test(TestResult $res) {
        // execute parser
        $command = "$this->php " . $this->args->parse . " < $this->src > $res->parse_stdout_path 2> $res->stderr_path";
        exec($command, result_code: $res->returned_code);
        // check if expected and actual returned codes are different
        if ($res->returned_code != $res->expected_code) {
            $res->test_result = false;
            return;
        }
        // if code return error there is no point in output comparison
        if ($res->expected_code != 0) {
            $res->test_result = true;
            return;
        }
        // compare output with jexam
        if ($this->args->parse_only) {
            $comp_command = "java -jar " . $this->args->jexam . " $this->out $res->parse_stdout_path delta.xml " . $this->args->options;
            exec($comp_command, result_code: $jexam_output);
            $res->test_result = $res->output_same = !$jexam_output;     # jexam returns 0 in case of no difference
            @unlink("delta.xml");
        }
    }

    /**
     * Execute tests on interpret
     *
     * @param TestResult $res test instance
     */
    private function run_interpret_test(TestResult $res) {
        // execute interpret
        $source = $this->args->both ? $res->parse_stdout_path : $this->src;
        $input = dirname($this->src). "/$this->name.in";
        $command = "$this->python " . $this->args->interpret . " --source=$source --input=$input > $res->int_stdout_path 2> $res->stderr_path";
        exec($command, result_code: $res->returned_code);
        // check if expected and actual returned codes are different
        if ($res->returned_code != $res->expected_code) {
            $res->test_result = false;
            return;
        }
        // if code return error there is no point in output comparison
        if ($res->expected_code != 0) {
            $res->test_result = true;
            return;
        }
        // compare with expected output
        $output = dirname($this->src). "/$this->name.out";
        $comp_command = "diff $res->int_stdout_path $output";
        exec($comp_command, result_code: $diff_ret);
        $res->test_result = $res->output_same = !$diff_ret;     # diff returns 0 in case of no difference
    }
}
