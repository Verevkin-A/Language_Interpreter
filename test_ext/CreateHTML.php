<?php
/**
 * IPPcode22 create html results page
 * @author Aleksandr Verevkin (xverev00), VUT FIT IPP 2021/2022
 */

/**
 * Class for creating HTML results page
 */
final class CreateHTML
{
    // define html document and his main element
    private DOMDocument $dom;
    private DOMElement $html;
    
    private const CENTER_ALIGN = "text-align:center";
    // css styles
    private const STYLES = "
            body {
                background: #B9D0EA;
                font-family: fantasy;
                color: #0E3F60;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 10px;
            }
            th {
                border: 1px solid;
            }
            td {
                border: 1px solid;
                padding-left: 21px;
                padding-right: 21px;
            }
            .right {
                background-color: #6BCB77;
            }
            .wrong {
                background-color: #FF6B6B;
            }
            ";

    /**
     * CreateHTML constructor
     *
     * @param array $test_results
     */
    public function __construct(array $test_results) {
        $this->dom = new DOMDocument("1.0", "UTF-8");
        $this->dom->formatOutput = true;
        // create html header
        $this->html = $this->dom->createElement("html");
        $this->html->setAttribute("lang", "en");
        $this->dom->appendChild($this->html);
        // create html parts
        $this->create_head();
        $this->create_body($test_results);
    }

    /**
     * Create and attach html head element
     */
    private function create_head() {
        $head = $this->dom->createElement("head");

        $meta = $this->dom->createElement("meta");
        $meta->setAttribute("charset", "UTF-8");
        $head->appendChild($meta);
        // page title
        $title = $this->dom->createElement("title", "Results");
        $head->appendChild($title);
        // css styles element
        $style = $this->dom->createElement("style", $this::STYLES);
        $head->appendChild($style);

        $this->html->appendChild($head);
    }

    /**
     * Create and attach html body element
     *
     * @param array $test_results all tests results
     */
    private function create_body(array $test_results) {
        $body = $this->dom->createElement("body");
        // get amount of passed tests
        $passed = count(array_filter($test_results, function (TestResult $res) {
            return $res->test_result;
        })) . "/" . count($test_results);
        // header
        $heading = $this->dom->createElement("h1", "Test results ($passed passed)");
        $heading->setAttribute("style", $this::CENTER_ALIGN);
        $body->appendChild($heading);
        // results table
        $table = $this->dom->createElement("table");
        $table->appendChild($this->get_table_header());
        // write tests entries into table
        foreach ($test_results as $result) {
            $table->appendChild($this->get_result_row($result));
        }
        $body->appendChild($table);

        $this->html->appendChild($body);
    }

    /**
     * Create first, heading row of the table
     *
     * @return DOMElement first row
     */
    private function get_table_header(): DOMElement {
        // create and set up first, heading row
        $row = $this->dom->createElement("tr");
        $row_header_name = $this->dom->createElement("th", "Test name");
        $row_header_result = $this->dom->createElement("th", "Result");
        $row_header_expected = $this->dom->createElement("th", "Expected code");
        $row_header_returned = $this->dom->createElement("th", "Returned code");
        $row_header_error = $this->dom->createElement("th", "Returned error");
        $row_header_output = $this->dom->createElement("th", "Outputs same");
        $row->appendChild($row_header_name);
        $row->appendChild($row_header_result);
        $row->appendChild($row_header_expected);
        $row->appendChild($row_header_returned);
        $row->appendChild($row_header_error);
        $row->appendChild($row_header_output);
        return $row;
    }

    /**
     * Format test result into table row
     *
     * @param TestResult $result single test result
     * @return DOMElement row element with formatted result into it
     */
    private function get_result_row(TestResult $result): DOMElement {
        // declare if outputs are same
        if (isset($result->output_same)) {
            $output_entry = $result->output_same ? "Yes" : "No";
        } else {
            $output_entry = "-";
        }
        // declare overall result
        if (!$result->test_result) {
            if ($result->expected_code == $result->returned_code) {
                if (!$result->output_same) {
                    $result_entry = "Different outputs";
                } else {
                    $result_entry = "Other error";
                }
            } else {
                $result_entry = "Different return codes";
            }
        } else {
            $result_entry = "Pass";
        }
        // row element
        $row = $this->dom->createElement("tr");
        $row->setAttribute("class", $result->test_result ? "right" : "wrong");
        // name column
        $name = $this->dom->createElement("td");
        $name->appendChild($this->dom->createTextNode("Name: $result->test_name"));
        $name->appendChild($this->dom->createElement("br"));
        $name->appendChild($this->dom->createTextNode("Path: $result->test_path"));
        // other columns
        $test_res = $this->dom->createElement("td", $result_entry);
        $test_res->setAttribute("style",$this::CENTER_ALIGN);
        $expected = $this->dom->createElement("td", "$result->expected_code");
        $expected->setAttribute("style",$this::CENTER_ALIGN);
        $returned = $this->dom->createElement("td", "$result->returned_code");
        $returned->setAttribute("style",$this::CENTER_ALIGN);
        $error = $this->dom->createElement("td", $result->stderr ?: "-");
        $output = $this->dom->createElement("td", $output_entry);
        $output->setAttribute("style",$this::CENTER_ALIGN);
        // connect all td elements to tr element
        $row->appendChild($name);
        $row->appendChild($test_res);
        $row->appendChild($expected);
        $row->appendChild($returned);
        $row->appendChild($error);
        $row->appendChild($output);

        return $row;
    }

    /**
     * Return html page of the tests results
     *
     * @return string html page
     */
    public function get_html(): string {
        return "<!DOCTYPE html>\n" . $this->dom->saveHTML();
    }
}
