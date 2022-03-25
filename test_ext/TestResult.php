<?php
/**
 * IPPcode22 single test result
 * @author Aleksandr Verevkin (xverev00), VUT FIT IPP 2021/2022
 */

final class TestResult
{
    // temporary files paths
    public string $stdout_path;
    public string $stderr_path;
    // outputs
    public string $stdout;
    public string $stderr;

    public int $expected_code;
    public ?int $returned_code;
    public ?bool $output_same;

    public function __construct(string $path, string $name) {
        $this->stdout_path = "$path/$name.tmpout";
        $this->stderr_path = "$path/$name.tmperr";

        $this->expected_code = intval(file_get_contents("$path/$name.rc"));
    }

    public function clean() {
        $this->stdout = file_get_contents($this->stdout_path);
        $this->stderr = file_get_contents($this->stderr_path);
        @unlink($this->stdout_path);
        @unlink($this->stderr_path);
    }
}
