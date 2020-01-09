# doingTheData
"working code executed now is better than perfect code executed next week"
Are you curious about the language used in political emails? Political emails are an intimate window into the language used to influence supporters.

I began collecting campaign emails from various candidates sometime in 2017, and this is an exercise in data wrangling, and in progress:[natural language processing, and potentially network analysis]

Python 3 is the language of the day

# emailParseAndScrub
I get google takeout to give me a .mbox file of all the messages in a given label. I have a gmail that is subscribed to a bunch of political email accounts, and the takeout function from google makes it very easy to download messages in a given label as a .mbox.
mboxEmailParseAndScrub.py: imports mailbox, re, pickle, and BeautifulSoup from BS4
- **Assumes there is a /obj folder in the cwd**
- defines class emailMboxParser. emailMboxParser takes a .mbox file as an input. Touples of compiled regex's and what to replace the regex with when found (re.Pattern,str) can be added to the list regexTouples internal to an emailMboxParser, as well as replaceTouples (str,str) which will just be remove and replace at runtime.
- Some messages are multi-part. The emailMboxParser automatically extracts the first part only as the body if it is multi-part. Sometimes this cuts off the disclaimer section at the end of emails ("donations are not tax-deductable"), sometimes the entire email is in plaintext in part [0], and html in [1].
- declareDefaultRegex creates regex touple combinations for hyperlinks, large spans of whitespace, and some characters to remove to make plaintext make sense.
- parseToPickle(self,outputFilename='mboxPickleOutput',outputFolder='obj/',simple=False) outputs a pickle file of a list of dictionaries. Each dictionary created from a message with keys for Subj, Date, From, and Body.

sampleEmailParser.py: imports mailbox, mboxEmailParseAndScrub.py.
- An example of how the emailMboxParser is used. Replaces email, first name, last name, and full name of the user with tags to maintain context while scrubbing for user info.

Don't worry, there's no error handling.

