from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate


def generate_pet_name(animal_type: str, pet_color: str):
    # Set up a parser + inject instructions into the prompt template.
    llm = Ollama(model="llama3.1", temperature=0.7)

    prompt_template_name = PromptTemplate(
        input_variables=['animal_type', 'pet_color'],
        template="I have a {animal_type} pet with color {pet_color} and I want a cool name for it. Suggest me five cool names for my pet."
    )

    name_chain = prompt_template_name | llm
    response = name_chain.invoke({'animal_type': animal_type, 'pet_color': pet_color})
    return response

