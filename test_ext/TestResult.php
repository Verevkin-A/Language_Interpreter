<?php
/**
 * IPPcode22 single test result
 * @author Aleksandr Verevkin (xverev00), VUT FIT IPP 2021/2022
 */

/**
 * Class with single test result information
 */
final class TestResult
{
    // temporary files paths
    public string $parse_stdout_path;
    public string $int_stdout_path;
    public string $stderr_path;
    // stderr output
    public string $stderr;
    // test information
    public string $test_name;
    public string $test_path;
    public int $expected_code;
    public ?int $returned_code;
    public ?bool $output_same;
    public bool $test_result;

    /**
     * TestResult constructor
     *
     * @param string $path path to test suit
     * @param string $name name of the test
     */
    public function __construct(string $path, string $name) {
        $this->test_name = $name;
        $this->test_path = "$path/$name";
        // declare temporary files paths
        $this->parse_stdout_path = "$this->test_path.tmpparse";
        $this->int_stdout_path = "$this->test_path.tmpint";
        $this->stderr_path = "$this->test_path.tmperr";
        // get expected return code from file
        $this->expected_code = intval(file_get_contents("$this->test_path.rc"));
    }

    /**
     * Clean up temporary files from system
     */
    public function clean() {
        // transit content of stderr file into string
        $this->stderr = file_get_contents($this->stderr_path);
        // delete temporary files
        @unlink($this->parse_stdout_path);
        @unlink($this->int_stdout_path);
        @unlink($this->stderr_path);
    }
}
