import wikipedia
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
import re



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
            ("user", "{query}")
        ]
    )

    # Create the initial human query
    query = "What is the average age of a football player? Multiply the age by 3."
    human_message = HumanMessage(query)


    # Use the prompt template to format the initial message
    formatted_prompt = prompt_template.format_prompt(query=human_message)

    # LLM generates the initial response
    llm_response = llm.invoke(formatted_prompt)

    # Decide which tool to use based on the LLM response
    if "average age" in query.lower():
        # Use the Wikipedia tool to get a summary related to the query
        summary = tools["wikipedia"](query)
        print(f"Wikipedia Summary: {summary}")
        
        # Extract the calculation part from the LLM response
        calculation = re.search(r'(\d+(\.\d+)?) \× \d+', llm_response)
        if calculation:
            equation = f"{calculation.group(1)} * 3"  # Build the calculation equation
            tool_output = tools["llm-math"](equation)
        else:
            tool_output = "No calculation found in LLM response."

        # Print the LLM response and tool output
        final_response = f"LLM Response: {llm_response}\nTool Output: {tool_output}"
    else:
        # If the query does not involve average age, use the LLM response directly
        final_response = f"LLM Response: {llm_response}"

    print(final_response)

if __name__ == "__main__":
    langchain_agent()