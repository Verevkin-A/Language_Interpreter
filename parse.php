<?php
ini_set('display_errors', 'stderr');

while ($line = fgets(STDIN)) {
    echo $line;
}

//$line = trim(explode("#", $line)[0]);
//if ($line == "") continue;