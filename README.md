WebAuth
========

This is a collection of scripts that power the authentication on [The Worldwide Minecraft Alliance](http://wma.im/register). Huge thanks to @barneygale, @BoomBox for proving scripts and support to get this all working perfectly!

Within standalone-python-server/ you will find purposefully modified files from [this auth server](https://github.com/barneygale/authserver) by @barneygale.

Within web-forms/ you will find three purpose-built scripts. These will create entries in a MySQL database which is then accessed by the python server.

Below is the basic MySQL command to create a table for the above scripts to use.

    CREATE TABLE IF NOT EXISTS `wp_auth_players` (
      `username` varchar(16) NOT NULL,
      `address` varchar(100) NOT NULL,
      `time` datetime NOT NULL,
      `verified` tinyint(1) NOT NULL DEFAULT '0',
      UNIQUE KEY `username` (`username`)
    )

Create your own if you wish, but that's how ours looks.
