import json
from difflib import get_close_matches
import wikipedia

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
def search(keyword):
    searchResult = wikipedia.search(keyword)[0]
    return wikipedia.page(searchResult).summary
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
            print("Bot: I don't understand that. Do you want me to search Wikipedia, or do you want to teach me? "
                  "Otherwise type 'skip'")
            choice = input("Your choice: ").lower()
            if choice == 'skip':
                continue
            elif "wikipedia" in choice:
                keyword = input("What keyword would you like to search: ")
                print(search(keyword))

            else:
                newAnswer = input("Type the answer to your question: ")
                knowledgeBase['questions'].append({'question': userInput, 'answer': newAnswer})
                saveKnowledgeBase('knowledgeBase.json', knowledgeBase)
                print("Bot: Thank you I learned something new.")

if __name__ == '__main__':
    chatBot()