<?php
$MDS_SERVER_IP = "172.16.161.125:9000";
$MDS_USER_INTERFACE = "http://" . $MDS_SERVER_IP . "/nusoap/IUser.php?wsdl";
$SSO_URL = "http://172.16.161.124";


//function generate_pwd ($username, $displayname) {
//      return substr(md5("qwer".$username."poiu"),-10);
//}

function jsr_user_add ($username, $displayname, $password) {
        $MDS_SERVER_IP = "172.16.161.125:9000";
        $client = new SoapClient("http://" . $MDS_SERVER_IP . "/nusoap/IUser.php?wsdl");
        # $password = substr(md5("qwer".$username."poiu"),-10);

        # this is old soap

        $r = $client->__soapCall('CreateUser', $parameters);
        print_r($password);
        print_r($r);
}

function jsr_user_del ($username) {
        $MDS_SERVER_IP = "172.16.161.125:9000";
        $client = new SoapClient("http://" . $MDS_SERVER_IP . "/nusoap/IUser.php?wsdl");
        $parameters = array('999999','999999',$username);
function jsr_user_update($username, $userpwd) {
        $MDS_SERVER_IP = "172.16.161.125:9000";
        $client = new SoapClient("http://" . $MDS_SERVER_IP . "/nusoap/IUser.php?wsdl");
        $password = substr(md5("qwer".$userpwd."OKMU"),-10);
        //$password = "123456";
        echo $password;
        $r = $client->__soapCall('SetUserInfo', $parameters);
        echo $r;
}

function jsr_user_add_test ($username) {
        $MDS_SERVER_IP = "172.16.161.125:9000";
        $client = new SoapClient("http://" . $MDS_SERVER_IP . "/nusoap/IUser.php?wsdl");
        $password = substr(md5("qwer".$username."poiu"),-10);
        $r = $client->__soapCall('CreateUser', $parameters);
        print_r($password);
        print_r($r);
}

/**
 * 将修改后的密码提交到sso服务器
 * @param array $employee
 */
function updatePwd ($uid, $pwd_new)
{
        $ext = array();
        $ext['jsy']=$pwd_new;
        $data = array();
        $data['userid']=$uid;
        $data['extInfo'] = json_encode($ext);
        $userdata=array();
        array_push($userdata,$data);
        // $url = Yii::app()->params["ssohost"]."/user/update";
        $SSO_URL = "http://172.16.161.124/user/update";

        curlPwd($userdata, $SSO_URL);
}

function curlPwd($userdata,$url)
{
        $ch = curl_init();

        $data = array();
        $data["userdata"]=$userdata;

        $post_data = array();
        $post_data["data"] = json_encode($data);
        curl_setopt($ch,CURLOPT_URL,$url);
        curl_setopt($ch,CURLOPT_POST, 1);
        curl_setopt($ch,CURLOPT_POSTFIELDS,$post_data);
        curl_setopt($ch,CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch,CURLOPT_CONNECTTIMEOUT ,3);
        curl_setopt($ch,CURLOPT_TIMEOUT, 20);
        $response = curl_exec($ch);
        print "curl response is:" . $response;
        curl_close ($ch);
        return json_decode($response);
}

# $argc $argv

print($argv[1]."--".$argv[2]."\n");

$username = $argv[1];
$displayname = $argv[2];
$userid = $argv[3];

//$pwd = generate_pwd($username, $displayname);
$pwd = substr(md5("qwer".$username."poiu"),-10);
jsr_user_add($username, $displayname, $pwd);
updatePwd($userid, $pwd);

?>
