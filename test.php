<?php

function test(){
    #header("Content-type: application/json");
    $url = "http://192.168.64.1:5001/chain";
    $html = file_get_contents($url);
    $html_php = json_decode($html);
#$url_chain = "http://192.168.64.1:5001/chain_number";
#$html_num = file_get_contents($url_chain);
#$chain_num = json_decode($html_num);
    $diary_num = $html_php->length - 1;
#print_r($html_php);
    for ($num=1; $num <= $diary_num; $num++)
    {
        $diary = $html_php->chain[$num]->transactions[0]->diary[0];
        echo $diary;
        echo "<br>";

    }
}
function test2(){
    $zouni = "nihao";
    print $zouni;
}
?>

<!DOCTYPE html>

<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>test</title>
</head>
<body>
<p><?php test()?></p>
</body>
</html>
