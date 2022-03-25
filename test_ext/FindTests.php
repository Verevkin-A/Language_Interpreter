<?php
/**
 * IPPcode22 searching tests in directory
 * @author Aleksandr Verevkin (xverev00), VUT FIT IPP 2021/2022
 */

require_once "ParseArgs.php";
require_once "TestItem.php";

final class FindTests
{
    public ParseArgs $args;
    // define test array
    public array $tests = [];

    public function __construct(ParseArgs $args) {
        $this->args = $args;
    }

    public function find_tests(string $dir) {
        // check each file in directory
        foreach (scandir($dir) as $file) {
            // pass system paths
            if ($file == "." or $file == "..") {
                continue;
            }
            $full_path = "$dir/$file";
            // check if file is directory
            if (is_dir($full_path)) {
                // check if recursive argument was set
                if ($this->args->recursive) {
                    $this->find_tests($full_path);  // recursive search of tests
                }
                continue;
            }
            // get file info
            $path_parts = pathinfo($file);
            // find all testing sources
            if (key_exists("extension", $path_parts)) {
                if (in_array($path_parts["extension"], ["src", "in", "out", "rc"])) {
                    // check if test case already exist
                    if (key_exists($path_parts["filename"], $this->tests)) {
                        $test_item = $this->tests[$path_parts["filename"]];
                    } else {
                        $test_item = new TestItem($path_parts["filename"], $this->args);
                        $this->tests[$path_parts["filename"]] = $test_item;
                    }
                    // save test file into his test case
                    switch ($path_parts["extension"]) {
                        case "src":
                            $test_item->src = realpath($full_path);
                            break;
                        case "in":
                            $test_item->in = realpath($full_path);
                            break;
                        case "out":
                            $test_item->out = realpath($full_path);
                            break;
                        case "rc":
                            $test_item->rc = realpath($full_path);
                            break;
                    }
                }
            }
        }
    }
}
