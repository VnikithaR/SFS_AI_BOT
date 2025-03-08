import random
import nltk

# Uncomment if you want to use NLTK's stopwords or other features
# nltk.download('punkt')
# nltk.download('stopwords')

# A simple set of pre-defined responses
responses = {
    "hello": ["Hi there!", "Hello!", "Greetings!", "Hey, how can I help you?"],
    "how are you": ["I'm doing great, thank you!", "I'm good, how about you?", "I'm just a bot, but I'm doing fine!"],
    "bye": ["Goodbye!", "See you later!", "Take care!"],
    "default": ["Sorry, I don't understand that.", "Can you please rephrase?", "I'm not sure how to respond to that."]
}

# Function to get a random response
def get_response(user_input):
    # Convert input to lowercase to make it case-insensitive
    user_input = user_input.lower()
    
    # Check if the input matches one of the pre-defined questions
    for key in responses:
        if key in user_input:
            return random.choice(responses[key])
    
    # Default response if no match is found
    return random.choice(responses["default"])

# Function to start the chatbot
def chatbot():
    print("Hello! I'm your AI chatbot. Type 'bye' to exit.")
    
    # Keep the conversation going until the user says 'bye'
    while True:
        user_input = input("You: ")
        
        # Check if the user wants to exit the conversation
        if user_input.lower() == "bye":
            print("Chatbot: " + random.choice(responses["bye"]))
            break
        
        # Get the response from the chatbot
        response = get_response(user_input)
        print("Chatbot: " + response)

# Run the chatbot
if __name__ == "__main__":
    chatbot()
