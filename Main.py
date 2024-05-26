import json
from difflib import get_close_matches

def loadKnowledgeBase(filePath):
    with open(filePath, 'r') as f:
        data = json.load(f)
    return data

def saveKnowledgeBase(filePath, data):
    with open(filePath, 'w') as f:
        json.dump(data, f, indent=2)

def findBestMatch(userQuestion, questions):
    matches = get_close_matches(userQuestion, questions, n = 1, cutoff = 0.6)
    return matches[0] if matches else None

def getAnswers(questions, knowledgeBase):
    for q in knowledgeBase['questions']:
        if q['question'] == questions:
            return q['answer']

def chatBot():
    knowledgeBase = loadKnowledgeBase('knowledgeBase.json')

    while True:
        userInput = input("You: ")

        if userInput.lower() == "quit":
            break

        bestMatch = findBestMatch(userInput, [q["question"] for q in knowledgeBase['questions']])

        if bestMatch:
            answer = getAnswers(bestMatch, knowledgeBase)
            print(f'Bot: {answer}')

        else:
            print("Bot: I don't understand that. Can you explain?")
            newAnswer = input("Type the answer or type 'skip': ")

            if newAnswer.lower() != "skip":
                knowledgeBase['questions'].append({'question': userInput, 'answer': newAnswer})
                saveKnowledgeBase('knowledgeBase.json', knowledgeBase)
                print("Bot: Thank you I learned something new.")

if __name__ == '__main__':
    chatBot()