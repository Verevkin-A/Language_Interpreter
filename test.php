<?php
/**
 * IPPcode22 test script
 * @author Aleksandr Verevkin (xverev00), VUT FIT IPP 2021/2022
 */

require_once "test_ext/ParseArgs.php";
require_once "test_ext/TestUtils.php";
require_once "test_ext/FindTests.php";

// setting to show errors on stderr
ini_set('display_errors', 'stderr');
// process arguments
$args_parser = new ParseArgs($argc);
$args_parser->set_params();
// process tests
$tests = new FindTests($args_parser);
$tests->find_tests($args_parser->dir);
// execute tests
$tests_results = [];
foreach ($tests->tests as $name => $test) {
    if (!$test->set_test()) {
        continue;
    }
    $tests_results[$name] = $test->run_parser_test();

    if (!$args_parser->noclean) {
        $tests_results[$name]->clean();
    }
//    print($tests_results[$name]->returned_code."/".$tests_results[$name]->expected_code."\n");
}
//var_dump($tests_results);

