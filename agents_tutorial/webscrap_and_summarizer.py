import urllib.request
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import re
from langchain_community.llms import Ollama
from langchain_core.messages import HumanMessage, ToolMessage
import threading


# Tool function to get an article from the web
def get_article(url: str) -> str:
    """Retrieve an article from the web starting from the URL"""
    try:
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, features="html.parser")
        text = soup.get_text()
        return text
    except Exception as e:
        return f"Error fetching article: {e}"

# Function to extract URL from a prompt
def extract_url(prompt: str) -> str:
    """Extracts URL from the prompt string"""
    url_match = re.search(r'(https?://\S+)', prompt)
    if url_match:
        return url_match.group(0)
    return ''

# Lock for thread-safe operations
lock = threading.Lock()

# Manually handle tool calls and LLM invocations
def invoke_with_tools(prompt: str):
    tools = {"get_article": get_article}
    messages = [HumanMessage(content=prompt)]
    
    # Initialize the LLM
    llm = Ollama(model="llama3.1")
    
    # Invoke the LLM with the initial prompt
    ai_msg = llm.invoke(prompt)
    messages.append(ai_msg)
    
    # Extract URL from the prompt
    url = extract_url(prompt)
    
    if url:
        tool_name = "get_article"
        selected_tool = tools[tool_name]
        
        # Generate a dummy tool_call_id to use in ToolMessage
        tool_call_id = "tool_call_1"
        
        # Use a thread to fetch the article concurrently
        with ThreadPoolExecutor() as executor:
            future = executor.submit(selected_tool, url)
            tool_output = future.result()  # Wait for tool result
        
        # Ensure thread-safe access when modifying shared messages list
        with lock:
            messages.append(ToolMessage(content=tool_output, tool_call_id=tool_call_id))
        
        # Re-invoke the LLM with the tool's output
        final_prompt = f"Summarize the article content in a single row:\n{tool_output}"
        final_response = llm.invoke(final_prompt)
        
        with lock:
            messages.append(final_response)
        
        return final_response, messages
    
    else:
        return "No valid URL found in the prompt."

# Main function
def main():
    response, messages = invoke_with_tools("You can summarize in a single row the article https://docs.celeryq.dev/en/latest/django/first-steps-with-django.html ?")
    print({"response": response, "messages": messages})

if __name__ == "__main__":
    main()