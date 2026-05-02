from langchain_openai import ChatOpenAI
from pydantic_models.eval import Metrics

def grade_extraction(state):
    """
    Node to evaluate the quality of the extraction using a 'Judge' LLM.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    # Bind the Metrics Pydantic model
    structured_grader = llm.with_structured_output(Metrics)
    
    context = state.get("context", "")
    extracted = state.get("structured_data", "")
    
    prompt = f"""
    You are a medical data auditor. Compare the raw clinical narrative with the extracted JSON data.
    
    RAW NARRATIVE:
    {context}
    
    EXTRACTED DATA:
    {extracted}
    
    Evaluate the extraction based on Accuracy (is the data correct?) and Faithfulness (is it grounded ONLY in the text?).
    Provide a score between 0.0 and 1.0 for each.
    """
    
    print("--- GRADING EXTRACTION QUALITY ---")
    grade_results = structured_grader.invoke(prompt)
    
    return {"metrics": grade_results.model_dump()}