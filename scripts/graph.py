#set the Langgraph to connect all the components together. This is the main entry point for the application.
from typing import TypedDict, Dict, Any
from langgraph.graph import START, StateGraph, END

# Import your nodes
from retriever import get_retriever
from pydantic_extractor import extract_clinical_data
from llm_grader import grade_extraction

# Define the State schema
class GraphState(TypedDict, total=False):
    query: str
    context: str
    structured_data: Dict[str, Any]
    metrics: Dict[str, Any]

#define langgraph nodes

def  retrieve_node(state: GraphState):
  retriever = get_retriever()
# Query Pinecone for the narrative summary
  docs = retriever.retrieve(state["query"])
  context = "\n\n".join([doc.get_content() for doc in docs])
  return {"context": context}

def extract_node(state: GraphState):
    # Uses ChatOpenAI + Pydantic (PatientEncounter)
    return extract_clinical_data(state)

def grade_node(state: GraphState):
    # Uses ChatOpenAI + Pydantic (Metrics)
    return grade_extraction(state)

#Buil the langraph using the nodes defined above
workflow = StateGraph(GraphState)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("extract", extract_node)
workflow.add_node("grade", grade_node)
workflow.add_edge(START, "retrieve")    
workflow.add_edge("retrieve", "extract")
workflow.add_edge("extract", "grade")
workflow.add_edge("grade", END)

#complie the graph
compiled_workflow = workflow.compile()



