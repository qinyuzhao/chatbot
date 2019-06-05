from bot import *



def test_nlp():
    
    assert preprocessing("This is a book.") == ['book']
    
    assert remove_stop_word(['python', 'is', 'interesting']) == ['python', 'interesting']
    
    assert tokenize("This is a book.") == ['This', 'is', 'a', 'book']
    
test_nlp()


chatbot = ChatBot("bot")

# The chat bot can answer python question
# He search the answer from Stack Overflow, so guarantee the network connection.
# You can ask him any python question and he can know that by the keyword 'python'.
chatbot.say(chatbot.answer_python_question("How can I save a file in python?"))

# Start a boot and enter 'quit' to stop it.
chatbot.chat()

# Let two bots chat 10 rounds.
two_bots(5)


def test_bot():
    
    assert chatbot.answer("How can I save a file in python?") != None
    
    assert chatbot.is_quit("quit") == True
    
    assert chatbot.is_question("What's this?") == True
    
    assert chatbot.is_question("Yes.") == False
    
    assert chatbot.is_python_question("How can I save a file in python?") == True
    
test_bot()