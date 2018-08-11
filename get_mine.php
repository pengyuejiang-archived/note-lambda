<?php
header("Content-type: application/json");

$url = "http://192.168.64.1:5001/mine";
$html = file_get_contents($url);
$response = json_decode($html);
$message = $response->message;
print_r($message) ;
?>
