import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()

# Define your desired data structure.
class Country(BaseModel):
    capital: str = Field(description="capital of the country")
    name: str = Field(description="name of the country")

PROMPT_COUNTRY_INFO = """
    Provide information about {country}.
    Please return the result in this JSON format:
    {{
        "capital": "The capital city",
        "name": "The country name"
    }}
    """


def main():
    # Set up a parser + inject instructions into the prompt template.
    parser = PydanticOutputParser(pydantic_object=Country)
    llm = Ollama(model="llama3.1")

    message = HumanMessagePromptTemplate.from_template(
        template=PROMPT_COUNTRY_INFO,
    )
    chat_prompt = ChatPromptTemplate.from_messages([message])

    # get user input
    country_name = input("Enter the name of a country: ")

    # generate the response
    print("Generating response...")
    # Format the prompt as a single string
    prompt = chat_prompt.format(
        country=country_name, format_instructions=parser.get_format_instructions()
    )

    # Pass the string prompt to the LLM
    output = llm.invoke(prompt)
    print(output)

    # Parse the output into the Country data structure
    country = parser.parse(output)
    print({"country": country})

    # print the response
    print(f"The capital of {country.name} is {country.capital}.")

if __name__ == '__main__':
    main()
