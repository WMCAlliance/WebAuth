from quarry.net.server import ServerFactory, ServerProtocol
import MySQLdb
# ##
# ## AUTH SERVER
###   ask mojang to authenticate the user
###

HOST = "auth.yourserver.com"
PORT = 25565
MOTD = u"An awesome MOTD"
FAVICON = None  # or a path to a 64x64 .png


class AuthProtocol(ServerProtocol):
    def player_joined(self):
        # This method gets called when a player successfully joins the server.
        #   If we're in online mode (the default), this means auth with the
        #   session server was successful and the user definitely owns the
        #   username they claim to.

        # Call super. This switches us to "play" mode, marks the player as
        #   in-game, and does some logging.
        ServerProtocol.player_joined(self)
        authed = "true"
        # Define your own logic here. It could be an HTTP request to an API,
        #   or perhaps an update to a database table.
        username = self.username
        ip_addr = self.recv_addr.host
        self.logger.info("[%s authed with IP %s]" % (username, ip_addr))

        # MYSQL Here
        db = MySQLdb.connect(host="localhost", user="user", passwd="pass", db="database")
        user = db.cursor()
        verified = db.cursor()
        hours = db.cursor()
        ip = db.cursor()
        full = db.cursor()

        if authed == "true":
            print " --> OK!"
            user.execute("SELECT * FROM wp_auth_players where username = '" + username + "'")
            ip.execute(
                "SELECT * FROM wp_auth_players where username = '" + username + "' and address <> '" + ip_addr + "'")
            verified.execute("SELECT * FROM wp_auth_players where username = '" + username + "' and verified = 1")
            #hours.execute("SELECT * FROM wp_auth_players where username = '" + username + "' and time < DATE_ADD(NOW(), INTERVAL 1 HOUR)")
            full.execute(
                "SELECT * FROM wp_auth_players where username = '" + username + "' and address = '" + ip_addr + "' and verified = 0")
            print "Found %s entries" % full.rowcount
            if full.rowcount == 1:
                sql = "UPDATE wp_auth_players SET verified = '1' where username = '" + username + "' and address = '" + client_addr + "' and verified = '0'"
                try:
                    full.execute(sql)
                    db.commit()
                except:
                    db.rollback()
                print "The user has been verified"
                message = u"\u00A7eGood to see you own this account \u00A76" + username + u"\u00A7e!\n \u00A7eNow just click \u00A76Next\u00A7e on the website!"
            elif user.rowcount == 0:
                print "The user has NOT been verified (doesn't exist)"
                message = u"\u00A7eSorry \u00A76" + username + u"\u00A7e, apparently you haven't tried registering yet!\nVisit http://yoursite.com/register to begin the process."
            elif ip.rowcount == 1:
                print "The user has NOT been verified (different ip)"
                message = u"\u00A7eSorry \u00A76" + username + u"\u00A7e, it looks like you're connecting from a different IP!\nIf this is incorrect, contact a staff member."
            elif verified.rowcount == 1:
                print "The user is already verified"
                message = u"\u00A7eHold on \u00A76" + username + u"\u00A7e, it looks like you've already been authenticated!\nIf this is incorrect, contact a staff member."
            #elif hours.rowcount == 1: # this will be done soon!
            #    print "The user has NOT been verified (too late)"
            #    return u"\u00A7eSorry \u00A76" + username + u"\u00A7e, it looks like you've taken too long!\nTry again tomorrow, without waiting over an hour."
            else:
                print "Overall else"
                message = u"\u00A7eWhoops, something went horribly wrong. Contact WizardCM!"
            db.close()
        else:
            print " --> FAILED!"
            message = u"\u00A74Are you sure you own this account (" + username + u")? Try restarting your game!\n(this doesn't actually do anything yet, but it will!)"

        # Kick the player.
        self.close(message)


class AuthFactory(ServerFactory):
    protocol = AuthProtocol


def main(args):
    # Create factory
    factory = AuthFactory()
    factory.motd = MOTD
    factory.favicon_path = FAVICON

    # Listen
    factory.listen(HOST, PORT)
    factory.run()