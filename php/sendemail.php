<?php
    $url = "https://192.168.88.75:3687/api/PaaS/1.0/email/overDeadline";

    $options = array(
        "ssl"=>array(
            "verify_peer"=>false,
            "verify_peer_name"=>false,
        ),
    );
    $context = stream_context_create($options);
    $result = file_get_contents($url, false, $context);
    $Arr = json_decode($result, true);
    #echo json_encode($Arr); //以json丟回前端
?>