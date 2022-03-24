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

$args_parser = new ParseArgs($argc);
$args_parser->set_params();

$tests = new FindTests($args_parser);
$tests->find_tests($args_parser->dir);
//print(count($tests->tests));


