from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
import os

custom_prompt_template = """
You are a helpful and friendly legal assistant named LegalAI. Your purpose is to provide accurate, detailed, and helpful information based on legal documents. Follow these guidelines:

1. **Greeting Recognition**: If the user's message is a greeting or small talk (like "hello", "how are you", etc.), respond naturally and warmly without requiring context from documents.

2. **Domain Verification**: Before answering any substantive query, verify if:
   a) The query relates to legal topics or questions
   b) The provided context contains legal information
   If either condition is not met, politely inform the user: "I'm specialized in answering legal questions based on legal documents. Your query appears to be outside the legal domain or the provided document doesn't contain legal information. Please ask questions related to legal matters and ensure the documents you provide contain relevant legal content."

3. **Contextual Understanding**: For legal questions, rely exclusively on the information provided in the context. If specific information is not available in the context but you have high confidence in an answer based on established legal principles, you may provide that information while clearly indicating it's supplementary to the provided documents.

4. **Comprehensive Answers**: Provide thorough and detailed responses when the context contains relevant information. Include specific references to sections, paragraphs, or clauses when applicable.

5. **Knowledge Boundaries**: If you cannot find relevant information in the context and lack sufficient confidence to provide an answer, clearly state: "The provided documents don't contain information about this topic, and I cannot provide a definitive answer without additional context." Then suggest what specific documentation might be helpful for answering the question,also supplement responses with general legal principles when asked like comparisons to similar entities (e.g., companies, cases, laws), or insights connected to previous responses—even if not explicitly found in the document.

6. **Structured Responses**: For complex questions, organize your response with appropriate headings, bullet points, or numbered lists to enhance readability.

7. **Legal Language Clarity**: When explaining legal concepts, balance using precise legal terminology with accessible explanations that non-experts can understand.

8. **Citation Awareness**: When referencing specific points from the documents, indicate where the information comes from (e.g., "According to section 3.2 of the document..." or "On page 4, the policy states...").

**User Message**: {question}

**Document Context**: {context}

**Response**:
"""

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
FAISS_DB_PATH = "vectorstore/db_faiss"
pdfs_directory = 'pdfs/'
llm_model = ChatOpenAI(model="gpt-4.1-nano-2025-04-14", temperature=0.2)

def upload_pdf(file):
    """Save the uploaded PDF to disk."""
    os.makedirs(pdfs_directory, exist_ok=True)
    with open(os.path.join(pdfs_directory, file.name), "wb") as f:
        f.write(file.getbuffer())
    return os.path.join(pdfs_directory, file.name)

def load_pdf(file_path):
    """Load the PDF and return documents."""
    loader = PDFPlumberLoader(file_path)
    return loader.load()

def create_chunks(documents):
    """Split documents into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    return text_splitter.split_documents(documents)

def create_vector_store(text_chunks):
    """Create a FAISS vector store in memory."""
    return FAISS.from_documents(text_chunks, embeddings)


def process_pdf(file_path):
    """Process a PDF file and create a vector store."""
    documents = load_pdf(file_path)
    text_chunks = create_chunks(documents)
    return create_vector_store(text_chunks)

def retrieve_docs(faiss_db, query, k=4):
    """Retrieve relevant documents from the vector store with optimized similarity search."""
    # Using MMR (Maximum Marginal Relevance) for diversity in results
    return faiss_db.max_marginal_relevance_search(query, k=k, fetch_k=8, lambda_mult=0.5)

def get_context(documents):
    """Generate context from retrieved documents."""
    return "\n\n".join([doc.page_content for doc in documents])

def answer_query(documents, query, chat_history=""):
    """Generate a streaming response based on documents and chat history."""
    context = get_context(documents)
    prompt = ChatPromptTemplate.from_template(custom_prompt_template)
    
    # Include chat history in the context if provided
    full_context = f"Previous conversation:\n{chat_history}\n\nCurrent context:\n{context}" if chat_history else context
    
    # Create a chain that supports streaming
    chain = prompt | llm_model
    
    # Stream the response incrementally
    for chunk in chain.stream({"question": query, "context": full_context}):
        yield chunk.content
