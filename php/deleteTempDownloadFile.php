<?php
    $this_crontab = $argv[1];
    $url = "https://192.168.88.75:3687/api/PaaS/1.0/Customized/Check/Delete/DownloadFiles/Deadline/".$this_crontab."?uid=@sapido@PaaS";

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