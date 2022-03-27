<?php
/**
 * IPPcode22 create html results page
 * @author Aleksandr Verevkin (xverev00), VUT FIT IPP 2021/2022
 */

final class CreateHTML
{
    private DOMDocument $dom;
    private DOMElement $html;

    public function __construct() {
        $this->dom = new DOMDocument("1.0", "UTF-8");
        $this->dom->formatOutput = true;

        $this->html = $this->dom->createElement("html");
        $this->html->setAttribute("lang", "en");
        $this->dom->appendChild($this->html);

        $this->create_head();
        $this->create_body();
    }

    private function create_head() {
        $head = $this->dom->createElement("head");

        $meta = $this->dom->createElement("meta");
        $meta->setAttribute("charset", "UTF-8");
        $head->appendChild($meta);

        $title = $this->dom->createElement("title", "Test results");
        $head->appendChild($title);

        $this->html->appendChild($head);
    }

    private function create_body() {
        $body = $this->dom->createElement("body");

        $heading = $this->dom->createElement("h1", "Test results");
        $body->appendChild($heading);

        $table = $this->dom->createElement("table");
        $body->appendChild($table);

        $this->html->appendChild($body);
    }

    public function get_html(): string {
        return "<!DOCTYPE html>\n" . $this->dom->saveHTML();
    }
}
