# -*- coding: utf-8 -*-

from jabberbot import botcmd
import feedparser
import datetime
import time
import urllib
import os
import json
import requests
import logging
from decorators import ignore_msg_from_self
from pentabot import feed_help, config
from gen_topic import get_topic
from gen_kickreason import get_kickreason 

def format_help(fun):
    fun.__doc__ = fun.__doc__.format(**feed_help) #** dict entpacken, * listen entpacken 
    return fun

def _stroflatlog_de(latitude, longitude):
    """
    helper for latitude longitude to german
    """
    southnorth = ("nördlicher","südlicher")[int(latitude < 0)]
    snshort = ("N", "S")[int(latitude < 0)]
    eastwest = ("östlicher","westlicher")[int(longitude < 0 )]
    ewshort = ("E", "W")[int(longitude<0)]
    return "%f %s Breite und %f %s Länge { %f°%s %f°%s }" % (abs(latitude), southnorth, abs(longitude), eastwest, abs(latitude), snshort, abs(longitude), ewshort)

@botcmd
@ignore_msg_from_self
def helloself(self, mess, args):
    """
    Hello Self, the botway
    """
    return 'Hello ' + str(self.jid)

@botcmd
@ignore_msg_from_self
def helloworld(self, mess, args):
    """
    Hello World, the botway
    """
    return 'Hello World, the botway!'

@botcmd
@ignore_msg_from_self
def echo(self, mess, args):
    """
    ein echo fuer die welt
    """
    return args

@botcmd
@ignore_msg_from_self
def thetime(self, mess, args):
    """
    Zeige die aktuelle Server Zeit
    """
    return str(datetime.datetime.now())

@botcmd
@ignore_msg_from_self
def gentopic(self,mess,args):
    """
    Generiert einen Vorschlag für ein Gesprächsthema
    """
    return 'Wie wärs mit „%s“'%get_topic()

@botcmd
@ignore_msg_from_self
def kickrnd(self,mess,args):
	"""
	Schmeißt eine zufällig gewählte Person raus
	"""
	rnduser = mess.getFrom()
	self.muc_kick(mess.getTo(),rnduser,get_kickreason())
	return ":-)"


@botcmd
@ignore_msg_from_self
def rot13(self, mess, args):
    """
    Gibt <string> in rot13
    """
    return args.encode('rot13')


@botcmd
@ignore_msg_from_self
def whoami(self, mess, args):
    """
    Zeigt dir dein Username
    """
    if mess.getType() == "groupchat":
        return str(mess.getFrom()).split("/")[1]
    else:
        return mess.getFrom().getStripped()

@botcmd
@ignore_msg_from_self
def serverinfo(self, mess, args):
    """
    Zeige Informationen ueber den Server
    """
    version = " ".join(map(str, open('/proc/version').read().split(" ")[0:3]))
    loadavg = open('/proc/loadavg').read().strip()
    return '%s\nload:\n%s' % ( version, loadavg, )

@botcmd
@ignore_msg_from_self
def fortune(self, mess, args):
    """
    Fortune Cookie for you

    A Cookie you can trust and accept.
    Just run fortune
    """
    fortune = ''
    try:
        fortune += os.popen('/usr/games/fortune').read()
    except:
        fortune += 'Your fortune unforseeable'
    return ('Your Cookie reads:\n' + fortune)

@botcmd
@ignore_msg_from_self
def ddate(self, mess, args):
    """
    Perpetual date converter from gregorian to poee calendar
    """
    args = args.strip().split(' ')
    ddate = ''
    if len(args) <= 1 :
        ddate += os.popen('/usr/bin/ddate').read()
    elif len(args) == 3 and all(arg.isdigit() for arg in args):
        ddate += os.popen('/usr/bin/ddate ' + args[0] + ' ' + args[1] + ' ' + args[2]).read()
    else:
        ddate = 'You are not using correctly!\n Just enter ddate or append day month year'
    return ddate

@format_help
@botcmd
@ignore_msg_from_self
def last(self, mess, args):
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
@ignore_msg_from_self
def elbe(self, mess, args):
    """
    aktueller elbpegel
    """
    message = ""
    url = config.get("elbe", "url")
    params = dict(
        includeTimeseries='false',
        includeCurrentMeasurement='true',
        waters='ELBE'
        )

    data = requests.get(url=url)
    content = json.loads(data.content)
    pegel = content.get('value')

    message += 'Pegelstand: %d cm' % pegel
    return message

@botcmd
@ignore_msg_from_self
def abfahrt(self, mess, args):
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
            haltestelle = args[0]
        else:
            if args[-1].isdigit():
                laufzeit = args[-1]
                haltestelle = " ".join(args[0:-1])
            else:
                laufzeit = config.get("abfahrt", "laufzeit")
                haltestelle = " ".join(args[0:])

        values = {"ort": "Dresden",
                    "hst": haltestelle,
                    "vz": laufzeit,
                    "timestamp": int(time.time())}

        # fix unicode issues of urlencode
        encoded_values = {}
        for key, value in values.iteritems():
            encoded_values[key] = unicode(value).encode('utf-8')
        url_values = urllib.urlencode(encoded_values)

        full_url = config.get("abfahrt", "abf_url") + "?" + url_values
        data = requests.get(url=full_url)

        if json.loads(data.content):
            abfahrt += "\n%6s %-19s %7s\n" % ("Linie", "Richtung", "Abfahrt")

            for line in json.loads(data.content):
                abfahrt += "%6s %-19s %7s\n" % (line[0], line[1], line[2])

        else:
            hst_url = config.get("abfahrt", "hst_url") + "?" + url_values
            data = requests.get(url=hst_url)

            if json.loads(data.content)[1]:
                abfahrt += "Such dir eine aus:\n"
                i = 0

                for line in json.loads(data.content)[1]:
                    i = i + 1
                    if i <= 10:
                        abfahrt += "* %s\n" % line[0]
                    else:
                        abfahrt += "und viele mehr..."
                        break


    return abfahrt

@botcmd
@ignore_msg_from_self
def hq(self, mess, args):
    """
    Information die ueber http://www.hq.c3d2.de/spaceapi.json auszulesen sind
    """

    url = config.get("hq", "url")
    data = requests.get(url=url)
    content = json.loads(data.content)

    message = ""
    contact_help_msg = "        all         Zeigt dir alle Daten\n"
    contact_help_msg += "        phone       Zeigt dir die Festnetz Nummer unter der wir erreichbar sind\n"
    contact_help_msg += "        twitter     Zeigt dir das Voegelchen unter dem wir schreiben oder erreichbar sind\n"
    contact_help_msg += "        jabber      Zeigt dir die den MUC unter der wir erreichbar sind\n"
    contact_help_msg += "        irc         Zeigt dir wie du uns im IRC erreichen kannst\n"
    contact_help_msg += "        ml          Zeigt dir auf welcher Mailingliste du uns erreichen kannst\n"
    feeds_help_msg = "        blog         Zeigt dir die C3D2-Mews-Feed-URL an\n"
    feeds_help_msg += "        wiki          Zeigt dir die C3D2-Wiki-Feed-URL an\n"
    feeds_help_msg += "        calendar   Zeigt dir die C3D2-Kalender-Feed-URL an\n"
    sensors_help_msg = "       pi         Zeigt die Temperatur von " + content.get("sensors").get("temperature")[0].get("name") + "\n"
    help_msg = "Benutze: hq <option> (<option>)\n"
    help_msg += "Optionen:\n"
    help_msg += "    status          Zeigt dir den Status (offen/zu) vom HQ\n"
    help_msg += "    coords          Zeigt dir die Koordinaten des HQ\n"
    help_msg += "    sensors         Zeigt die Werte der Sensoren im HQ\n"
    help_msg += sensors_help_msg
    help_msg += "    contact         Zeigt dir Kontakt Daten zum HQ\n"
    help_msg += contact_help_msg
    help_msg += "    web             Zeigt dir den Link zu unserer Webseite\n"
    help_msg += "    feeds           Zeigt dir die Newsfeeds des C3D2\n"
    help_msg += feeds_help_msg

    args = args.strip().split(' ')

    if not args[0]:
        message = help_msg
    elif args[0] == "status":
        message += content.get("state").get("message")
    elif args[0] == "coords":
        message += "Das HQ findest du auf %s ."%(_stroflatlog_de(content.get("location").get("lat") , content.get("location").get("lon")))
    elif args[0] == "web":
        message += "Der Chaos Computer Club Dresden (C3D2) ist im Web erreichbar unter " + content.get("url") + " ."
    elif args[0] == "sensors":
        if len(args) == 1:
            message += "Du kannst waehlen zwischen:\n"
            message += sensors_help_msg
        elif args[1] == "pi":
            message += content.get("sensors").get("temperature")[0].get("location") + " (" + content.get("sensors").get("temperature")[0].get("name") + "): " + str(content.get("sensors").get("temperature")[0].get("value")) + content.get("sensors").get("temperature")[0].get("unit")
        else:
            message += "Probier es noch mal mit einer der folgenden Optionen: [aktuell nur] pi"
    elif args[0] == "contact":
        if len(args) == 1:
            message = "Du kannst waehlen zwischen:\n"
            message += contact_help_msg
        elif args[1] == "all":
            message += "Du kannst uns unter dieser Festnetznummer erreichen: +" + content.get("contact").get("phone") + " .\n"
            message += "Wir sind auf Twitter unter: https://twitter.com/" + content.get("contact").get("twitter") + " zu finden.\n"
            message += "Im IRC findest du uns hier: " + content.get("contact").get("irc") + "\n"
            message += "Im Jabber vom C3D2 findest du uns im Raum " + content.get("contact").get("jabber") + " .\n"
            message += "Falls du uns auf der Mailingliste folgen willst meld dich einfach hier an: " + content.get("contact").get("ml") + "\n"
        elif args[1] == "phone":
            message += "Du kannst uns unter dieser Festnetznummer erreichen: +" + content.get("contact").get("phone") + " ."
        elif args[1] == "twitter":
            message += "Wir sind auf Twitter unter: https://twitter.com/" + content.get("contact").get("twitter") + " zu finden."
        elif args[1] == "irc":
            message += "Im IRC findest du uns hier: " + content.get("contact").get("irc")
        elif args[1] == "jabber":
            message += "Im Jabber vom C3D2 findest du uns im Raum " + content.get("contact").get("jabber") + " ."
        elif args[1] == "ml":
            message += "Falls du uns auf der Mailingliste folgen willst meld dich einfach hier an: " + content.get("contact").get("ml")
        else:
            message += "Probier es noch mal mit einer der folgenden Optionen: all, phone, twitter, jabber, irc oder ml."
    elif args[0] == "feeds":
        if len(args) == 1:
            message += "Du kannst waehlen zwischen:\n"
            message += feeds_help_msg
        elif args[1] == "blog":
            message += "Den Atom-Feed zu den C3D2 News findest du hier: " + content.get("feeds").get("blog").get("url")
        elif args[1] == "wiki":
            message += "Den Atom-Feed zum C3D2-Wiki News findest du hier: " + content.get("feeds").get("wiki").get("url")
        elif args[1] == "calendar":
            message += "Den iCal-Feed vom C3D2 findest du hier: " + content.get("feeds").get("calendar").get("url")

        else:
            message += "Probier es noch mal mit einer der folgenden Optionen: blog, wiki oder calendar."
    else:
        message += "Probier es noch mal mit einer der folgenden Optionen: status, sensors, coords, contact, web oder feeds."
    return message
