from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# Initialize summarization LLM with streaming enabled
summarize_llm = ChatOpenAI(model_name="gpt-4.1-nano-2025-04-14", temperature=0.3, streaming=True)

# Initialize the OpenAI client
client = OpenAI()

def transcribe_audio(audio_path):
    """Transcribe audio using OpenAI's Whisper small model."""
    with open(audio_path, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=file,  # Required audio file
            model="whisper-1",  # OpenAI's Whisper model
            response_format="text"  # Get raw text output
        )
        return transcription

def summarize_meeting(audio_path, target_language="English"):
    """Transcribes audio and streams a structured legal summary using LangChain in the specified language."""
    # Transcribe audio using Whisper model
    transcript = transcribe_audio(audio_path)  # transcript is a string
    transcript = transcript.strip()  # Remove leading/trailing whitespace
    
    if not transcript:
        raise ValueError("Transcription failed or returned an empty response.")

    # Legal-focused prompt for summarization with language support
    prompt = ChatPromptTemplate.from_template(
        """As a legal expert, analyze and summarize this meeting transcript:
        {transcript}
        
        Create a structured summary including:
        1. Key discussion points
        2. Important legal arguments
        3. Decisions made
        4. Action items with responsible parties
        5. Next steps
        6. Any critical deadlines
        
        Present in clear, professional language suitable for legal documentation.
        
        Provide the summary in {language} language."""
    )

    # LangChain Expression Language (LCEL) pipeline
    chain = prompt | summarize_llm | StrOutputParser()

    # Stream the summary chunks
    for chunk in chain.stream({"transcript": transcript, "language": target_language}):
        yield chunk