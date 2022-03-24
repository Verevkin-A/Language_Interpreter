<?php
/**
 * IPPcode22 single test instance
 * @author Aleksandr Verevkin (xverev00), VUT FIT IPP 2021/2022
 */

final class TestItem
{
    // test case info and paths to files
    public string $name;
    public string $src;
    public string $in;
    public string $out;
    public string $rc;

    public function __construct(string $name) {
        $this->name = $name;
    }
}