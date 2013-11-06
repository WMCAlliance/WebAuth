<?php
$user = $_GET['username'];
if (!(strlen($user) == NULL)) {
echo('<style>#start-form { display: none }</style>');
		// Create connection
		$con = mysqli_connect("localhost", "user", "pass", "database");
		date_default_timezone_set('Australia/Melbourne');
		$date = date('Y-m-d H:i:s');
		$ip = $_SERVER['REMOTE_ADDR'];
		
		// Check connection
		if ( mysqli_connect_errno($con) )
		{
			echo("Failed to connect to MySQL: " . mysqli_connect_error());
		}
		else
		{
			// insert something
			$insert_sql = "INSERT INTO wp_auth_players (username, address, time) VALUES ('$user', '$ip', '$date')";
			if ( !mysqli_query($con, $insert_sql) )
			{
				echo("It seems you already tried to register. Skip forward a step!");
				echo("<form name='step3' method='get' action='/register/step-3/'>");
				echo("<input type='text' name='username' id='username' class='input' value='$user' size='18' maxlength='16' style='display:none' />");
				echo("<input type='submit' value='Next'/>");
				echo("</form>");
			}
			else {
				echo("Now for the fun part. Open up your game, and connect to <strong>auth.myserver.com</strong><br />");
				echo("When you're done, hit Next!");
				echo("<form name='step3' method='get' action='/register/step-3/'>");
				echo("<input type='text' name='username' id='username' class='input' value='$user' size='18' maxlength='16' style='display:none' />");
				echo("<input type='submit' value='Next'/>");
				echo("</form>");
			}
			// close connection
			mysqli_close($con);
		}
}
?>