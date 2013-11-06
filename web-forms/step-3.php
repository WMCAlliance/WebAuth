<style>#theme-my-login1 { display: none } #registerform1 p:first-child, .login .message, .post-entry > p:nth-child(odd), .post-entry > p:nth-child(4) { display: none } .post-entry > p { margin-bottom: 0 !important }</style>
<?php
$user = $_GET['username'];
if (!(strlen($user) == NULL)) {
		// Create connection
		$con = mysqli_connect("localhost", "user", "pass", "database");
		$ip = $_SERVER['REMOTE_ADDR'];
		
		// Check connection
		if ( mysqli_connect_errno($con) )
		{
			echo("Failed to connect to MySQL: " . mysqli_connect_error());
		}
		else
		{
			// read something
			$fetch_sql = "SELECT * FROM wp_auth_players WHERE username = '$user' and verified = 1";
			$result = mysqli_query($con, $fetch_sql);
			if ( count(mysqli_fetch_array($result)) > 0 )
			{
			echo("Thank you for proving that you own the <strong>$user</strong> Minecraft account. Just do the steps below to finish making the account!");
			echo("<style>#theme-my-login1 { display: block } #registerform1 p:first-child, .login .message { display: none }</style>");
			}
			else {
				echo("Oops, we couldn't prove that you own this account. Try connecting to  <strong>auth.wma.im:25560</strong> again.<br />");
				echo("When you're done, hit Retry!");
				echo("<form name='step3' method='get' action='/register/step-3/'>");
				echo("<input type='text' name='username' id='username' class='input' value='$user' size='18' maxlength='16' style='display:none' />");
				echo("<input type='submit' value='Retry'/>");
				echo("</form>");
			}
			// close connection
			mysqli_close($con);
		}
}
?>

[theme-my-login default_action="register"]
<script>function $_GET( name ){
  name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp( regexS );
  var results = regex.exec( window.location.href );
  if( results == null )
    return "";
  else
    return results[1];
}
document.getElementById('user_login1').value = $_GET('username'); </script>