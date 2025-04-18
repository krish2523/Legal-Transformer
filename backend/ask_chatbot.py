from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv

# Section 1: LLM Setup
def initialize_llm():
    load_dotenv()
    return ChatOpenAI(
        model_name="gpt-4.1-nano-2025-04-14",
        temperature=0.3,
        streaming=True
    )

# Section 2: Memory Setup
def initialize_memory(window_size=5):
    return ConversationBufferWindowMemory(k=window_size, return_messages=True)

# Section 3: Prompt Setup
def create_legal_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", """You are a legal assistant specialized in legal cases. Your role is to provide accurate and concise information related to legal cases, statutes, precedents, and procedures based on the user's input. 

        When responding:
        1. First determine if the query is legal-related (even loosely)
        2. For legal queries, provide helpful information
        3. For borderline cases, try to relate it to legal concepts
        4. Only for completely unrelated queries (like cooking, sports, etc.) respond with the disclaimer"""),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

# Section 4: Create Runnable Chain
def create_runnable_chain():
    llm = initialize_llm()
    memory = initialize_memory(window_size=5)
    prompt = create_legal_prompt()
    
    # Define the chain
    chain = (
        {"history": lambda x: memory.load_memory_variables({})["history"], 
         "input": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    # Create a function that also updates memory
    def chain_with_memory(user_input):
        response = chain.invoke(user_input)
        memory.save_context({"input": user_input}, {"output": response})
        return response
    
    return chain_with_memory

# Section 5: Main Chatbot Interface
legal_chain = create_runnable_chain()

def get_legal_response(user_input):
    response = legal_chain(user_input)
    for chunk in response:
        yield chunk