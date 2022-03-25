<?php
/**
 * IPPcode22 single test result
 * @author Aleksandr Verevkin (xverev00), VUT FIT IPP 2021/2022
 */

final class TestResult
{
    // temporary files paths
    public string $parse_stdout_path;
    public string $int_stdout_path;
    public string $stderr_path;
    // outputs
    public string $stdout;
    public string $stderr;

    public int $expected_code;
    public ?int $returned_code;
    public ?bool $output_same;

    public function __construct(string $path, string $name) {
        $this->parse_stdout_path = "$path/$name.tmpparse";
        $this->int_stdout_path = "$path/$name.tmpint";
        $this->stderr_path = "$path/$name.tmperr";
        // get expected return code from file
        $this->expected_code = intval(file_get_contents("$path/$name.rc"));
    }

    public function clean(bool $parse_only) {
        // transit content of temporary files into strings
        $this->stderr = file_get_contents($this->stderr_path);
        $this->stdout = $parse_only ? file_get_contents($this->parse_stdout_path) : file_get_contents($this->int_stdout_path);
        // delete temporary files
        @unlink($this->parse_stdout_path);
        @unlink($this->int_stdout_path);
        @unlink($this->stderr_path);
    }
}
