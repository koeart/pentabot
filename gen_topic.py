#!/usr/bin/env python
# -*- coding: utf-8 -*-


import random

donouns = [
    "Programmieren" ,
    "Hacken" ,
    "λaskell" ,
    "Python" ,
    "Kuchen" ,
    "Nudeln" ,
    "Pizza" ,
    "Computer" ,
    "Elektronik" ,
    "Bier" ,
    "Kaffee" ,
    "Löten" ,
    "Ruby" ]

philnouns = [
    "Linux" ,
    "Wind0ze",
    "XMPP-Clients unter Android" ,
    "Topologisches Sortieren" ,
    "Erdbeeren"]

nouns = donouns + philnouns


ortphrase = [
    "an der Elbe" ,
    "in der sächs.Schweiz" ,
    "im HQ",
    "im Netzbiotop e.V.",
    "bei $h4ck3r",
    "in dd" ,
    "im CCC" ]
zeitphrase = [
    "im späten 18.Jhrd" ,
    "in der heutigen Zeit" ,
    "heute abend"
]


adverbphrase = ortphrase + zeitphrase + [
    "an sich",
    "überhaupt" ]


def get_topic():
	def ra(x):
		return random.choice(x)
	whundert = random.randint(0,99)
	if (whundert < 40):
		return "%s %s"%(ra(nouns) ,ra(adverbphrase))
	elif (whundert > 40) :
		return "%s %s %s"%(ra(donouns),ra(ortphrase),ra(zeitphrase))
	else :
		return "Das Leben und der ganze Rest"


if __name__ == "__main__":
    for i in range(80):
	print get_topic()


