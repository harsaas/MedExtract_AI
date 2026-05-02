from langchain_openai import ChatOpenAI
from pydantic_models.clinical import PatientEncounter
from dotenv import load_dotenv

load_dotenv()
def extract_clinical_data(state):
    """
    Node to transform retrieved text into a structured Pydantic model.
    """
    # Initialize the LLM (GPT-4o is highly recommended for structured output)
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    # Bind the Pydantic model to the LLM
    structured_llm = llm.with_structured_output(PatientEncounter)
    
    # Process the context retrieved from Pinecone
    context = state.get("context", "")
    
    print("--- EXTRACTING STRUCTURED DATA ---")
    extracted_data = structured_llm.invoke(
        f"Extract clinical details from this patient encounter narrative: {context}"
    )
    
    # Return the dictionary version of the Pydantic model to the graph state
    return {"structured_data": extracted_data.model_dump()}