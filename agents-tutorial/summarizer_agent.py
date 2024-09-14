import wikipedia
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage



# Define the math tool for calculation
def math_tool(expression: str) -> str:
    try:
        result = eval(expression)
        return f"The result is: {result}"
    except Exception as e:
        return f"Error calculating expression: {e}"
    
def get_wikipedia_summary(query: str) -> str:
    try:
        # Fetch the summary of the given query from Wikipedia
        summary = wikipedia.summary(query, sentences=1)  # Adjust the number of sentences as needed
        return summary
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn't find a Wikipedia page for that query."
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Your query is ambiguous. Please be more specific. Options: {e.options}"
    except Exception as e:
        return f"An error occurred: {e}"
    

def langchain_agent():
    # Initialize the LLM with the specific model
    llm = Ollama(model="llama3.1", temperature=0.7)
    
    # Define tools manually instead of using `.bind_tools`
    tools = {
        "wikipedia": get_wikipedia_summary,
        "llm-math": math_tool
    }

    # Define the prompt template for the agent
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant capable of retrieving information and solving mathematical problems."),
            ("user", "{query}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ]
    )

    # Create the initial human query
    query = "What is the average age of a dog? Multiply the age by 3."
    human_message = HumanMessage(query)

    # LLM generates the initial response
    llm_response = llm.invoke(query)

    # Process the tool call based on the LLM response
    if "wikipedia" in query.lower():
        tool_output = tools["wikipedia"](query)
    elif "multiply" in query.lower():
        tool_output = tools["llm-math"]("7 * 3")  # Assuming age is 7 years as an example

    # Append tool output to the conversation and print the final result
    final_response = f"LLM Response: {llm_response}\nTool Output: {tool_output}"
    print(final_response)


if __name__ == "__main__":
    langchain_agent()