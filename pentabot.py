#!/usr/bin/python
# -*- coding: utf-8 -*-

# a simple Jabber Bot serving pentamedia to you and your news to pentamedia


from jabberbot import JabberBot, botcmd
import ConfigParser
import feedparser

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
    def helloworld( self, mess, args):
        """ Hello World, the botway"""
        return 'Hello World, the botway'
    @botcmd
    def echo( self, mess, args):
        '''ein echo fuer die welt'''
        print mess
        print args
        return args

    @format_help
    @botcmd
    def last( self, mess, args):
        '''
        letzte Episode
        Moegliche Eingaben:
        {lastrss}
        '''
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
    pentabot = pentaBot(secret.get('pentaBotConf', 'username'), secret.get('pentaBotConf', 'password'), secret.get('pentaBotConf', 'resource'), bool(secret.get('pentaBotConf', 'debug')))
    pentabot.serve_forever()
