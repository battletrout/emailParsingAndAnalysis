# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 17:07:12 2020

@author: the hash-slinging slasher
"""
import mailbox
from mboxEmailParseAndScrub import emailMboxParser

RECIPIENT_EMAIL = 'foo-bar@gmail.com'
RECIPIENT_EMAIL_CAPS = 'FOO-BAR@GMAIL.COM'

RECIPIENT_FIRNAME1 = '\nChuck,'
RECIPIENT_FIRNAME2 = ' Chuck '
RECIPIENT_FIRNAME3 = ' Chuck,'
RECIPIENT_FULLNAME = '\nChuck Yeager'

mBox = mailbox.mbox('Allmyspam.mbox')
newParser = emailMboxParser(mBox)
newParser.AddReplacementTouple(RECIPIENT_EMAIL,'++RECIPIENT_EMAIL++')
newParser.AddReplacementTouple(RECIPIENT_EMAIL_CAPS,'++RECIPIENT_EMAIL++')
newParser.AddReplacementTouple(RECIPIENT_FIRNAME1,'++RECIPIENT_FIRNAME++')
newParser.AddReplacementTouple(RECIPIENT_FIRNAME2,'++RECIPIENT_FIRNAME++')
newParser.AddReplacementTouple(RECIPIENT_FIRNAME3,'++RECIPIENT_FIRNAME++')
newParser.AddReplacementTouple(RECIPIENT_FULLNAME,'++RECIPIENT_FULLNAME++')
newParser.declareDefaultRegex()

newParser.parseToPickle('spamEmailOutput1',simple=False)
newParser.parseToText('spamEmailOutput1',simple=False)

