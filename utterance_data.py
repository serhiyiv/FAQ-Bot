
import regex as re
import spacy

class UtteranceData:
    """UtteranceData class
    Returns:
        UtteranceData: a class to define an utterance object
    """
    utterances = []
    answer = ""
    pattern = ""
    flags = ""
    match = None
    type = ""
    docList = []
   
    
    def __init__(self, utterances, answer, pattern, flags, type):
        """UtteranceData constructor

        Args:
            utterances (String[]): An array of possible utterances
            answer (String): A string with an answer
            pattern (String): REGEX search pattern
            flags (String): REGEX flags
            type (String): Type of the utterance object
        """
        self.utterances = utterances
        self.answer = answer
        self.flags = flags
        self.pattern = pattern if pattern != "" else utterances[0]
        self.type = type
        self.docList = []
       

    def matchUtterance(self, userUtteranceDoc):
        """Try to Match user's utterance
        Args:
           userUtteranceDoc (Spacy Doc Object): An utterance from the user to match 
        """
        # format the pattern to use word boundary anchor
        pattern = r"(\b(" + self.pattern +")\\b)"
        # set BESTMATCH and IGNORECASE
        self.match = re.search(pattern + self.flags, userUtteranceDoc.text, flags= re.IGNORECASE)

        """ Debug Purpose output"""
        if self.match:
           
            print(" * Match:", self.match)
            print(" * Pattern: " + self.pattern)
            print(" * Utterances: ", self.utterances)
            print(" * Answer: " + self.answer)
            print(" * Fuzzy Counts: ", self.match.fuzzy_counts) 
            print(" * Fuzzy Changes: ", self.match.fuzzy_changes)
            print(" * All Captures: ", self.match.allcaptures())
            print(" * Captures: ", self.match.captures())
            print(" * Groups: ", self.match.groups())
            print(" * Group Dict: ", self.match.groupdict())
            print(" * Groups Length:", self.getGroupsLenght())
            
            print(" * Group Dict: ", self.match.capturesdict())
            print(" * Group Dict: ", self.match.detach_string())
            print(" * Group Dict: ", self.match.allspans()) 
            print(" * Group Dict: ", self.match.span())
            print(self.match)
            
            
            
            print(" * Captures: ", self.match.captures()[0])
             
             
              
        return self.match
        
    
    def getFuzzyCounts(self):
        """Gets a total sum of the fuzzy counts tuple
        Returns:
            Integer: total sum of the fuzzy counts tuple
        """
        result = 0
        if (self.match != None):
            fuzzies = self.match.fuzzy_counts
            for value in fuzzies:
                result += value
            
        return result
    
    
    def getGroupsLenght(self):
        """Gets a total length of the matched strings in the group 
        Returns:
            Integer: total length of the matched strings in the group 
        """
        result = 0
        if (self.match != None):
            groups = self.match.groups()
            for group in groups:
                if ((group != None) and (group != '')):
                    result+= len(group)
        
        return result
        
        
    def initializeDoc(self, nlp):
        for utterance in self.utterances:
            
            doc = nlp(utterance)
            self.docList.append(doc)
            print("len: > ", len(self.docList))
            #print(" ____" + doc.text)
            
            
            #for token in doc:
                #print(token.text)
        
    def wordMatchCount(self, userUtteranceDoc):
        for usertoken in userUtteranceDoc:
            print("Checking for: ", usertoken.text)
            matchCnt = 0
            for doc in self.docList:
                print("  > " + doc.text)
                for token in doc:
                    if (token.text.lower() == usertoken.text.lower()):
                        matchCnt+= 1
            print("Match Cnt: ", matchCnt)           
        
     







    def wordMatchCount2(self):
        counter = 0
        for i in self.match.captures():
            counter += 1

        print("COUNTT: ", counter)
        return counter
        