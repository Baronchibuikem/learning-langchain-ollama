from langchain_community.llms import Ollama
from pydantic import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser

# Define the SocialPost schema
class SocialPost(BaseModel):
    """Posts for social media"""
    tags: str = Field(description="Post tags")
    text: str = Field(description="Plain text of the post")

# Initialize Ollama with llama3.1 model
llm = Ollama(model="llama3.1")

# Set up a Pydantic output parser
parser = PydanticOutputParser(pydantic_object=SocialPost)

# Create a prompt template
PROMPT = """
Write a social media post about a {topic}.
{format_instructions}
"""

# Function to generate the post
def generate_social_post(topic: str):
    # Format the prompt with topic and instructions for structured output
    prompt = PROMPT.format(
        topic=topic,
        format_instructions=parser.get_format_instructions()
    )

    # Invoke the LLM with the formatted prompt
    response = llm.invoke(prompt)

    # Parse the response into a structured SocialPost object
    try:
        social_post = parser.parse(response)
        return social_post.model_dump_json(indent=2)  # Return as a JSON-formatted string
    except Exception as e:
        print(f"Error parsing the response: {e}")
        return None

# Generate the post
topic = "beach holiday"
response = generate_social_post(topic)

# Print the structured response
if response:
    print(response)
else:
    print("Failed to generate structured response.")
