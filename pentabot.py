#!/usr/bin/python
# -*- coding: utf-8 -*-

# a simple Jabber Bot serving pentamedia to you and your news to pentamedia


from jabberbot import JabberBot, botcmd
import ConfigParser
import logging
import botcommands
import inspect
import types

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


class pentaBot(JabberBot):
    """
    pentabot
    It shall server you at your fingertips. And you shall serve him. With News for pentaradio.
    For more info: http://github.com/koeart/pentabot
    koeart <at remove this> zwoelfelf <this as well> <net>
    """

    def __init__( self, jid, password, res = None, debug=False, command_prefix=''):
        super( pentaBot, self).__init__( jid, password, res, debug, command_prefix=command_prefix)
        if debug:
            chandler = logging.StreamHandler()
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            chandler.setFormatter(formatter)
            self.log.addHandler(chandler)
            self.log.setLevel(logging.DEBUG)

        self._reload()

    def _reload(self):
        for name, value in inspect.getmembers(botcommands):
            if hasattr(getattr(botcommands, name), '__call__') and getattr(value, '_jabberbot_command', False):
                setattr(self, name, types.MethodType(value, self, self.__class__))
                setattr(value, '_botcmd', True)
        for name, value in inspect.getmembers(self):
            if getattr(value, '_botcmd', False) and name not in [x[0] for x in inspect.getmembers(botcommands)]:
                delattr(self, name)
        self.commands = {}
        for name, value in inspect.getmembers(self, inspect.ismethod):
            if getattr(value, '_jabberbot_command', False):
                name = getattr(value, '_jabberbot_command_name')
                self.log.info('Registered command: %s' % name)
                self.commands[self._JabberBot__command_prefix + name] = value


    @botcmd
    def reload(self, msg, args):
        for attr in dir(botcommands):
            if attr not in ('__name__', '__file__'):
                delattr(botcommands, attr)
        reload(botcommands)
        self._reload()


if __name__ == "__main__":
    #start Server
    while True:
        pentabot = pentaBot(secret.get('pentaBotSecret', 'username'), secret.get('pentaBotSecret', 'password'), secret.get('pentaBotSecret', 'resource'), bool(secret.get('pentaBotSecret', 'debug')), command_prefix='!')
        lChan = config.get("muc", "chan").split(',')
        lNick = config.get("muc", "name").split(',')
        for _int in range(0, len(lChan)):
           pentabot.join_room(lChan[_int], lNick[0] if len(lNick) == 1 else lNick[_int])
        pentabot.serve_forever()

