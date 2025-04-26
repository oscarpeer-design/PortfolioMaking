#This Symbolic AI chatbot was developed using NO libraries or API frameworks.

#Symbolic AI techniques
#1. Forward Chaining: use implication, conjunction, disjunction, and negation to make logic from rules
#2. Queries and Backwards Chaining: Determine if a conclusion can be reached by starting with the conclusion first, and working back to find whether said conclusion is true.
#3. Creating new rules from observed facts. This is done via a form of pattern recognition such as inductive reasoning or deductive reasoning.

class SymbolicAi():
    def __init__(self):
        userInput = []
        global FB #assume a human being is using the system

        self.ChatWithUser(FB, userInput)

    class ChatWithUser():
        def __init__(self, FB, userInput):
            self.FB = FB
            self.userInput = userInput
            #This communicates with the user, processes strings, and gets information which is passed to the knowledge base.
            userInput = self.GetInput(FB, userInput)
            #analysis = self.ProcessUserInput(userInput)
            #response = self.GenerateResponse()
            

        class GetInput():
            def __init__(self, FB, userInput):
                self.FB = FB
                self.userInput = userInput

                global breakConversation
                global responseType

                userInput = self.askQuestion(responseType)
                breakConversation = self.checkUserInput(userInput, breakConversation)

                if breakConversation is False:
                    SymbolicAi.ChatWithUser.ProcessUserInput(userInput, FB)
            
            def validateResponseType(self, responseType):
                validResponseType = False
                if len(responseType) == 2:
                    responseNumber = responseType[0]
                    responseString = responseType[1]
                    if type(responseString) is str and type(responseNumber) is int:
                        if responseNumber >= 1 and responseNumber <= 4:
                            validResponseType = True

                return validResponseType

            def askQuestion(self, responseType):
                defaultQuestion = "Tell me something. If you don't want to talk, enter 'X'. "
                
                validResponseType = self.validateResponseType(responseType)

                if validResponseType == True:
                    defaultEnding = "? If you don't want to talk, enter 'X'. " 
                    responseNumber = responseType[0]
                    responseString = responseType[1]
                    
                    if responseNumber == 1 or responseNumber == 2:
                        question = defaultQuestion
                    elif responseNumber == 3:
                        question = "Tell me something about " + responseString + defaultEnding
                    else:
                        question = "What is the " + responseString + defaultEnding

                else:
                    question = defaultQuestion

                userInput = input(question)

                return userInput

            def checkUserInput(self, userInput, breakConversation):
                if userInput == "X":
                    breakConversation = True
                return breakConversation

        class ProcessUserInput():
            def __init__(self, userInput, FB): 
                self.userInput = userInput
                self.FB = FB

                userInput = self.de_Capitalise(userInput)

                listOfWords = self.getListOfUserWords(userInput)
                userClauses = self.getUserClauses(userInput)
                #print(userClauses)

                SymbolicAi.ChatWithUser.GenerateResponse(listOfWords, userClauses, FB)

            def getListOfUserWords(self, userInput):
                listOfWords = []
                
                userInput = self.removePunctuation(userInput)
                listOfWords = self.getListOfWords(userInput)
                listOfWords = self.removeComponentsSpeech(listOfWords)

                return listOfWords

            def getUserClauses(self, userInput):
                userClauses = []

                charsList = self.getListOfCharacters(userInput)
                unPunctuatedClauses = self.breakClauses_Punctuation(charsList)

                for unbrokenClause in unPunctuatedClauses:

                    userClauses.append(self.getListOfWords(unbrokenClause[0]))

                return userClauses

            def breakClauses_Punctuation(self, charsList):
                brokenClauses = [] #this contains a list of strings for each clause that is separated by a punctuation mark

                clauseEndingPunctuation = {".":True, ",":True, "!":True, "?":True, ":":True, ";":True}

                clauseEnds = False
                startPoint = 0

                for i in range(0, len(charsList)):
                    clauseEnds = clauseEndingPunctuation.get(charsList[i])
                    if clauseEnds is True:
                        endPoint = i
                        clauseChars = []

                        while startPoint < endPoint:
                            clauseChars.append(charsList[startPoint])
                            startPoint += 1

                        startPoint = endPoint + 1

                        clauseSentence = self.charsListToString(clauseChars)
                        brokenClauses.append([clauseSentence]) #N.B. put each "sentence" as its own list

                if clauseEnds is False or clauseEnds is None:

                    clauseSentence = self.charsListToString(charsList)
                    brokenClauses.append([clauseSentence])

                return brokenClauses

            def de_Capitalise(self, string):
                string = string.lower() #make all lowercase
                return string

            def getListOfCharacters(self, string):
                charsList = []
                idx = 0

                while idx < len(string):
                    char = string[idx]
                    charsList.append(char)
                    
                    idx += 1

                return charsList

            def charsListToString(self, charsList):
                string = ""
                for char in charsList:
                    string += char

                return string

            def removePunctuation(self, string):
                punctuationList = [".", ",", "!", "?", ":", ";", "(", ")"]
                charIdxToRemove = []
                
                charsList = self.getListOfCharacters(string)
                
                i = 0
                while i < len(charsList):
                    char = charsList[i]
                    j = 0
                    isPunctuationMark = False
                    while isPunctuationMark is False and j < len(punctuationList):
                        if char == punctuationList[j]:
                            isPunctuationMark = True
                            charIdxToRemove.append(i)
                        j += 1
                    i += 1

                idx = len(charIdxToRemove) - 1
                while idx >= 0:
                    charIdx = charIdxToRemove[idx]
                    charsList.pop(charIdx)
                    idx -= 1

                string = self.charsListToString(charsList)

                return string

            def getListOfWords(self, string):
                #print("starting words {}".format(string))
                listOfWords = []
                string += " "
                spaceChar = " " 
                #To convert a string into a list of words we check for spaces. These differentiate one word from the next.
                word = ""
                idx = 0
                while idx < len(string):
                    if string[idx] == spaceChar and word != "":
                       listOfWords.append(word)
                       word = ""
                    elif string[idx] != spaceChar:
                        word += string[idx]
                    idx += 1

                #Removing the space character from the final word
                if len(listOfWords) > 0:
                    lastWordIdx = len(listOfWords) - 1
                    lastWord = listOfWords[lastWordIdx]

                    lastCharIdx = len(lastWord) - 1
                    if lastWord[lastCharIdx] == " ":
                        lastWord = lastWord[:lastCharIdx]

                    listOfWords[lastWordIdx] = lastWord

                #print("list of words {}".format(listOfWords))

                return listOfWords

            def removeComponentsSpeech(self, listOfWords):
                #This removes some components of language from a list of words, getting rid of pronouns, auxilliary verbs, prepositions, and other components of writing.           
                
                ##pronouns = ["i", "he", "she", "they", "them", "me", "my", "we"]
                ##auxilliaryVerbs = ["am", "are", "is", "will", "will be", "a"]
                ##prepositions = ["to", "for", "by", "from","of", "about", "as", "with", "at", "through", "in", "on","inside", "before", "during", "after", "until", "where", "why", "what", "which" "how", "you", "some"]
                ##otherComponents = ["they're", "their", "there", "the", "and"]
                
                componentsDict = {"a":["a", "about", "additionally", "after","also", "am", "and", "an", "are", "at"], "b":["by", "be", "been", "before", "beneath"], "c":["can"], "d":["do", "during"], "f":["for", "from"], "h":["he", "how"], "i":["i", "i'd", "i'll","in", "inside", "is", "isn't", "it"], "o":["of", "on", "our"], "m":["me", "my", "mine"], "s":["she","so", "some"], "t":["the", "their", "them", "they", "they're", "there", "there's", "this", "to"], "u":["until", "us"], "w":["was", "we", "what", "where", "why", "which", "will", "with"], "y":["you", "your", "you're"]} #N.B. everything in this dictionary is in alphabetical order
                idxsToRemove = []

                idx = 0
                while idx < len(listOfWords):
                    word = listOfWords[idx]
                    try: 
                        char = word[0] #first character of every word
                        correspondingWords = componentsDict.get(char)
                        if correspondingWords is not None: 
                            wordMatch = False
                            #checking the word against other words that we wish to remove that start with the same letter
                            j = 0
                            while wordMatch is False and j < len(correspondingWords):

                                if word == correspondingWords[j]:
                                    wordMatch = True
                                    idxsToRemove.append(idx)
                                j += 1
                    except:
                        idx += 1
                    idx += 1

                i = len(idxsToRemove) - 1
                while i >= 0:
                    idxToCull = idxsToRemove[i]
                    listOfWords.pop(idxToCull)
                    i -= 1

                return listOfWords

            def recogniseSynonyms(self, listOfWords):
                return listOfWords

            def turnTextToRules(self):
                #This turns a string of text into a list of preconditions and postconditions
                FB = []
                return FB

        class GenerateResponse():
            def __init__(self, userInputsList, userClauses, FB):

                self.userInputsList = userInputsList
                self.userClauses = userClauses

                userEmotions = self.recogniseEmotions(userInputsList)
                emotionalResponse = self.getEmotionalResponse(userEmotions)
                self.outputRespose(emotionalResponse)

                SymbolicAi.AnalyseData(userInputsList, userEmotions, userClauses, FB)

            def recogniseEmotions(self, userInputsList):
                #This recognises an emotion and uses said emotion to generate a generic response. It also replaces the emotional synonym in the user's input with a simpler synonym. Note that I have paid more attention to the connotations of words than to their literal meaning.
                
                #emotionsMap = [ [["sad", "sadness", "sorrow", "sorrowful", "grief", "grieves", "melancholy", "depressed", "depression", "forlorn"],"sadness"], [["happy", "happiness", "joy", "joyous", "joyful", "halcyon", "delight", "delighted", "delightful", "gay", "gaeity", "jolly", "wonderful"], "happiness"], [["frustrated","frustrate","frustrates","impatient", "impatience", "annoy", "annoys", "annoyed", "annoyance"],"frustration"], [["angry", "anger", "angers", "angrier","angered", "bucolic", "rage", "rages", "enraged", "rageful", "upset", "upsets", "supsetting", "apoplectic"], "anger"], [["suprised", "suprise", "astound", "astounded", "astonishing", "unbelievable"],"suprise"], [["shocked", "shock", "flabbergasted", "incredulous", "horror", "horrified"], "shock"], [["curious","curiousity","wonders","wonder","wondering"], "curiousity"], [["love", "loved", "loves", "loving", "adore", "adored", "adores", "adoring"], "love"] ]
                
                emotionsMapDict = {"a":{"adore":"love", "adored":"love", "adores":"love", "adoring":"love", "anger":"anger", "angers":"anger", "angry":"anger", "angrier":"anger","angered":"anger", "annoy":"frustration", "annoyed":"frustration", "annoys":"frustration", "annoyance":"frustration", "apoplectic":"anger", "appall":"shock", "appalled":"shock", "appalling":"shock", "astound":"suprise", "astounds":"suprise", "astounded":"suprise", "astonish":"suprise", "astonished":"suprise", "astonishes":"suprise", "astonishing":"suprise"}, "b":{"bucolic":"anger"}, "c":{"curious":"curiousity", "curiousity":"curiousity"}, "d":{"delight":"happiness", "delighted":"happiness", "delightful":"happiness", "depressed":"sadness", "depression":"sadness", "disbelief":"suprise"}, "e":{"enraged":"anger"}, "f":{"flabbergasted":"shock", "forlorn":"sadness", "frustrate":"frustration", "frustrated":"frustration", "frustrates":"frustration", "frustration":"frustration", "furious":"anger"}, "g":{"gay":"happiness", "gaiety":"happiness", "grief":"sadness", "grieves":"sadness"}, "h":{"halcyon":"happiness","happy":"happiness", "happiness":"happiness", "horror":"shock", "horrified": "shock", "horrific":"shock"}, "i":{"impatient":"frustration", "impatience":"frustration", "incredulous":"shock", "incredulously":"shock"}, "j":{"joy":"happiness", "joyful":"happiness", "joyous":"happiness", "jolly":"happiness"}, "l":{"love":"love", "loved":"love", "loves":"love", "loving":"love"}, "m":{"melancholy":"sadness", "miserable":"sadness", "mortify":"shock", "mortified":"shock"}, "r":{"rage":"anger", "raged":"anger", "rages":"anger"}, "s":{"sad":"sadness", "sadness":"sadness", "shock":"shock", "shocked":"shock", "sorrow":"sadness", "sorrowful":"sadness", "suprise":"suprise", "suprised":"suprise"}, "u":{"unhappy":"sadness", "unbelievable":"suprise", "upset":"anger", "upsets":"anger", "upsetting":"anger"}, "w":{"wonder":"curiousity", "wondered":"curiousity", "wonderful":"happiness", "wonders":"curiousity", "wondering":"curiousity"}} #N.B. This is in alphabetical order.
                userEmotions = []

                for userInput in userInputsList: 
                    matchFound = False

                    firstChar = userInput[0]
                    emotions_sameChar = emotionsMapDict.get(firstChar)
                    if emotions_sameChar is not None:
                        newEmotion = emotions_sameChar.get(userInput)
                        if newEmotion is not None:
                            userEmotions.append(newEmotion)

                return userEmotions

            def alterForPositiveEmotions(self, emotionalResponse, userEmotions, responsesBank):
                
                if userEmotions[1] == "happiness": #happiness is last emotion
                    emotionalResponse = responsesBank.get("happiness")[2] 
                elif userEmotions[1] == "love": #love is last emotion
                    emotionalResponse = responsesBank.get("love")[0]

                return emotionalResponse

            def alterForNegativeEmotions(self, emotionalResponse, userEmotions, responsesBank):
                
                if userEmotions[1] == "sadness":
                    emotionalResponse = responsesBank.get("sadness")[1]
                elif userEmotions[1] == "anger":
                    emotionalResponse = responsesBank.get("anger")[2]
                elif userEmotions[1] == "shock":
                    emotionalResponse = responsesBank.get("shock")[1]
                elif userEmotions[1] == "frustration":
                    emotionalResponse = responsesBank.get("frustration")[2]

                return emotionalResponse

            def getEmotionalResponse(self, userEmotions):
                responsesBank = {"sadness":["Oh I'm sorry.","That sounds awful.","I get that you're sad and upset."], "happiness":["Wow that's great!", "I'm happy for you.","How wonderful!"], "frustration":["Yeah I get it. That sounds annoying.","Wow that's frustrating.","That must make you feel really angry and upset."], "anger":["That sounds upsetting.","I get how you feel.","That must make you feel really angry and upset."], "suprise":["That is a suprise.","That's a suprise. Thanks for telling me.","What a wonderful suprise."], "shock":["That sounds shocking.", "I am astounded too.", "I understand that this must be really shocking and upsetting to you."], "curiousity":["That sounds interesting.","Wow. That's fascinating!","I envy your happiness and curiousity. When I was young, I too was an adventurous lad."], "love":["That sounds wonderful.","I am extremely happy. That sounds incredible.","What a wonderful experience."]}
                
                emotionalResponse = ""
                length = len(userEmotions)

                if length > 0:
                    responseList = responsesBank.get(userEmotions[0])
                    if length <= 1:
                        emotionalResponse = responseList[0]
                    elif length > 1 and length < 3: #alternatively get 3rd emotional response
                        if userEmotions[0] == "anger" or userEmotions[1] == "anger":
                            emotionalResponse = responsesBank.get("anger")[2]
                            emotionalResponse = self.alterForPositiveEmotions(emotionalResponse, userEmotions, responsesBank)
                        elif userEmotions[0] == "frustration" or userEmotions[1] == "frustration":
                            emotionalResponse = responsesBank.get("frustration")[1]
                            emotionalResponse = self.alterForPositiveEmotions(emotionalResponse, userEmotions, responsesBank)
                        elif userEmotions[0] == "sadness" or userEmotions[1] == "sadness":
                            emotionalResponse = responsesBank.get("sadness")[1]
                            emotionalResponse = self.alterForPositiveEmotions(emotionalResponse, userEmotions, responsesBank)
                        elif userEmotions[0] == "happiness" or userEmotions[1] == "happiness":
                            emotionalResponse = responsesBank.get("happiness")[2]
                        elif userEmotions[0] == "suprise" or userEmotions[1] == "suprise":
                            emotionalResponse = responsesBank.get("suprise")[1]
                        elif userEmotions[0] == "curiousity" or userEmotions[1] == "curiousity":
                            emotionalResponse = responsesBank.get("curiousity")[2]
                        elif userEmotions[0] == "love" or userEmotions[1] == "love":
                            emotionalResponse = responsesBank.get("love")[2]
                    else:
                        emotionalResponse = "That sounds really complicated. I guess feelings can be like that."
                    
                return emotionalResponse

            def getGenericResponse(self, userInputsList):
                genericResponsesBank = {}

            def outputRespose(self, response):
                if response != None and response != "":
                    print(response)

    class AnalyseData():
        def __init__(self, userInputsList, userEmotions, userClauses, FB):
            self.userInputsList = userInputsList
            self.userEmotions = userEmotions
            self.FB = FB

            global RB
            global negationBank
            global disjunctionBank

            newRules = {}
            inferredFacts = []

            KB = self.KnowledgeBase(FB, RB, userInputsList, userClauses, userEmotions, negationBank, disjunctionBank, newRules)
            self.ApplyRules(KB, newRules, inferredFacts)

            SymbolicAi.VerifyOutput(newRules, inferredFacts, KB.RB, KB.FB)

        class KnowledgeBase():
            def __init__(self, FB, RB, userInputsList, userClauses, userEmotions, negationBank, disjunctionBank, newRules):
            #The knowledge base is a set of rules and facts that enable deduction. Note that the KB should be able to grow as more data is processed.
                self.userInputsList = userInputsList
                self.userEmotions = userEmotions
                self.RB = RB
                self.FB = FB #This is the Facts Base. It contains facts about a person
                self.negationBank = negationBank
                self.disjunctionBank = disjunctionBank
                self.newRules = newRules

                self.ProcessNewInformation(userClauses, self.RB, newRules)

                FB.append(userInputsList)
                if userEmotions != [] and userEmotions is not None:
                    FB.append(userEmotions)

            def addNewRule_MainRB(Rules, newPrecondition, newPostcondition):
                Rules.setdefault(newPrecondition, newPostcondition)
                #RB.update({newPrecondition:newPostcondition})
                return Rules

            class ProcessNewInformation():
                def __init__(self, userClauses, RB, newRules):
                    self.userClauses = userClauses 
                    self.RB = RB
                    self.newRules = newRules

                    for i in range(0, len(userClauses)):
                        clause = userClauses[i]
                        clause = self.removeWordsFromClause(clause)
                        clause = self.concatenateCausalWords(clause)
                        
                    #print("clauses {}".format(userClauses))
                    RB = self.establishCausalityFromUserInput(userClauses, RB, newRules)

                def removeWordsFromClause(self, userWords):
                    wordsToRemoveDict = {"a":True, "and":True, "of":True, "to":True} #Because only the user inputs list and not the clauses is wiped of unnecessary words I have a dictionary of words here that can be removed.
                    wordNeedsRemoving = False

                    wordsToRemove = []

                    for word in userWords:
                        wordNeedsRemoving = wordsToRemoveDict.get(word)

                        if wordNeedsRemoving is True:
                            wordsToRemove.append(word)

                    for wordToCull in wordsToRemove:
                        userWords.remove(wordToCull)

                    return userWords

                def concatenateCausalWords(self, clauses):
                    clauseWordDict = {"c":"consequence", "d":"due", "r":"result"} #Here are someords that are commonly used to form transition clauses. They are in alphabetical order.
                    
                    idxsToRemove = []
                    i = 1
                    length = len(clauses)
                    while i < length - 1:
                        #print("userWords at i {} : {}".format(i, clauses[i])) #debugging output statement
                        firstChar = clauses[i][0]
                        relatedClause = clauseWordDict.get(firstChar)

                        if relatedClause is not None:

                            if relatedClause == "consequence" and clauses[i - 1] == "as":
                                clauses[i] = "as consequence"
                                idxsToRemove.append(i-1)

                            elif relatedClause == "due" and clauses[i + 1] == "to":
                                clauses[i] = "due to"
                                idxsToRemove.append(i+1)

                            elif relatedClause == "result" and clauses[i - 1] == "as":
                                 clauses[i] = "as result"
                                 idxsToRemove.append(i-1)

                        i += 1

                    j = len(idxsToRemove) - 1
                    while j >= 0:
                        idxToCull = idxsToRemove[j]
                        clauses.pop(idxToCull)
                        j -= 1

                    #print(clauses) #DEBUGGING OUTPUT STATEMENT

                    return clauses

                def getCausalWordIdx(self, clauseWords):
                    #print(clauseWords)
                    causalWordsDict = {"a":["as result", "as consequence"],"b":["because"],"c":["consequently", "cause", "caused", "causes"],"d":["due"], "r":["resulted", "resulting"], "t":["therefore","thus"]} #N.B. This is in alphabetical order
                    causalIdx = 0 #Tracks the index of the first causal word found
                    causalWordFound = False

                    i = 0
                    while causalWordFound is False and i < len(clauseWords):
                        word = clauseWords[i]
                        firstChar = word[0]
                        relatedCausalWords = causalWordsDict.get(firstChar)
                        #if relatedCausalWords  is not None:
                        if type(relatedCausalWords) == list:
                            j = 0
                            
                            while causalWordFound is False and j < len(relatedCausalWords):
                                #print("causalWord {}, word {}".format(relatedCausalWords[j], word))
                                if relatedCausalWords[j] == word:
                                    causalIdx = i
                                    causalWordFound = True
                                j += 1

                        i += 1

                    return causalIdx, causalWordFound

                def concatenateConditionFromList(self, wordsList):
                    if len(wordsList) > 0:
                        condition = ""
                        length = len(wordsList)
                        if length == 1:
                            condition = wordsList[0]
                        else:
                            for i in range(0, length):
                                condition = condition + wordsList[i] + " "
                        return condition

                def addRules_determinedCausality(self, newPreconditionsList, newPostconditionsList, RB, newRules):
                    preconIdx = 0
                    postconIdx = 0

                    while preconIdx < len(newPreconditionsList) and postconIdx < len(newPostconditionsList):
                        #print("precondition: {}, poscondition: {}".format(newPreconditionsList[preconIdx], newPostconditionsList[postconIdx])) #DEBUGGING OUTPUT STATEMENT
                        precondition = newPreconditionsList[preconIdx]
                        postcondition = newPostconditionsList[postconIdx]

                        if precondition is not None and postcondition is not None:
                            RB = SymbolicAi.AnalyseData.KnowledgeBase.addNewRule_MainRB(RB, precondition,postcondition)
                            newRules.setdefault(precondition, postcondition)
                        else:
                            break

                        preconIdx += 1
                        postconIdx += 1

                    #print(RB) #DEBUGGING OUTPUT STATEMENT

                    return newRules

                def validateConditionWords(self, conditionWordsList):
                    validCondition = False
                    if len(conditionWordsList) > 0: #1st check list not empty
                        validCondition = True

                    return validCondition

                def establishCausalityFromUserInput(self, userClauses, RB, newRules): 
                    #This algorithm generates new rules based on transition words employed by the user in their input prompt
                    #causalWords = ["thus", "consequently", "because", "due to this reason", "due to this", "as a result", "as a result of", "resulting from", "resulted from"]
                    newPreconditionsList = []
                    newPostconditionsList = []

                    for clause in userClauses:
                        #SOMETHING DOESN'T WORK HERE:
                        #E.G. I am sad as a result of a recent breakup. I am lost as a consequence of being found. I travel as a result of my need to explore.
                        #When the words "as" and "a" are used, the proper transition words are not concatenated
                        causalWordIdx, causalWordFound = self.getCausalWordIdx(clause) #ERROR LIES IN THIS FUNCTION                      

                        #print("causalWordFound {}".format(causalWordFound)) #DEBUGGING OUTPUT STATEMENT
                        if causalWordFound is True:
                           
                           start = 0
                           end = len(clause)

                           newPreconditionWords = clause[start:causalWordIdx]
                           newPostconditionWords = clause[causalWordIdx+1:end]

                           #print("newPreconditionWords {}".format(newPreconditionWords)) #DEBUGGING OUTPUT STATEMENT
                           #print("newPostconditionWords {}".format(newPostconditionWords)) #DEBUGGING OUTPUT STATEMENT

                           validPrecon = self.validateConditionWords(newPreconditionWords)
                           validPostcon = self.validateConditionWords(newPostconditionWords)

                           if validPrecon is True and validPostcon is True:
                               newPreconditionsList.append(self.concatenateConditionFromList(newPreconditionWords))
                               newPostconditionsList.append(self.concatenateConditionFromList(newPostconditionWords))

                    self.addRules_determinedCausality(newPreconditionsList, newPostconditionsList, RB, newRules)
                    
                    return RB

        class ApplyRules():
            def __init__(self, KB, newRules, inferredFacts):
                self.KB = KB
                self.newRules = newRules
                self.inferredFacts = inferredFacts

                self.forwardChaining(KB.FB, KB.RB, inferredFacts)
                self.Generating_AddingRules(FB, RB, newRules)

                #print("facts base: {}".format(KB.FB))
                #print("rules base: {}".format(KB.RB))

                self.removeDuplicateValues(KB.negationBank)
                self.removeDuplicateValues(KB.disjunctionBank)

            def forwardChaining(self, FB, RB, inferredFacts):
                #Forward chaining takes rules and given facts, and uses the rules given to deduce new rules and new facts.
                factsListIdx = 0
                while factsListIdx < len(FB):
                    factsList = FB[factsListIdx]
                    self.implication(factsList, inferredFacts, factsListIdx, FB, RB)
                    
                    factsListIdx += 1

            def Generating_AddingRules(self, FB, RB, newRulesDict):

                #newRule = inductiveReasoning([["woman or man or boy or girl", "human"], ["woman or man or boy or girl", "human"], ["man", "human"]])
                newRule = self.inductiveReasoning(FB, )
                #print(newRule) #DEBUGGING OUTPUT STATEMENT
                if len(newRule) > 0 and len(newRule) < 3: #check if empty and if contains 2 strings
                    newPrecondition = newRule[0]
                    newPostcondition = newRule[1]

                    RB = self.addNewRule_MainRB(RB, newPrecondition, newPostcondition) #add the new rule to the Rules Base
                    newRulesDict.setdefault(newPrecondition, newPostcondition)
                    #If a rule's precondition contains 'or' or 'not', either the disjunction bank or the negation bank must be updated.
        
                    isNegation, isDisjunction, listOfWords = self.checkPrecondition(newPrecondition)  #test with string: "not human or not mortal" and "neither apple nor fruit"    
                    #print("negation: {}, disjunction: {}".format(isNegation, isDisjunction))

                    termsPrecondition = self.searchTerms_InList(listOfWords) #removing terms such as 'or', 'not', 'are', 'is'
                    termsPostcondition = self.searchTerms_InList(self.getListOfWords_FromString(newPostcondition))

                    enoughTermsPresent = False
                    #If the precondition has more than three words in it, it must contain two terms. As such, the negation bank will be updated with only the precondition supplying the rule and the two terms supporting said rule..
                    if len(listOfWords) > 3:
                        enoughTermsPresent = True

                    if isNegation is True and isDisjunction is False:
                        #Add new rule to negationBank
                        self.addNewRule_NegationBank(newPrecondition, newPostcondition, termsPrecondition, termsPostcondition, enoughTermsPresent)

                    elif isNegation is False and isDisjunction is True:
                        #Add new rule to disjunctionBank
                        self.addNewRule_DisjunctionBank(newPrecondition, termsPrecondition)

                    elif isNegation is True and isDisjunction is True:
                        #Add new rule to negationBank
                        self.addNewRule_NegationBank(newPrecondition, newPostcondition, termsPrecondition, termsPostcondition, enoughTermsPresent)
        
                    else:
                        #if len(listOfWords) == 1: #expect to only add single-word strings as terms
                        self.addNewTerm_DisjunctionBank(newPrecondition, newPostcondition)
                        #See if terms can be added to a string in the disjunctionBank.

            def removeDuplicateValues(self, dictOfLists):
                #This algorithm searches through the negation bank and the disjunction bank to ensure that the lists corresponding to each dictionary key do not contain duplicate values
                maxNum = 1
                keysList = list(dictOfLists.keys())
    
                listDuplicates = []

                termsDict = {}
                #THIS ALGORITHM HAS A TIME COMPLEXITY OF O(N^3). PLEASE, FOR THE LOVE OF ALL THAT IS GOOD ON THIS EARTH, REFACTOR IT!
                for key in keysList: 
                    termsList = dictOfLists.get(key)
                    termsDict = self.getDictShowingTimesElementOccurs([termsList]) #N.B. the function only accepts a list of lists, so our list is wrapped inside another list
                    termsKeysList = list(termsDict.keys())

                #print(termsDict) #DEBUGGING OUTPUT STATEMENT

                    for term in termsKeysList:
                        numOccurs = termsDict.get(term)

                        if numOccurs > maxNum:
                            indexesToRemove = []
                            numDuplicates = numOccurs - maxNum
                            #print("number of duplicates of term ({}): {}".format(term,numDuplicates))
                            duplicates = numDuplicates
                            idx = 0
                
                            while idx < len(termsList) and duplicates >= 0:
                                if term == termsList[idx]: #and duplicates != numDuplicates: #Ignore first non-duplicate term and only remove subsequent terms
                                    indexesToRemove.append(idx)
                                    #print(indexesToRemove)
                                    duplicates -= 1
                                idx += 1
                
                            #make sure lowest index is removed from indexesToRemove to preserve original value
                            indexesToRemove.pop(0)

                            #print(termsList)
                            #print("indexes to remove in list: {}".format(indexesToRemove))

                            j = len(indexesToRemove) - 1

                            while j >= 0:
                                idxToCull = indexesToRemove[j]
                                termsList.pop(idxToCull)
                                j -= 1

                return dictOfLists

            
            def implication(self, factsList, inferredFacts, factsListIdx, FB, RB):
                #IF-THEN or implication says that if one condition is true, another must also be true
                #This also handles negation (NOT operation), whereby if one condition is true, another must be false
                i = 0
                while i < len(factsList): 
                #factsList is one item in the FB. It is a list within a list.
                    newInfo = factsList[i]
                    added = False
                    newFact = RB.get(newInfo)
                    #If a given conclusion fits the rules and does not already exist in the facts list it is added.
                    if newFact is not None:
                        factExisting = self.checkFactExists(newFact, factsListIdx, FB)
                        if factExisting is False: 
                            added = True
                            #print(newFact) #DEBUGGING OUTPUT STATEMENT
                            self.addToFacts(newFact, factsList, inferredFacts, factsListIdx)
                        else:
                            print("Fact already accounted for") #DEBUGGING OUTPUT STATEMENT
                    i += 1
                #N.B. The updated facts are passed back by reference, owing to the fact that FB, as a list, is a mutable data type.

            def getListOfWords_FromString(self, string):
                listOfWords = []
                string += " "
                spaceChar = " " 
                #To convert a string into a list of words we check for spaces. These differentiate one word from the next.
                word = ""
                idx = 0
                while idx < len(string):
                    if string[idx] != spaceChar:
                        word += string[idx]
                    else:
                        listOfWords.append(word)
                        word = ""
                    idx += 1

                return listOfWords

            def searchTerms_InList(self, listOfWords):
                terms = []
                auxilliaryVerbs = ["are", "not", "is", "neither", "nor", "or", "as"]
                for word in listOfWords:
                    count = 0
                    notAuxVerb = True
                    while count < len(auxilliaryVerbs):
                        if word == auxilliaryVerbs[count]:
                            notAuxVerb = False
                    
                        count += 1

                    if notAuxVerb is True:
                        terms.append(word)

                return terms

            def getItem_fromDictionaryOfLists(self, dictionary, info1, info2):
                #This function gets the relevant key from a {dictionary:[list]} data structure and returns this key.
                #If no key is found, None is returned.
                #print("info1: {} info2: {}".format(info1, info2)) #DEBUGGING OUTPUT STATEMENT

                item = ""
                i = 0
                found = False
                keysList = list(dictionary.keys())
                length = len(keysList)

                while i < length and found is False:
                    itemKey = keysList[i]
                    #print("itemKey: {}".format(itemKey)) #DEBUGGING OUTPUT STATEMENT
                    itemsList = dictionary.get(itemKey)
                    #print("itemsList: {}".format(itemsList)) #DEBUGGING OUTPUT STATEMENT
                    j = 0
                    while j < len(itemsList) and found is False:
                        item = itemsList[j]
                        #print("item: {}".format(item)) #DEBUGGING OUTPUT STATEMENT

                        if  info1 == item or info2 == item:
                            found = True
                            #print("found: {}".format(found)) #DEBUGGING OUTPUT STATEMENT
                        j += 1
                    i += 1
                if found is True:
                    return itemKey
                else:
                    return None

            def negation(self, fact1, fact2, RB):
                negatedFact = "" 
    
                global negationBank

                condition = self.getItem_fromDictionaryOfLists(negationBank, fact1, fact2)
                #print("condition: {}".format(condition)) #DEBUGGING OUTPUT STATEMENT
                conclusion = RB.get(condition)

                if conclusion is not None:
                    negatedFact = conclusion
                    return negatedFact
                else:
                     #if no match can be found, None is returned
                  return None

            def conjunction(self, fact1, fact2, RB):
                #AND operation: both facts must be true
                #If a fact is true, it must link to a rule in the RB
                newFact = ""
                condition1 = fact1 + " and is " + fact2
                condition2 = fact2 + " and is " + fact1

                conclusion1 = RB.get(condition1)
                conclusion2 = RB.get(condition2)

                if conclusion1 is not None:
                    newFact = conclusion1
                elif conclusion2 is not None:
                    newFact = conclusion2
                else:
                    newFact = self.negation(fact1, fact2, RB)

                return newFact

            def disjunction(self, fact1, fact2, RB):
                #OR operation: either fact must be true
                #If a fact is true, it must link to a rule in the RB
                global disjunctionBank
    
                newFact = ""
                condition = self.getItem_fromDictionaryOfLists(disjunctionBank, fact1, fact2)
                conclusion = RB.get(condition)

                if conclusion is not None:
                    newFact = conclusion
                else:
                    newFact = self.negation(fact1, fact2, RB)
                return newFact

            def findLargestInDict(self, largest, secondLargest, termsList, termsDict):
                mostCommon = ""
                if largest == 2 and secondLargest == 1: #indicates largest hasn't been found
                    for term in termsList:
                        num = termsDict.get(term)
                        if  num > largest:
                            largest = num
                            mostCommon = term
                    big = largest
                else: #indicates most common term has been found
                    for term in termsList:
                        num = termsDict.get(term)
                        if num < largest and num >= secondLargest:
                            secondLargest = num
                            mostCommon = term
                            big = secondLargest
                return big, mostCommon

            def checkValid(self, largest, secondLargest, termsList, termsDict):
                #This algorithm checks if the rule is valid by looking at the repetition of strings in the lists given. It returns a boolean, 'valid', and an error message string, 'errorMsg.'

                valid = True
                errorMsg = ""
                #Check if a pattern cannot be distinguished due to a lack of repetition
                if largest < 2 or secondLargest < 2:
                    valid = False
                    errorMsg = "No pattern percievable."
                #Check if a pattern cannot be distinguished due to issues of causality.
                elif largest == secondLargest: 
                    valid = False
                    errorMsg = "Causality issues."
                
                #If multiple terms are repeated the same number of times, it is impossible to determine which are the most common and second most common. As a result, causality is indeterminable.
                idx = 0
                count_MostCommon = 0
                count_2ndMostCommon = 0
                while idx < len(termsList) and count_MostCommon < 2 and count_2ndMostCommon < 2:
                    key = termsList[idx]
                    num = termsDict.get(key)
                    if  num == largest:
                        count_MostCommon += 1
                    elif num == secondLargest:
                        count_2ndMostCommon += 1
                    idx += 1
    
                if count_MostCommon >= 2 or count_2ndMostCommon >= 2:
                    valid = False
                if len(errorMsg) < 1:
                    errorMsg = "Difficulty discerning most common and second most common elements."

                return valid, errorMsg

            def getDictShowingTimesElementOccurs(self, listOfLists):
                termsDict = {}
                #This dictionary shows how often each string occurs in a list of lists

                for array in listOfLists:
                    for term in array:
                        inc = termsDict.get(term)
                        if inc is None:
                            termsDict.setdefault(term,1)
                        else:
                            inc += 1
                            termsDict.update({term:inc})
                    
                return termsDict

            def inductiveReasoning(self, FB):
                #In our symbolic AI we want to be able to create new rules from patterns within existing facts. This is done via inductive reasoning.
                #In Inductive Reasoning, we create observations from these patterns and use these observations to create generalised rules. These rules are then tested based on the existing data.
                #To do this we look through our lists of facts to determine whether any facts go together and create an appropriate generalisation. If multiple facts lead to a single generalisation, this generalisation is added as a rule.
                newRule = [] 
                #Set this to list. If the list is empty or null it is not valid.
    
                if len(FB) > 1: 
                    termsDict = {} #This item contains all the terms in the FB and how often they occur
                    termsDict = self.getDictShowingTimesElementOccurs(FB)
                    #print("termsDict: {}".format(termsDict))
                    #search for the most common and second most common terms in the dictionary
                    largest = 2
                    secondLargest = 1
                    mostCommon = ""
                    secondMostCommon = ""

                    #print(termsDict) #DEBUGGING OUTPUT STATEMENT
                    termsList = list(termsDict.keys())
                    largest, mostCommon = self.findLargestInDict(largest, secondLargest, termsList, termsDict)
                    secondLargest, secondMostCommon = self.findLargestInDict(largest, secondLargest, termsList, termsDict)

                    #print("largest: {}, second largest: {}".format(largest, secondLargest)) #DEBUGGING OUTPUT STATEMENT
                    #print("most common: {}, second most common: {}".format(mostCommon, secondMostCommon)) #DEBUGGING OUTPUT STATEMENT

                    #checking rule is valid
                    errorMsg = ""
                    validRule, errorMsg = self.checkValid(largest, secondLargest, termsList, termsDict)
                    if validRule == False:
                        print(errorMsg)
                    else:
                        #[precondition =  second most common term, postcondition = most common term]
                        newRule = [secondMostCommon, mostCommon]
                else:
                    print("Insufficient data for pattern recognition.")

                return newRule

            def addNewRule_MainRB(self, Rules, newPrecondition, newPostcondition):
                Rules.setdefault(newPrecondition, newPostcondition)
                #RB.update({newPrecondition:newPostcondition})
                return Rules

            def addToFacts(self, newFact, factsList, inferredFacts, factsListIdx):
                factsList.append(newFact)
                inferredFacts.append([newFact, factsListIdx])

            def checkFactExists(self, newFact, factsListIdx, FB):
                lim = 2 #Go maximum of two idxs backwards in the FB
                count = 1

                factFound = False

                i = factsListIdx
                while i >= 0 and count <= lim and factFound is False:
                    factsList = FB[i]
                    j = 0
                    while j < len(factsList) and factFound is False:
                        if factsList[j] == newFact:
                            factFound = True
                        j += 1

                    count += 1
                    i -= 1

                return factFound

            def addNewRule_DisjunctionBank(precondition, preconditionTerms):
                global disjunctionBank
                #This adds keys and values to the disjunctionBank
                disjunctionBank.setdefault(precondition, preconditionTerms)
                #print(disjunctionBank) #DEBUGGING OUTPUT STATEMENT

            def addNewRule_NegationBank(precondition, postcondition, termsPrecondition, termsPostcondition, enoughTermsPresent):
                #print("precondition: {}, postcondition: {}".format(precondition, postcondition)) #DEBUGGING OUTPUT STATEMENT
                global negationBank
                #This adds keys and values to the negationBank

                termsList = []

                for i in range(0, len(termsPrecondition)):
                    term = "not " + termsPrecondition[i]
                    termsList.append(term)

                if enoughTermsPresent is False: #The precondition does not contain more than two words, and therefore, the postcondition needs to be added to increase the length of the negation bank.

                    for j in range(0, len(termsPostcondition)):
                        term = "not " + termsPostcondition[j]
                        termsList.append(term)

                    negationBank.setdefault(precondition, termsList)
                    #print(negationBank) #DEBUGGING OUTPUT STATEMENT

            def addNewTerm_DisjunctionBank(self, precondition, postcondition):
                #print("precondition: {} postcondition: {}".format(precondition, postcondition)) #DEBUGGING OUTPUT STATEMENT
    
                global disjunctionBank
                #Here, we add new terms to the disjunction bank. We check if they fit within any term in the dictionary and then determine if the term to be added is unique.
                #N.B. This algorithm only takes in single-word string values as parameters. E.g. "apple", "coconunt", "fruit"
                disjunctionBank_Keys = list(disjunctionBank.keys())
    
                keyCount = 0
                matchFound = False

                while keyCount < len(disjunctionBank_Keys) and matchFound is False:
                    #search every word of every key in the dictionary to find a match
                    key = disjunctionBank_Keys[keyCount]
                    key_wordsList = self.getListOfWords_FromString(key)
                    keyTerms = self.searchTerms_InList(key_wordsList)

                    termCount = 0

                    while termCount < len(keyTerms) and matchFound is False:
                        termInKey = keyTerms[termCount]
                        if postcondition == termInKey:
                            value = precondition
                            matchFound = True
                        elif precondition == termInKey:
                            value = postcondition
                            matchFound = True
                        termCount += 1

                    keyCount += 1

                if matchFound is True:
                    #add the term into the list at the corresponding key
                    valuesList = disjunctionBank.get(key)
                    valuesList.append(value)

                    #print(disjunctionBank) #DEBUGGING OUTPUT STATEMENT

            def checkPrecondition(self, precondition):
                isNegation = False
                isDisjunction = False
                listOfWords = self.getListOfWords_FromString(precondition)
                for word in listOfWords:
                    if word == "or":
                        isDisjunction = True
                    elif word == "not" or word == "neither":
                        isNegation = True

                return isNegation, isDisjunction, listOfWords

    class VerifyOutput():
        def __init__(self, newRules, inferredFacts, RB, FB):
            self.newRules = newRules
            self.inferredFacts = inferredFacts
            #Here the symbolic ai confirms whether or not its deductions are true.

            validFacts, validRules = self.checkRulesAndFacts(newRules, inferredFacts)



            if validFacts == True:
                self.verifyDeducedFacts(inferredFacts, FB)

            if validRules == True:
                self.verifyDeducedRules(newRules, RB)
            
            responseNumber = self.adjustResponseNumber(validFacts, validRules)
            
            self.adjustResponseType(responseNumber, inferredFacts, newRules, validFacts, validRules)

            self.refireAI()

        def checkRulesAndFacts(self, newRules, inferredFacts):
            #This checks whether any rules or facts have in fact been deduced.
            validFacts = True
            validRules = True
            if len(inferredFacts) == 0: #check empty list
                validFacts = False   

            if newRules == {}: #check empty dictionary
                validRules = False

            return validFacts, validRules

        def removeFact(self, inferredFact, FB):
            #relevantList =  FB[inferredFact[1]]
            relevantListIdx = inferredFact[1]
            relevantFact = inferredFact[0]
            FB[relevantListIdx].remove(relevantFact)

        def verifyDeducedRules(self, newRules, RB):
            question = "Is it true that {} because {}? Answer 'Y' for yes and 'N' for no. "
            preconsList = list(newRules.keys())
            postconsList = list(newRules.values())
            
            i = 0
            j = 0

            while i < len(preconsList) and j < len(postconsList):
                validAnswer = False
                while validAnswer is False:
                    confirmation = input(question.format(preconsList[i], postconsList[j]))
                    if confirmation == "Y":
                        validAnswer = True
                    elif confirmation == "N":
                        validAnswer = True
                        #Remove the rule from the RB
                        keyToRemove = preconsList[i]
                        RB.pop(keyToRemove)
                    else:
                        print("Invalid response. Please try again.")

                i += 1
                j += 1

        def verifyDeducedFacts(self, inferredFacts, FB):
            print("inferredFacts {}".format(inferredFacts))

            question = "Is it true that you are {}? Answer 'Y' for yes and 'N' for no. "
            for fact in inferredFacts: #N.B. each 'fact' contains a fact and the index of the list in the FB in which said fact is located 
                validAnswer = False
                while validAnswer is False:
                    confirmation = input(question.format(fact[0]))
                    if confirmation == "Y":
                        validAnswer = True
                    elif confirmation == "N":
                        validAnswer = True
                        #remove fact from FB
                        self.removeFact(fact, FB)
                    else:
                        print("Invalid response. Please try again.")
        
        def adjustResponseNumber(self, validFacts, validRules):
            responseNumber = 1
            if validFacts is True and validRules is False:
                responseNumber = 3
                #This means the ai should follow-up on finding new rules.
            elif validFacts is False and validRules is True:
                responseNumber = 4
                #This means the ai should follow-up on finding new facts.
            elif validFacts is True and validRules is True:
                responseNumber = 1
                #This means the ai has applied its logic and the user will be prompted to enter generic data.
            else:
                responseNumber = 2
                #This means no follow-up question is asked. The user will be prompted to enter generic data.

            return responseNumber

        def adjustResponseType(self, responseNumber, inferredFacts, newRules, validFacts, validRules):
            global responseType
            #The ai can only ask a question about one thing at a time. Rules are more important than facts as they greater empower the forward reasoning. As such, rules are prioritised over facts.
            responseString = ""

            if validRules is True:
                keysList = list(newRules.keys())
                precondition = keysList[0]
                postcondition = newRules.get(precondition)
                responseString = "relationship between {} and {}?".format(precondition, postcondition)
            
            elif validFacts is True:
                factUnit = inferredFacts[0] #the fact unit contains [fact, index of list in FB]
                responseString = factUnit[0]

            responseType = [responseNumber, responseString]

        def refireAI(self):
            #This function is the recursive system that allows the ai to continue running.
            global breakConversation
            if  breakConversation is False: #verify again that the user still wants the program to run.
                SymbolicAi()

FB = [["human"]] #This is the Facts Base. It contains facts about a person
RB = {"man":"human", "human":"mortal","apple":"fruit", "mortal":"will not live forever", "human and is mortal": "created", "not human or not mortal":"not created", "apple or fruit":"may like fruit salad", "neither apple nor fruit":"doesn't like fruit salad"}
#Above is the Rules Base. Inside I have set a rule stating that if X is a man then X is mortal.

negationBank = {"not human or not mortal":["not human", "not mortal"], "neither apple nor fruit":["not apple", "not fruit", "not pineapple", "not orange"]}
disjunctionBank = {"apple or fruit":["apple", "fruit", "pineapple","orange"]} #This dictionary allows multiple terms to have the same condition.
#The negationBank is used in negation
#The disjunctionBank is used in disjunction
responseType = [1,""] #The response type variable contains two variables, an integer, and a string. The integer is a number from 1 to 4 which is updated when output is generated by the symbolic ai. This variable is the used when asking questions to change which types of questions are asked. The string variable is the text which helps the ai determine what question to ask. If there is no question, it is an empty string "".
breakConversation = False

def main():
    prompt = "Here is my symbolic ai. It does reasoning and determines causality. \nYou can tell it about facts and relationships between things. \nWhen telling it about a causal relationship, make sure you only include one causal relationship per sentence."
    print(prompt)
    SymbolicAi()

if __name__ == '__main__':
    main()
    
#Tested (on both a modular and system level)
#1. implication
#2. inductive reasoning
#3. disjunction, conjunction, and dictionary-list functions and their corresponding functions to check if a new rule belongs in either the negation or disjunction bank
#4. adding new strings to the lists in the disjunction bank
#5. adding new rules to disjunction bank and negation bank
#6. algorithm to search through disjunction bank and negation bank and remove any duplicate values
#7. forward Chaining implementation.

#8. Chatbot ability to remove punctuation and capitalisation from text
#9. Chatbot ability to turn a string into a list of words
#10. Chatbot ability to remove components of speech from a list of words
#11. Create guard on implication and which prevents the FB from being filled with multiples of the same information.
#12. Chatbot ability to recognise feelings 
#13. Chatbot ability to generate emotional responses 

#14. Chatbot ability to separate user input into clauses based on punctuation. This helps determining causality based on causal words.
#15.Chatbot ability to discern causality from user input.
#16. Chatbot ability to formulate appropriate responses based on the responseType global variable.
#17. Turn conclusions into meaningful responses to be displayed to the user

#Still need to be tested
#1. 
#2. 
#3.

#Still need to be created

#3. Organise data and functions inside of classes

 



