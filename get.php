<?php
header("Content-type: application/json");

$url = "http://192.168.64.1:5001/chain";
$html = file_get_contents($url);
echo $html;
?>