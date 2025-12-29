""" 
    This is an Assignment 3 implementation of Phase 1 of FAQ Bot Plus
    Serhii Ivanchuk [000818168], Mohawk College, October 23, 2023
    ----------------------------------------------------------------------------------------------------------------------
    
    Sources Used for 20 Q/A:
        https://www.embarcadero.com/products/rad-studio/firedac
        https://docwiki.embarcadero.com/RADStudio/Alexandria/en/Using_Databases
        https://learndelphi.org/how-to-build-a-database-app-in-delphi-in-less-than-8-minutes/
        https://learndelphi.org/these-3-tools-provide-powerful-solutions-for-web-development/#:~:text=These%20include%20TMS%20Webcore%2C%20IntraWeb,once%20required%20native%20windows%20development.
        https://www.embarcadero.com/products/delphi/features/cloud
        https://en.wikipedia.org/wiki/Delphi_(software)
        https://docwiki.embarcadero.com/RADStudio/Sydney/en/64-bit_Windows_Application_Development
        https://jonlennartaasenden.wordpress.com/2014/11/06/famous-software-made-with-delphi/
        https://6sense.com/tech/rapid-application-development/delphi-market-share
        https://stackoverflow.com/questions/755980/are-delphi-strings-immutable#:~:text=Delphi%20strings%20are%20not%20immutable,and%20copy-on-write.
    ----------------------------------------------------------------------------------------------------------------------
    
    PHASE 1: FAQ BOT
     - for this phase, a "regex" library is used to find best matching data for the users utterances.
     - data now is stored and loaded from a .JSON file
     - UtteranceData class is defined to make the bot implementation more flexible
     - User's utterance is iterated over all available UtteranceData objects to find a match
     - The best match is chosen by two methods: getFuzzyCounts() and getGroupsLenght() of the UtteranceData object
       in a way that the most suitable response is considered to have total longer count of characters and 0 fuzzy counts  
     - If no match found, the utterance is then offered to be searched in Google
     - for now keep 1 error - {e<=1}
    
       So far the patterns allow to ask questions with different composition and match proper responses.
       EX: is code backward compatible
           what about code backward compatibility
       etc.
       
       It is not perfect but seems to work fine. One thing to note, the "regex" library is also somehow behaves strange with some patterns, 
       and when some petterns were successfully tested on https://regexr.com or https://regex101.com, they did not work with the library

       C:\...\AppData\Local\Programs\Python\Python311\python.exe -m pip install regex 
       C:\ProgramData\anaconda3\python.exe -m pip install regex
"""

import webbrowser
import json
import utterance_data
import regex as re
import spacy

# a list of UtteranceData objects
dataList: list[utterance_data.UtteranceData] = []
nlp = spacy.load("en_core_web_sm")


def load_FAQ_data():
    """Loads questions/answers data from files
    Returns:
        bool: True if data was successfully loaded
    """
    print("\nAvailable Questions:")
    loaded = True
    try:
        dataFile = open('datafile.json')
        jsonObject = json.load(dataFile)
        index = 0
        for dataItem in jsonObject['data']:
            index+=1
            print(str(index) + " - " + str(dataItem['utterances']))
            botData = utterance_data.UtteranceData(dataItem['utterances'], dataItem['answer'], dataItem['pattern'], dataItem['flags'], dataItem['type'])
            botData.initializeDoc(nlp)
            dataList.append(botData)
       

        dataFile.close()
    except FileNotFoundError as e:
        loaded = False
        print(f"Can not find file: datafile.json, Exception:  {e}") 
    
    return loaded


def understand(userUtteranceDoc):
    """This method processes an utterance to determine which intent it matches.
    Args:
        utterance (string): A question asked
    Returns:
        UtteranceData: An utterance object containing all needed information.
    """
    
    
    

    # keep the latest element with the longest match
    possibleData = None
    # iterate over  list  and check if utterance matches
    
   
            
        
    for  botData in dataList:
        botData.wordMatchCount(userUtteranceDoc)  
        
    
    
    
    
   
    for  botData in dataList:
        
        if botData.matchUtterance(userUtteranceDoc) :
            #set initial element
            if (possibleData == None):
                possibleData = botData
                
            # compare total group length with next element and set longer to be the possible answer element
            if (possibleData.getGroupsLenght() < botData.getGroupsLenght()):
                possibleData = botData
            
            #if (possibleData.wordMatchCount2() < botData.wordMatchCount2()):
                #possibleData = botData            
            
            
            
            #print("BD CNT: ", botData.wordMatchCount(userUtteranceDoc)) 
            #if (possibleData.wordMatchCount(userUtteranceDoc) < botData.wordMatchCount(userUtteranceDoc)):
                #possibleData = botData                
                   
    # double check the selected element has a match with not zero chars and also no fuzzy counts as they indicte that there are some garbage words present
    # if so then return nothing
    if (possibleData.getGroupsLenght() <= 1): # or (possibleData.getFuzzyCounts() > 0)
        possibleData = None
        
    return possibleData






def get_token(userUtteranceDoc, start_index, attributes):

    for index in range(start_index, len(userUtteranceDoc)):
        token = userUtteranceDoc[index]   
        match_count = 0
        for key in attributes: 
            #print("key:", key, "Value:", attributes[key]) 
            if (getattr(token, key) == attributes[key]):
                match_count+= 1
        
        if match_count == len(attributes):
            print("Token found: " + token.text)
            return token, index
        
    return None, -1   



def processReply(userUtteranceDoc):
    for token in userUtteranceDoc:
            if (token.tag_ == "WDT"):
                print("WH Determiner: " + token.text)
                return token.text 
    return ""    
         

def get_root_verb(userUtteranceDoc):
    for token in userUtteranceDoc:
            if (token.pos_ == "VERB") and (token.dep_ == "ROOT"):
                print("Root Verb: " + token.text); 
                return token.text 
    return "" 

def get_root_verb_direct_object(userUtteranceDoc):
    for token in userUtteranceDoc:
            if (token.pos_ == "NOUN") and (token.dep_ == "dobj"):
                print("Direct Object of the Root Verb: " + token.text); 
                return token.text 
    return "" 
            
def get_adverb(userUtteranceDoc):
    for token in userUtteranceDoc:
            if (token.tag_ == "WRB"):
                print("WG- Adverb: " + token.text); 
                return token.text 
    return ""          
            
      
def get_particle(userUtteranceDoc):
    for token in userUtteranceDoc:
            if (token.pos_ == "PART"):
                print("Particle: " + token.text); 
                return token.text 
    return ""         
      
def get_root_verb_pronoun(userUtteranceDoc):
    for token in userUtteranceDoc:
            if (token.pos_ == "PRON"):
                print("Pronoun: " + token.text); 
                return token.text 
    return ""             


def process_input(utterance):
    """Processes Input from User
    Args:
        utterance (string): A guestion from the user
    Returns:
        string: Response message for the provided user input
    """

    userUtteranceDoc = nlp(utterance)
    intent = understand(userUtteranceDoc)
    
    for token in userUtteranceDoc:
        print(token.text, 
              token.lemma_, 
              token.pos_, 
              token.tag_, 
              token.dep_,
              token.shape_, 
              token.is_alpha, 
              token.is_stop)
        
    processReply(userUtteranceDoc)    
    get_root_verb(userUtteranceDoc)    
    get_root_verb_direct_object(userUtteranceDoc)    
    get_particle(userUtteranceDoc)        #how to make it
   
    get_token(userUtteranceDoc, 0, {"pos_":"VERB", "dep_":"ROOT"}) 
     
        
    if (intent == None):
        
        
            """  start_adverb = get_adverb(userUtteranceDoc)
            if (start_adverb != ""):
                root_verb = get_root_verb(userUtteranceDoc)
                if (root_verb != ""): 
                    direct_object = get_root_verb_direct_object(userUtteranceDoc)
                    if (direct_object == ""):
                      direct_object = get_root_verb_pronoun(userUtteranceDoc)  
                    
                    if (direct_object != ""):
                        particle = get_particle(userUtteranceDoc)
                        print(" Sorry, I dont know " + start_adverb + " " + particle + " " + root_verb + " " + direct_object)   
            """    
        
        
        
            # find what question word is it starting from
            start_adverb, start_adverb_index = get_token(userUtteranceDoc, 0, {"tag_":"WRB"}) 
            
            
            
            # if starting is W-word
            if (start_adverb.tag != None):
                print(" --- Start Adverb: ", start_adverb.text)
                
                # look for TO or is/are
                particle, particle_index = get_token(userUtteranceDoc, start_adverb_index, {"pos_":"PART"})
                if (particle != None): 
                    print(" Particle: ", particle.text)
                    
                    # look for verb
                    root_verb, root_verb_index = get_token(userUtteranceDoc, particle_index, {"pos_":"VERB", "dep_":"ROOT"}) 
                    if (root_verb != None): 
                        print(" Root Verb: ", root_verb.text)
                    
                        # look for NOUN as direct object
                        direct_object, direct_object_index = get_token(userUtteranceDoc, root_verb_index, {"pos_":"NOUN", "dep_":"dobj"})
                        # if could not find noun then look for pronoun EX: it
                        if (direct_object == None):
                            direct_object, direct_object_index = get_token(userUtteranceDoc, root_verb_index, {"pos_":"PRON"}) 
                    
                        if (direct_object != None): 
                            # once noun found
                            print(" Direct Object: ", direct_object.text)             

                            print(" Sorry, I dont know " + start_adverb.text + " " + particle.text + " " + root_verb.text + " " + direct_object.text) 
                
                    
                    
                    
                    
                # if no TO found look for is/are     Auxiliary 
                else:
                    auxiliary, auxiliary_index = get_token(userUtteranceDoc, start_adverb_index, {"pos_":"AUX"}) 
                    if (auxiliary != None): 
                        print(" Auxiliary: ", auxiliary.text)  
                    
                        # look for NOUN as direct object
                        direct_object, direct_object_index = get_token(userUtteranceDoc, auxiliary_index, {"pos_":"NOUN"})
                        
                        # if could not find noun then look for pronoun EX: it
                        if (direct_object == None):
                            direct_object, direct_object_index = get_token(userUtteranceDoc, auxiliary_index, {"pos_":"PRON"}) 
                
                        # if could not find pronoun then look for adj EX: in this case Delphi because it does not know it is a name
                        if (direct_object == None):
                            direct_object, direct_object_index = get_token(userUtteranceDoc, auxiliary_index, {"pos_":"ADJ"})                 
                
                
                        if (direct_object != None): 
                            # once noun found
                            print(" Direct Object: ", direct_object.text)       

                            # look for verb
                            root_verb, root_verb_index = get_token(userUtteranceDoc, direct_object_index, {"pos_":"VERB", "dep_":"ROOT"}) 
                            
                            # if no verb found, look for adjective Developed
                            if (root_verb == None):
                                root_verb, root_verb_index = get_token(userUtteranceDoc, direct_object_index, {"pos_":"ADJ", "dep_":"ROOT"}) 
                            
                            
                            if (root_verb != None): 
                                print(" Root Verb: ", root_verb.text)
                                
                                print(" Sorry, I dont know " + start_adverb.text + " " + direct_object.text + " " + auxiliary.text + " " + root_verb.text) 
                
                
                
                
                
        
        
        
            # format URL properly
            formatted_utterance = userUtteranceDoc.text.replace(" ", "+")
            googleURL = f"https://www.google.com/search?q={formatted_utterance}"
            webbrowser.open(googleURL)
            return (
                True,
                f"Sorry, I don't know the answer to that! Lets check in Google! - {googleURL}",
            )
    elif (intent.type == "farewell"):
        return False, intent.answer
    else:
        return True, intent.answer


def main():
    """Application main method"""
    
    
  
  
    
    
    ## Try to load data from data files. If failed then Exit the program
    if not load_FAQ_data():
        print("Exiting program...\n")
        exit()

    print("\nHello! I am a FAQ Bot. I know all about the best programming language - Delphi. Just ask me.\n")

    keep_conversation = True
    response = ""
    while keep_conversation:
        try:
            keep_conversation, response = process_input(input(">>> "))
            print("\n - " + response + "\n")
        except KeyboardInterrupt:
            print("Application Terminated by User\n")
            exit()


## Run the chat code
# the if statement checks whether or not this module is being run
# as a standalone module. If it is beign imported, the if condition
# will be false and it will not run the chat method.
if __name__ == "__main__":
    main()
