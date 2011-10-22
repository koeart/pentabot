#!/usr/bin/python
# -*- coding: utf-8 -*-

# a simple Jabber Bot serving pentamedia to you and your news to pentamedia


from jabberbot import JabberBot, botcmd
import ConfigParser
import feedparser

#secret
secretfile = ".pentabot.login"
secret = ConfigParser.RawConfigParser()
secret.read([secretfile, secretfile])

# Configuration
configfile = "pentabot.conf"
config = ConfigParser.RawConfigParser()
config.read([configfile, configfile])

config_help= {}
config_help['lastrss']= "\n".join(dict(config.items('RSS')).keys())



def format_help(fun):
        fun.__doc__ = fun.__doc__.format(**config_help) #** dict entpacken, * listen entpacken 
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

                if args in dict(config.items('RSS')).keys():

                        f = feedparser.parse(config.get('RSS', args)).get('entries')[0]
                        message = 'Titel: ' + f.get('title') + '\n' + 'URL: ' + f.get('link') + '\n'
                else:
                        message = 'Bitte rufe \"help last\" fuer moegliche Optionen auf!'
                return(
                message
                )

#start Server
pentabot = pentaBot(secret.get('pentaBotConf', 'username'), secret.get('pentaBotConf', 'password'))

pentabot.serve_forever()
