# -*- coding: utf-8 -*-
"""
First Version began March 30, 2019

@author: testBro1745

go use the sampleEmailParser.py file or read the readme in the github 
https://github.com/TestBro1745/doingTheData

"""

import mailbox
import re
import pickle
import json
from bs4 import BeautifulSoup

class emailMboxParser:
    
    def __init__(self,mBox = None):
        self.mBox = mBox
        #replaceTouples is a list of (0,1) touples where [0] is what to replace
        #and [1] is what to replace it with. Both strings.
        self.replaceTouples = []
        #regexTouples is a list of (0,1) touples where [0] is a compiled 
        #re.Pattern object (regex pattern) and [1] is what to sub it with.
        self.regexTouples = []
        #headerTouples is a list of (0,1,2) touples. [0] is what header you are searching in
        #[1] is what you're searching for in that header.  [2] is what you want the 
        #dictionary's key name to be. This enables multiple things from the same header to be 
        #recorded with different keys
        self.headerTouples = []
        self.encode = 'ascii'
    
    def declareDefaultRegex(self):
        # create the regex for hyperlinks
        self.regexTouples.append((re.compile(r'https?://\S+', re.IGNORECASE),' ++HYPERLINK++ '))
        # regex for quotes and apostrophes &rsquo; &ldquo; &rdquo;
        self.regexTouples.append((re.compile(r'\&\w{5};'),"'"))
        # for tabs
        self.regexTouples.append((re.compile(r'\t'),'  '))
        # for too many spaces
        self.regexTouples.append((re.compile(r'\s\s\s*'),' '))     
        # for arrows
        self.regexTouples.append((re.compile(r'\&\w{4};'),'--'))
        # for all other &... html characters
        self.regexTouples.append((re.compile(r'\&\S{3,6};'),''))
        # for all blocks of whitespace 2+lines with any number of spaces between
        self.regexTouples.append((re.compile(r'(\n+\s+\n)+'),'\n'))
    
    def AddHeaderTouple(self,header,findValue=None,keyValue=None):
        if type(header) != str or (findValue != None and type(findValue) != str) or (keyValue != None and type(keyValue) != str):
            print('header must be string. Other 2 arguments are optional-- None or string')
        else: self.headerTouples.append((header,findValue,keyValue))
    
    def AddRegexTouple(self,regexPattern,replaceWith=' '):    
        if type(regexPattern) == re.Pattern and type(replaceWith) == str:
            self.regexTouples.append((regexPattern,replaceWith))
        else: print('''requires at least 1 argument (re.Pattern object), 
                    and the second if provided must be a string''')
        
    def AddReplacementTouple(self,whatToReplace,replaceWith=' '):
        #both inputs must be strings
        if type(whatToReplace) == str and type(replaceWith) == str:
            replaceTouple = (whatToReplace,replaceWith)
            self.replaceTouples.append(replaceTouple)
        else: print('requires at least 1 argument, and arguments must be strings')
    
    def ParseMsgToDict(self,message,simple=True):
        bodyExtract = self.cleanMessageBody(self.UnpackMessagePayload(message))
        MsgDict= {
        'Subject' : self.cleanMessageBody(message['Subject']),
        'Date' : message['Date'] ,
        'From' : message['From'],
        'Body' : bodyExtract
        }
        
        if len(self.headerTouples) == 0: return MsgDict
        additionalItems = self.FindAdditionalItems(message)
        for item in additionalItems:
            MsgDict.update({item[0] : item[1]})
        return MsgDict
    
    def FindAdditionalItems(self,message):
        additionalItems = []
        for header in self.headerTouples:
            try: headerPayload = message[header[0]]
            except:
                print('header {} not present'.format(header[0]))
                continue
            if not header[1] and not header[2]: #key:mbox header, value: mbox value
                additionalItems.append((header[0],headerPayload))
                break
            else:
                #if findValue not found, break and move on
                if not header[1] in headerPayload: continue
                #if findValue is found but no dictvalue give, key: mbox header, value: findValue
                elif not header[2]: additionalItems.append((header[0],header[1]))
                #if findValue found and dictvalue given, key: keyValue, value: findValue
                else: additionalItems.append((header[2],header[1]))
        return additionalItems
            
    def ParseMsgToTxt(self,message):    
        printString = ''
        printString += ('**'*20 + '\n')
        printString += ('Subject:     ' + message['Subject'] + '\n')
        printString += ('Date:        ' + message['Date'] + '\n')
        printString += ('From:        ' + message['From'] + '\n')
        printString += ('Body:        ' + '\n')
        printString += self.UnpackMessagePayload(message)
        return printString
        
    def UnpackMessagePayload(self,message):
        TotalPayload = ''
        if message.is_multipart():
            payloadParts = []
            # If it is multipart, get all parts of the payload, but only print the first one. The rest is just encoding stuff.
            # It looks like the first part is plaintext, and the second is the email as html. Not sure.
            for part in message.get_payload():
                payloadParts.append(part.get_payload()) 
            TotalPayload += str(payloadParts[0])
        else:
            payloadString = message.get_payload()
            #payloadString = BeautifulSoup(payloadString,features="html.parser").text
            payloadString = BeautifulSoup(payloadString,features="html.parser").text
            TotalPayload += payloadString.split('{ display: none !important; }')[2]
        return(TotalPayload)
    
    def removeReplaceScrub(self,payloadString,simple=False):
        for removeTouple in self.replaceTouples:
            if simple: 
                if removeTouple[1][:2] == '\n': removeTouple[1] = '\n '
                else: removeTouple[1] = ' '
            payloadString = payloadString.replace(removeTouple[0],removeTouple[1])
        return payloadString
    
    def regexReplaceScrub(self,payloadString,simple=False):
        for regexTouple in self.regexTouples:
            if simple:
                if regexTouple[1][:2] == '\n': regexTouple[1] = '\n '
                else: regexTouple[1] = ' '
            payloadString = regexTouple[0].sub(regexTouple[1],payloadString)
        return payloadString
    
    def cleanMessageBody(self,payloadString,simple=False):
        #removeReplaceScrub first to keep from regexing email addresses
        payloadString = self.removeReplaceScrub(payloadString,simple)
        payloadString = self.regexReplaceScrub(payloadString,simple)
        return(bytes(payloadString,self.encode,'ignore').decode(self.encode,'ignore'))
    
    def parseToText(self,outputFilename='mboxTxtOutput',outputFolder='obj/',simple=True):
        # create an output file in write mode
        outputText = open(outputFolder + outputFilename + '.txt','w')
        try:
            for message in self.mBox:
                outputString = self.ParseMsgToTxt(message)
                outputString = self.cleanMessageBody(outputString)
                outputText.write(outputString)
        except: print('failed to parse')
        outputText.close()
    
    def parseToDict(self,simple=True):
        #Input is an mBox file, output is a list of dictionaries.
        #MsgCount = 0
        AllMessages = []
        for message in self.mBox:
            #MsgCount += 1
            MsgDict = self.ParseMsgToDict(message,simple)
            AllMessages.append(MsgDict)
        return AllMessages
    
    def objToPickle(self,inputObj,outputFilename,outputFolder='obj/'):         
        with open(outputFolder + outputFilename + '.pkl', 'wb+') as f:
            pickle.dump(inputObj, f)
            
    def objToJson(self,inputObj,outputFilename,outputFolder='obj/'):         
        with open(outputFolder + outputFilename + '.json', 'w') as f:
            json.dump(inputObj, f, sort_keys=False, indent=4)
    
    def parseToPickle(self,outputFilename='mboxPickleOutput',outputFolder='obj/',simple=False):
        self.objToPickle(self.parseToDict(simple),outputFilename,outputFolder)
    
    def loadObjFromPickle(self,pickleFile='mboxPickleOutput',inputFolder='obj/'):
        with open(inputFolder + pickleFile + '.pkl', 'rb') as f:
            return pickle.load(f)
    
    def parseToJson(self,outputFilename='mboxJSONOutput',outputFolder='obj/',simple=False):
        self.objToJson(self.parseToDict(simple),outputFilename,outputFolder)

if __name__ == "__main__":
    pass
#go use the sampleEmailParser.py file. 