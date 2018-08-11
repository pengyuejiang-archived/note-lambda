<?php
header('Content-type: application/json');

function do_post($url, $params, $headers) {
    $ch = curl_init ();
    curl_setopt ( $ch, CURLOPT_URL, $url );
    curl_setopt ( $ch, CURLOPT_RETURNTRANSFER, 1 );
    curl_setopt ( $ch, CURLOPT_CUSTOMREQUEST, 'POST' );
    curl_setopt ( $ch, CURLOPT_POSTFIELDS, $params );
    curl_setopt ( $ch, CURLOPT_HTTPHEADER, $headers );
    curl_setopt ( $ch, CURLOPT_TIMEOUT, 60 );
    $result = curl_exec ( $ch );
    curl_close ( $ch );
    return $result;
}

$url="http://192.168.64.1:5001/transactions/new";
$params=array(
    'user'=>array('ggggg'), 'diary'=>array('你好！你怎么样？'));
$headers=array(
    "Content-Type:application/json",
);
//json序列化
$params=json_encode($params);
$result=do_post($url,$params,$headers);
echo $result;
?>
