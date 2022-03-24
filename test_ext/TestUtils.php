<?php
/**
 * IPPcode22 utilities
 * @author Aleksandr Verevkin (xverev00), VUT FIT IPP 2021/2022
 */

/**
 * Class with test utilities
 */
final class TestUtils
{
    // errors
    const PARAM_ERR = 10;
    const BAD_DIR = 41;

    /**
     * Print error message and exit program with given return code
     *
     * @param int $err error code
     * @param string $msg error message
     */
    function error(int $err, string $msg) {
        fwrite(STDERR, "Error: " . $msg . "\n");
        exit($err);
    }
}
