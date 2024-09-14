from langchain_community.llms import Ollama
from langchain.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory

# Initialize the Ollama LLM with model "llama3.1"
llm = Ollama(model="llama3.1")

# Define the chat prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an assistant who helps users plan trips."),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Chain the prompt with the LLM
chain = prompt | llm

# Initialize the chat message history
history = ChatMessageHistory()

# Main loop for user input and responses
while True:
    message = input("User: ")
    if message.lower() == "exit":
        break
    # Add user's message to history
    history.add_user_message(message)
    
    # Generate response using the chain
    response = chain.invoke({"messages": history.messages})
    
    # Add AI's message to history
    history.add_ai_message(response)
    
    # Print the AI's response
    print("AI: " + response)
