import mailbox
import re
import pickle
from bs4 import BeautifulSoup
import campaignEmailConfig

class emailMboxParser:
    
    def __init__(self,mBox = None,declareRegex=True):
        self.mBox = mBox
        #replaceTouples is a list of (0,1) touples where [0] is what to replace
        #and [1] is what to replace it with. Both strings.
        self.replaceTouples = []
        #regexTouples is a list of (0,1) touples where [0] is a compiled 
        #re.Pattern object (regex pattern) and [1] is what to sub it with.
        self.regexTouples = []
    
    def declareDefaultRegex(self):
        # create the regex for hyperlinks
        self.regexTouples.append((re.compile(r'http://\S+', re.IGNORECASE),'++HYPERLINK++'))
        # regex for quotes and apostrophes &rsquo; &ldquo; &rdquo;
        self.regexTouples.append((re.compile(r'\&\w{5};'),"'"))
        # for tabs
        self.regexTouples.append((re.compile(r'\t'),'  '))
        # for arrows
        self.regexTouples.append((re.compile(r'\&\w{4};'),'--'))
        # for all other &... html characters
        self.regexTouples.append((re.compile(r'\&\S{3,6};'),''))
        # for all blocks of whitespace 2+lines with any number of spaces between
        self.regexTouples.append((re.compile(r'(\n+\s+\n)+'),'\n'))
        
    def AddRegexTouple(self,regexPattern,replaceWith=' '):    
        if type(regexPattern) == re.Pattern and type(replaceWith) == str:
            regexTouple = (regexPattern,replaceWith)
            self.regexTouples.append(regexTouple)
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
        
        return MsgDict
    
    def ParseMsgToTxt(self,message):    
        printString = ''
        printString += ('**'*20 + '\n')
        printString += ('Subject:     ' + message['Subject'] + '\n')
        printString += ('Date:        ' + message['Date'] + '\n')
        printString += ('From:        ' + message['From'] + '\n')
        printString += ('Body:        ' + '\n')
        printString += self.UnpackMessagePayload(message)
        return printString
        # Check to see if the message is a multi-part message.
    
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
        return(bytes(payloadString,'ascii','ignore').decode('ascii','ignore'))
    
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
        #Input is an mBox file, output is a dictionary with a 
        MsgCount = 0
        AllMessages = {}
        for message in self.mBox:
            MsgCount += 1
            MsgDict = self.ParseMsgToDict(message,simple)
            AllMessages.update({MsgCount:MsgDict})
        return AllMessages
    
    def dictToPickle(self,inputDict,outputFilename='mboxPickleOutput',outputFolder='obj/'): 
        with open(outputFolder + outputFilename + '.pkl', 'wb+') as f:
            pickle.dump(inputDict, f)
    
    def parseToPickle(self,outputFilename='mboxPickleOutput',outputFolder='obj/',simple=True):
        self.dictToPickle(self.parseToDict(simple),outputFilename,outputFolder)
    
    def loadDictFromPickle(self,pickleFile='mboxPickleOutput',inputFolder='obj/'):
        with open(inputFolder + pickleFile + '.pkl', 'rb') as f:
            return pickle.load(f)

if __name__ == "__main__":
    
    RECIPIENT_EMAIL = 'nathanmkemp@gmail.com'
    RECIPIENT_EMAIL_CAPS = 'NATHANMKEMP@GMAIL.COM'

    RECIPIENT_FIRNAME1 = '\nN,'
    RECIPIENT_FIRNAME2 = ' N '
    RECIPIENT_FIRNAME3 = ' N,'
    RECIPIENT_FULLNAME = '\nN K'
    
    mBox = mailbox.mbox('Trump.mbox')
    newParser = emailMboxParser(mBox)
    newParser.AddReplacementTouple(RECIPIENT_EMAIL,'++RECIPIENT_EMAIL++')
    newParser.AddReplacementTouple(RECIPIENT_EMAIL_CAPS,'++RECIPIENT_EMAIL++')
    newParser.AddReplacementTouple(RECIPIENT_FIRNAME1,'++RECIPIENT_FIRNAME++')
    newParser.AddReplacementTouple(RECIPIENT_FIRNAME2,'++RECIPIENT_FIRNAME++')
    newParser.AddReplacementTouple(RECIPIENT_FIRNAME3,'++RECIPIENT_FIRNAME++')
    newParser.AddReplacementTouple(RECIPIENT_FULLNAME,'++RECIPIENT_FULLNAME++')
    newParser.declareDefaultRegex()
    
    newParser.parseToPickle(simple=False)
    newParser.parseToText(simple=False)
    
    




    

'''
print(message['X-Received:'])
print(message.get_from)
'''