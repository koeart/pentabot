#!/usr/bin/python
# -*- coding: utf-8 -*-

# a simple Jabber Bot serving pentamedia to you and your news to pentamedia


from jabberbot import JabberBot, botcmd
# das was man nicht tun sollte "*"
from types import *
import ConfigParser
import feedparser
import datetime
import time
import urllib
import urllib2
import sys
import os
import json
import requests

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

elbabsaufer = dict()

#fridge
fridge = {}
message =""
def open_fridge(product, action, amount):
        if (not(fridge.has_key(product)) and action != "sub"):
            fridge.update({product : 0})
            add_product(product)
        else:
            if action == "show":
                message = fridge.viewitems()
            if action == "add":
                for i in range(amount):
                    add_product(product)
            elif action == "sub":
                for i in range(amount):
                    sub_product(product)
            else:
                message = "Bitte sub oder add ein Produkt! Oder lass es dir mit show zeigen"
        return message

        def add_product(product):
            fridge[product] += 1
            message = "Produkt hinzugefuegt"
            return message

        def sub_product(product):
            if fridge[product] >= 1:
                fridge[product] -= 1
                message = "Produkt rausgenommen"
            else:
                message = "Fridge leer!"
            return message


def format_help(fun):
    fun.__doc__ = fun.__doc__.format(**feed_help) #** dict entpacken, * listen entpacken 
    return fun

def test(fun):
        def wrapper(self, mess, args):
            fun(self,mess,args)
        return wrapper


class pentaBot(JabberBot):
    """
    pentabot. It shall server you at your fingertips. And you shall serve him. With News for pentaradio.
    For more info: http://github.com/koeart/pentabot
    koeart <at remove this> zwoelfelf <this as well> <net>
    """

    def _checkGroup(self, jid, group):
        """
        Gibt Gruppenzugehoerigkeit als Bool
        """
        if group in self.conn.Roster.getGroups(jid):
            return True
        else:
            return False

    def _listGroup(self, jid):
        """
        Gibt eine liste der Gruppen wieder
        """
        try:
            return self.conn.Roster.getGroups(jid)
        except:
            return None

    def _groupList(self, mess, groups, args):
        if args [1] == "existing" and  self._checkGroup(mess.getFrom().getStripped(), config.get("group", "admin")):
            existing = []
            for x in self.conn.Roster.getItems():
                if self.conn.Roster.getGroups(x):
                    if type(self.conn.Roster.getGroups(x)) is ListType:
                        for y in self.conn.Roster.getGroups(x):
                            existing.append(y)
                    else:
                        existing.append(self.conn.Roster.getGroups(x))
            ab = {}
            for z in existing:
                ab[z] = ''
            existing = ab.keys()
            existing.sort()
            _groupList = "Die bisher existierenden Gruppen sind: %s" % ", ".join(existing)
        else:
            if groups:
                list_group = ", ".join(groups)
                if not list_group:
                    _groupList = "%s ist in keiner Gruppe" % args[1]
                else:
                    _groupList = "%s ist in de{n,r} Gruppe(n) %s " % (args[1], list_group)
            else:
                _groupList = "Bitte rufe 'help group' fuer moegliche Optionen auf!"
        return _groupList

    def _groupAdd(self, groups, args):
        try:
            groups.append(", ".join(args[2:]))
            self.conn.Roster.setItem(args[1], None, groups)
            _groupAdd = "Fuege %s zu %s" % (args[1], ", ".join(groups))
        except:
            _groupAdd = "Beim gruppen erweitern trat ein Fehler auf!"
        return _groupAdd

    def _groupDel(self, groups, args):
        if args[2] == "all":
            try:
                self.conn.Roster.setItem(args[1], None, [])
                _groupDel = "Loesche %s von %s" % (args[1], ", ".join(groups))
            except:
                _groupDel = "Beim Loeschen von %s aus %s trat ein Fehler auf!" % (args[1], args[2])
        else:
            if args[2] in groups:
                groups.remove(args[2])
                try:
                    self.conn.Roster.setItem(args[1], None, groups)
                    _groupDel = "Loesche %s von %s" % (args[1], args[2])
                except:
                    _groupDel = "Beim Loeschen von %s aus %s trat ein Fehler auf!" % (args[1], args[2])
            else:
                _groupDel = "%s ist nicht in %s" % (args[1], args[2])
        return _groupDel

    @test
#    @botcmd(hidden=True)
    def testen(self,mess,args):
        return args

    @botcmd
    def fridge(self, mess, args):
        """ Fridge
            
            open_fridge(product, action, amount)
            action = add or sub or show
        """
        args = args.strip().split(' ')

        open_fridge(args[0], args[1], args[2])
        return message

    @botcmd
    def fortune(self, mess, args):
        '''Fortune Cookie for you

        A Cookie you can trust and accept.
        Just run fortune
        '''
        fortune = ''
        try:
            fortune += os.popen('/usr/games/fortune').read()
        except:
            fortune += 'Your fortune unforseeable'
        return ('Your Cookie reads:\n' + fortune)

    @botcmd
    def ddate(self, mess, args):
        '''ddate
        '''
        args = args.strip().split(' ')
        ddate = ''
        if len(args) <= 1 :
            ddate += os.popen('/usr/bin/ddate').read()
        elif len(args) == 3:
            ddate += os.popen('/usr/bin/ddate '+str(int(args[0]))+' '+ str(int(args[1]))+' '+ str(int(args[2]))).read()
        else:
            ddate = 'You are not using correctly!\n Just enter ddate or append day month year'
        return ddate


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
        if mess.getType() == "groupchat":
            return str(mess.getFrom()).split("/")[1]
        else:
            return mess.getFrom().getStripped()

    @botcmd
    def roster( self, mess, args):
        """Wiedergabe der aktuellen Roster"""
        if self._checkGroup(mess.getFrom().getStripped(), config.get("group", "admin")):
            roster = ", ".join(self.conn.Roster.getItems())
        elif mess.getFrom().getStripped() != config.get("muc", "chan"):
            if mess.getFrom().getStripped() in self.conn.Roster.getItems():
                if self._listGroup(mess.getFrom().getStripped()):
                    roster = "Hallo %s, du bist in" % mess.getFrom().getStripped(), self._listGroup(mess.getFrom().getStripped())
                else:
                    roster = "Hallo %s, du bist noch in keiner Gruppe" % mess.getFrom().getStripped()
            else:
                roster = "Hallo %s, ich kenn dich noch nicht!" % mess.getFrom().getStripped()
        else:
            roster = "Please PM!"
        return roster

    @botcmd
    def group( self, mess, args):
        """
        Bearbeiten von Gruppen
        Benutze: group (add|del|list) jid <groups>
        """
        args = args.strip().split(' ')
        if len(args) <= 1:
            group = "Bitte rufe \"help group\" fuer moegliche Optionen auf!"
        else:
            group = "\n"
            if self._listGroup(args[1]) and args[1] != "existing":
                groups = self._listGroup(args[1])
            else:
                groups = ""
            if args[0] == "add" and self._checkGroup(mess.getFrom().getStripped(), config.get("group", "admin")):
                group += self._groupAdd(groups, args)
            elif args[0] == "del" and self._checkGroup(mess.getFrom().getStripped(), config.get("group", "admin")):
                group += self._groupDel(groups, args)
            elif args[0] == "list":
                group += self._groupList(mess, groups, args)
            else:
                group += "Befehl '%s' nicht gefunden!\n" % args[0]
                group += "Bitte rufe 'help group' fuer moegliche Optionen auf!"
        return group

    @botcmd
    def abfahrt( self, mess, args):
        """
        Abfahrtsmonitor
        Benutze: abfahrt <Haltestellenname>
        """
        args = args.strip().split(' ')
        if len(args) < 1:
            abfahrt = "Benutze: abfahrt <Haltestellenname>"
        else:
            abfahrt = ""
            if len(args) == 1:
                laufzeit = config.get("abfahrt", "laufzeit")
                haltestelle = " ".join(args[0:])
            else:
                laufzeit = args[-1]
                haltestelle = " ".join(args[0:-1])
            values = {"ort": "Dresden",
                      "hst": haltestelle,
                      "vz": laufzeit,
                      "timestamp": int(time.time())}

            url_values = urllib.urlencode(values)
            full_url = config.get("abfahrt", "url") + "?" + url_values

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
            if int(args[1]) > int(config.get('RSS', "maxfeeds")):
                args[1] = config.get('RSS', "maxfeeds")
            for loop in range(int(args[1])):
                f = feedparser.parse(config.get('RSS', args[0])).get('entries')[loop]
                message += 'Titel: ' + f.get('title') + '\n' + 'URL: ' + f.get('link') + '\n'
        else:
            message = 'Bitte rufe \"help last\" fuer moegliche Optionen auf!'
        return message
        
    @botcmd
    def elbe(self, mess, args):
        '''
        aktueller elbpegel
        '''
        message = ""
        url = 'http://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/DRESDEN/W/currentmeasurement.json'
        params = dict(
            includeTimeseries='false',
            includeCurrentMeasurement='true',
            waters='ELBE'
            )
        #elbabsaufer = dict()
        data = requests.get(url=url)
        

#        try:
#            args = args.strip().split(' ')
#            print "" + args[0] + ", "+ args[1]
#        except:
#            message = "fehler\n"
#        if (len(args)!=0):
#            if (elbabsaufer.has_key(args[1])):
#                elbabsaufer[args[0]] = args[1]
#                message = "%s wird bei %s absaufen\n" % args[0], args[1]
#            else:
#                message = "%s saeuft bei %s ab!\n" % args[0], elbabsaufer[args[0]]
#                    
#    
        
        content = json.loads(data.content)
        #pprint.pprint(content)

        pegel = content.get('value')

        message += 'Pegelstand: %d cm' % pegel
        
        return message



if __name__ == "__main__":
    #start Server
    while True:
        pentabot = pentaBot(secret.get('pentaBotSecret', 'username'), secret.get('pentaBotSecret', 'password'), secret.get('pentaBotSecret', 'resource'), bool(secret.get('pentaBotSecret', 'debug')))
        pentabot.join_room(config.get("muc", "chan"), config.get("muc", "name"))
        pentabot.serve_forever()
