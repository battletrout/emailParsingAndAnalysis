import mailbox
import re
import pickle
from bs4 import BeautifulSoup

#os.chdir('C:\\PythonProjects\\DataAnalysisProjects\\TrumpEmails\\mBoxFile\\Mail\\TEST\\')

#i = 0

#shelve.open('trumpEmailOutputShelve')



RECIPIENT_EMAIL = 'nathanmkemp@gmail.com'
# find a way to replace N? with recipient firstname and N K with fullname...
RECIPIENT_FIRNAME1 = '\nN,'
RECIPIENT_FIRNAME2 = ' N '
RECIPIENT_FULLNAME = '\nN K'

# create the regex for hyperlinks
regexHyper = re.compile(r'http://\S+', re.IGNORECASE)
# regex for quotes and apostrophes &rsquo; &ldquo; &rdquo;
regexQuote = re.compile(r'\&\w{5};')
# for tabs
regexTab = re.compile(r'\t')
# for arrows
regexArr = re.compile(r'\&\w{4};')
# for all other &... html characters
regexOther = re.compile(r'\&\S{3,6};')
# for all blocks of whitespace 2+lines with any number of spaces between
regexWhiteSpace = re.compile(r'(\n+\s+\n)+')


def ParseMsgToDict(message,simple=True):
    if simple: MsgDict= {
    'Subject' : message['Subject'],
    'Date' : message['Date'] ,
    'From' : message['From'],
    'Body' : cleanMessageBodyRemove(UnpackMessagePayload(message))
    }
    else: MsgDict= {
    'Subject' : message['Subject'],
    'Date' : message['Date'] ,
    'From' : message['From'],
    'Body' : cleanMessageBodyReplace(UnpackMessagePayload(message))
    }
    return MsgDict

def ParseMsgToTxt(message):
    
    printString = ''

    printString += ('**'*20 + '\n')
    printString += ('Subject:     ' + message['Subject'] + '\n')
    printString += ('Date:        ' + message['Date'] + '\n')
    printString += ('From:        ' + message['From'] + '\n')
    printString += ('Body:        ' + '\n')
    printString += UnpackMessagePayload(message)
    return printString
    # Check to see if the message is a multi-part message.

def UnpackMessagePayload(message):
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

def cleanMessageBodyReplace(payloadString):
    #replaces recipient firstname, email, etc. w/ tags ++whatever++
    payloadString = regexQuote.sub("'",payloadString)
    payloadString = regexArr.sub("--",payloadString)
    payloadString = regexOther.sub("",payloadString)
    payloadString = payloadString.replace(RECIPIENT_EMAIL,'++RECIPIENT_EMAIL++')
    # find a way to replace N? with recipient firstname and N K with fullname...
    payloadString = payloadString.replace(RECIPIENT_FIRNAME1,'\n++RECIPIENT_FIRNAME++')
    payloadString = payloadString.replace(RECIPIENT_FIRNAME2,'++RECIPIENT_FIRNAME++')
    payloadString = payloadString.replace(RECIPIENT_FULLNAME,'\n++RECIPIENT_FULLNAME++')
    # use the regular expression defined above to replace all hyperlinks with "++HYPERLINK++"
    payloadString = regexHyper.sub('++HYPERLINK++',payloadString)
    payloadString = regexTab.sub(' ',payloadString)
    payloadString = regexWhiteSpace.sub('\n',payloadString)
    return(bytes(payloadString,'ascii','ignore').decode('ascii','ignore'))

def cleanMessageBodyRemove(payloadString):
    #replaces recipient firstname, email, etc. w/ tags ++whatever++
    payloadString = regexQuote.sub("'",payloadString)
    payloadString = regexArr.sub("",payloadString)
    payloadString = regexOther.sub("",payloadString)
    payloadString = payloadString.replace(RECIPIENT_EMAIL,' ')
    # find a way to replace N? with recipient firstname and N K with fullname...
    payloadString = payloadString.replace(RECIPIENT_FIRNAME1,'\n ')
    payloadString = payloadString.replace(RECIPIENT_FIRNAME2,' ')
    payloadString = payloadString.replace(RECIPIENT_FULLNAME,'\n ')
    # use the regular expression defined above to replace all hyperlinks with "++HYPERLINK++"
    payloadString = regexHyper.sub(' ',payloadString)
    payloadString = regexTab.sub(' ',payloadString)
    payloadString = regexWhiteSpace.sub('\n',payloadString)
    return(bytes(payloadString,'ascii','ignore').decode('ascii','ignore'))

def parseToText(mBox,outputFilename='mboxTxtOutput',outputFolder='obj/',simple=True):
    # create an output file in write mode
    outputText = open(outputFolder + outputFilename + '.txt','w')
    for message in mBox:
        outputString = ParseMsgToTxt(message)
        if simple: outputString = cleanMessageBodyRemove(outputString)
        else: outputString = cleanMessageBodyReplace(outputString)
        outputText.write(outputString)
    outputText.close()

def parseToDict(mBox,simple=True):
    #__doc__ = 'hello'
    MsgCount = 0
    AllMessages = {}
    for message in mBox:
        MsgCount += 1
        MsgDict = ParseMsgToDict(message,simple)
        AllMessages.update({MsgCount:MsgDict})
        #if MsgCount > 10: break
    return AllMessages

def dictToPickle(inputDict,outputFilename='mboxPickleOutput',outputFolder='obj/'): 
    with open(outputFolder + outputFilename + '.pkl', 'wb+') as f:
        pickle.dump(inputDict, f)
                    #HIGHEST_PROTOCOL)

def parseToPickle(mBox,outputFilename='mboxPickleOutput',outputFolder='obj/',simple=True):
    dictToPickle(parseToDict(mBox,simple),outputFilename,outputFolder)

def loadDictFromPickle(pickleFile='mboxPickleOutput',inputFolder='obj/'):
    with open(inputFolder + pickleFile + '.pkl', 'rb') as f:
        return pickle.load(f)

if __name__ == "__main__":
    
    mBox = mailbox.mbox('Trump.mbox')
    parseToPickle(mBox,simple=False)
    parseToText(mBox,simple=True)
    
    




    

'''
print(message['X-Received:'])
print(message.get_from)
'''