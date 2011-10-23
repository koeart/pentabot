#!/usr/bin/python
# -*- coding: utf-8 -*-

# a simple Jabber Bot serving pentamedia to you and your news to pentamedia


from jabberbot import JabberBot, botcmd
import ConfigParser
import feedparser
import datetime
import time
import urllib
import urllib2

# secret
secretfile = ".pentabot.login"
secret = ConfigParser.RawConfigParser()
secret.read([secretfile, secretfile])

# Configuration
configfile = "pentabot.conf"
config = ConfigParser.RawConfigParser()
config.read([configfile, configfile])

# feed dict
feed_help= {}
feed_help['lastrss']= "\n".join(dict(config.items('RSS')).keys())

def format_help(fun):
    fun.__doc__ = fun.__doc__.format(**feed_help) #** dict entpacken, * listen entpacken 
    return fun

class pentaBot(JabberBot):
    """
    pentabot. It shall server you at your fingertips. And you shall serve him. With News for pentaradio.
    For more info: http://github.com/koeart/pentabot
    koeart <at remove this> zwoelfelf <this as well> <net>
    """

    @botcmd
    def serverinfo( self, mess, args):
        """Zeige Informationen ueber den Server"""
        version = open('/proc/version').read().strip()
        loadavg = open('/proc/loadavg').read().strip()

        return '%s\n\n%s' % ( version, loadavg, )

    @botcmd
    def time( self, mess, args):
        """Zeige die aktuelle Server Zeit"""
        return str(datetime.datetime.now())

    @botcmd
    def rot13( self, mess, args):
        """Gibt <string> in rot13"""
        return args.encode('rot13')

    @botcmd
    def whoami( self, mess, args):
        """Zeigt dir dein Username"""
        return mess.getFrom().getStripped()

    @botcmd
    def roster( self, mess, args):
        """Wiedergabe der aktuellen Roster"""
        roster = ", ".join(self.conn.Roster.getItems())
        return roster

    @botcmd
    def group( self, mess, args):
        """
        Bearbeiten von Gruppen
        Benutze: group (add|del|list) jid <groups>
        """
        args = args.strip().split(' ')
        if len(args) <= 1:
            group = 'Bitte rufe \"help group\" fuer moegliche Optionen auf!'
        else:
            try:
                groups = self.conn.Roster.getGroups(args[1])
                group = "\n"
            except:
                group = "\n"
            if args[0] == "add":
                try:
                    groups.append(", ".join(args[2:]))
                    self.conn.Roster.setItem(args[1], None, groups)
                    group += "Fuege %s zu %s" % (args[1], ", ".join(groups))
                except:
                    group += "Beim gruppen erweitern trat ein Fehler auf!"
            elif args[0] == "del":
                if args[2] == "all":
                    try:
                        self.conn.Roster.setItem(args[1], None, [])
                        group += "Loesche %s von %s" % (args[1], ", ".join(groups))
                    except:
                        group += "Beim Loeschen von %s aus %s trat ein Fehler auf!" % (args[1], args[2])
                else:
                    if args[2] in groups:
                        groups.remove(args[2])
                        try:
                            self.conn.Roster.setItem(args[1], None, groups)
                            group += "Loesche %s von %s" % (args[1], args[2])
                        except:
                            group += "Beim Loeschen von %s aus %s trat ein Fehler auf!" % (args[1], args[2])
                    else:
                        group += "%s ist nicht in %s" % (args[1], args[2])
            elif args[0] == "list":
                list_group = ", ".join(groups)
                if not list_group:
                    group += "%s ist in keiner Gruppe" % args[1]
                else:
                    group += "%s ist in de{n,r} Gruppe(n) %s " % (args[1], list_group)
            else:
                group += "Befehl '%s' nicht gefunden!\n" % args[0]
                group += "Bitte rufe 'help group' fuer moegliche Optionen auf!"
        return group

    @botcmd
    def abfahrt( self, mess, args):
        args = args.strip().split(' ')
        if len(args) < 1:
            abfahrt = "Benutze: abfahrt <Haltestellenname>"
        else:
            abfahrt = ""
            if len(args) == 1:
                laufzeit = config.get("bot", "laufzeit")
            else:
                laufzeit = args[-1]
            values = {"ort": "Dresden",
                      "hst": " ".join(args[0:]),
                      "vz": laufzeit,
                      "timestamp": int(time.time())}

            url_values = urllib.urlencode(values)
            full_url = config.get("bot", "abfahrt_url") + "?" + url_values

            data = urllib2.urlopen(full_url)
            dare = data.read()
            dare = dare.replace("[[", "")
            dare = dare.replace("]]", "")

            abfahrt += "\n"
            abfahrt += "%6s %-19s %7s\n" % ("Linie", "Richtung", "Abfahrt")

            for line in dare.split("],["):
                outp = line.replace("\"", "").split(",")
                abfahrt += "%6s %-19s %7s\n" % (outp[0], outp[1], outp[2])

        return abfahrt

    @botcmd
    def join_chan( self, chan, name="PentaBot"):
        self.join_room(chan, name)

    @botcmd
    def helloworld( self, mess, args):
        """ Hello World, the botway"""
        return 'Hello World, the botway!'

    @botcmd
    def echo( self, mess, args):
        """ein echo fuer die welt"""
        return args

    @format_help
    @botcmd
    def last( self, mess, args):
        """
        Gibt die letzten News zu PentaCast, PentaRadio und PentaMusic wieder
        Moegliche Eingaben:
        {lastrss}
        """
        args = args.strip().split(' ')
        if args[0] in dict(config.items('RSS')).keys():
            message = "\n"
            if len(args) == 1:
                args.append('1')
            for loop in range(int(args[1])):
                f = feedparser.parse(config.get('RSS', args[0])).get('entries')[loop]
                message += 'Titel: ' + f.get('title') + '\n' + 'URL: ' + f.get('link') + '\n'
        else:
            message = 'Bitte rufe \"help last\" fuer moegliche Optionen auf!'
        return message

if __name__ == "__main__":
    #start Server
    while True:
        pentabot = pentaBot(secret.get('pentaBotConf', 'username'), secret.get('pentaBotConf', 'password'), secret.get('pentaBotConf', 'resource'), bool(secret.get('pentaBotConf', 'debug')))
        pentabot.join_room(config.get("muc", "chan"), config.get("muc", "name"))
        pentabot.serve_forever()
