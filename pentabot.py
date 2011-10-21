#!/usr/bin/python
from jabberbot import JabberBot, botcmd
import ConfigParser
import feedparser
# Configuration
configfile = ".pentabot.conf"
config = ConfigParser.RawConfigParser()
config.read([configfile, configfile])

class pentaBot(JabberBot):
        """
        pentabot. It shall server you at your fingertips. And you shall serve him. With News for pentaradio.
        For more info: http://github.com/koeart/pentabot
        koeart <at remove this> zwoelfelf <this as well> <net>
        """

        @botcmd
        def helloworld( self, mess, args):
                """ Hello World, the botway"""
                return 'Hello World, the botway'
        @botcmd
        def echo(self,mess,args):
                '''ein echo fuer die welt'''
                return args

        @botcmd
        def last( self, mess, args):
                '''
                letzte Episode
                Moegliche Eingaben:
                pentacast
                pentaradio
                pentamusic
                '''
                f = feedparser.parse('http://c3d2.de/' + args + '.xml').get('entries')[0]
                return(
                'Titel: ' + f.get('title') + '\n' +
                'URL: ' + f.get('link') + '\n'
                )

#start Server
pentabot = pentaBot(config.get('pentaBotConf', 'username'), config.get('pentaBotConf', 'password'))

pentabot.serve_forever()
