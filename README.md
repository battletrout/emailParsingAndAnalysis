# Campaign Supporter Email Data Wrangling and Analysis
Note that links are to my previous github account name, TestBro1745.  Just replace TestBro 1745 with battletrout for any hyperlinks.

Are you curious about the rhetoric used in political emails to supporters? Political emails are easily gathered and are an intimate window into the language used to influence supporters that candidates are confident are already on their side.

This project takes emails of various formats and prepares them for natural language processing. All the data used here was collected by signing up for campaign emails on each political candidates' official campaign page.

I get google takeout to give me a .mbox file of all the messages in a given label. I have a gmail that is subscribed to a bunch of political email accounts, and the takeout function from google makes it very easy to download messages in a given label as a .mbox.

Python 3.7 is the language of the day.

# obj/
- ConsolidatedPoliticalEmails.mbox: .mbox with emails from the 3 democratic candidates who were topping the polls on the day I pulled the data from my campaign email collection email address.
- top3DemMboxOutput.json: output from running sampleEmailParser.py on ConsolidatedPoliticalEmails.mbox. It is plaintext extracted and smoothed from the emails and is ready for processing in NLTK.
- topGOPCampaignEmailOutput.json: a collection of 300+ political emails from a GOP candidate extracted and smoothed. I removed the email ending disclaimers ("Paid for by xyz, sent to recipientEmail, etc") using regex so as not to skew analysis of frequency, etc.

# emailParseAndScrub.py
- **Assumes there is a /obj folder in the cwd. This is default output file location**
- defines class emailMboxParser. emailMboxParser takes a .mbox file as an input and outputs .txt, .json, or .pkl. 
- Touples of compiled regex's and what to replace the regex with when found (re.Pattern,str) can be added to the list regexTouples internal to an emailMboxParser, as well as replaceTouples (str,str) which will just be removed and replaced at runtime.
- Users can extract other parts of the message's payload as well with HeaderTouples: AddHeaderTouple('X-Gmail-Labels','Warren','Candidate') creates a key "Candidate" with value "Warren" if Warren is found in the X-Gmail-Labels header's payload. This is particularly useful for emails you have marked with labels in gmail, as in this example.
- Some messages are multi-part. The emailMboxParser automatically extracts the first part only as the body if it is multi-part. Sometimes this cuts off the disclaimer section at the end of emails ("donations are not tax-deductable"), sometimes the entire email is in plaintext in part [0], and html in [1].
- declareDefaultRegex creates regex touple combinations for hyperlinks, large spans of whitespace, and some characters to remove to make plaintext make sense.
- parseToPickle(self,outputFilename='mboxPickleOutput',outputFolder='obj/',simple=False) outputs a pickle file of a list of dictionaries. Each dictionary created from a message with keys for Subj, Date, From, and Body.

sampleEmailParser.py: imports mailbox, mboxEmailParseAndScrub.py.
- An example of how the emailMboxParser is used. 

Don't worry, there's no error handling.

