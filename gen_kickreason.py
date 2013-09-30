#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

zu_verbs = [
		"oft",
		"langsam",
		"selten",
		"agressiv",
		"dumm",
		"schnell",
		"mittelmäßig",
		"extrem"
		]

done_verbs = [
		"jemanden beleidigt",
		"fragen gestellt",
		"hacker verunglimpft",
		"gekleckert",
		"prokrastiniert",
		"plagiert"
		]

def get_kickreason():
	def ra(x):
		return random.choice(x)
	whundert = random.randint(0,99)
	if (whundert == 42):
		return "choosen by fair dice roll"
	else :
		return "zu %s %s"%(ra(zu_verbs),ra(done_verbs))


