#!/usr/bin/python
from jabberbot import JabberBot, botcmd
import ConfigParser
import feedparser
# Configuration
configfile = ".pentabot.conf"
config = ConfigParser.RawConfigParser()
config.read([configfile, configfile])

config_help= {}
config_help['lastrss']= "\n".join(dict(config.items('RSS')).keys())



def format_help(fun):
        fun.__doc__ = fun.__doc__.format(config_help)
        return fun

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

        @format_help
        @botcmd
        def last( self, mess, args):
                '''
                letzte Episode
                Moegliche Eingaben:
                {lastrss}
                '''

                f = feedparser.parse('http://c3d2.de/' + args + '.xml').get('entries')[0]
                return(
                'Titel: ' + f.get('title') + '\n' +
                'URL:' + f.get('link') + '\n'
                )

#start Server
pentabot = pentaBot(config.get('pentaBotConf', 'username'), config.get('pentaBotConf', 'password'))

pentabot.serve_forever()
