# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 17:07:12 2020

@author: testBro1745

There are 3 different political candidates' emails compiled into a single file,
ConsolidatedPoliticalEmails.mbox. Each has their own style (some have 3+ parts
in their message payload, some have functions that insert your city and state 
information you entered when you signed up for their emails, etc.) and thus 
there are additional regex  touples, replace touples, and header touples to add
 in order to pre-process the data enough for our purposes.
 
This creates a key "Candidate," and before I used google takeout to download 
the data I applied labels to each candidate's emails. This can then be 
extracted from gmail's X-label header and used to populate the Candidate key.

I signed up as "Victro Pala" because I figured it was easy to pick out and 
unlikely to actually be included anywhere in an email.

This outputs to a .json.

"""
import re
import mailbox
from mboxEmailParseAndScrub import emailMboxParser

mBox = mailbox.mbox('obj/ConsolidatedPoliticalEmails.mbox')
newParser = emailMboxParser(mBox)
newParser.AddRegexTouple(re.compile(r'\=\w\w'),'')
newParser.AddRegexTouple(re.compile(r'\[.*\]'))
newParser.declareDefaultRegex()
NEWLINE = '=\n'
NEWLINE2 = '\n'
RECIPIENT_FIRNAME = 'Victro'
RECIPIENT_FIRNAME1 = 'victro'
RECIPIENT_LASTNAME = 'Pala'
newParser.AddReplacementTouple(RECIPIENT_FIRNAME,'recipientFirstName')
newParser.AddReplacementTouple(RECIPIENT_FIRNAME1,'recipientFirstName')
newParser.AddReplacementTouple(RECIPIENT_LASTNAME,'recipientLastName')
newParser.AddReplacementTouple(NEWLINE,'')
newParser.AddReplacementTouple(NEWLINE2,' ')

newParser.AddHeaderTouple('X-Gmail-Labels','Sanders','Candidate')
newParser.AddHeaderTouple('X-Gmail-Labels','Warren','Candidate')
newParser.AddHeaderTouple('X-Gmail-Labels','Biden','Candidate')

newParser.parseToJson('top3DemMboxOutput',simple=False)

