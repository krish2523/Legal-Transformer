import os
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI
import streamlit as st
import base64
from dotenv import load_dotenv
load_dotenv()



class LegalDocumentCrew:
    def __init__(self, document_type, user_details, language="English"):
        load_dotenv()
        self.SERPER_API_KEY=os.getenv("SERPER_API_KEY")
        self.llm = ChatOpenAI(
            model="gpt-4.1-nano-2025-04-14",
            temperature=0.2, 
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.search_tool = SerperDevTool()
        self.document_type = document_type
        self.user_details = user_details
        self.language = language
    
    def research_agent(self):
        return Agent(
            role="Legal Researcher",
            goal=f"Quickly gather key legal requirements and format for {self.document_type}",
            backstory="Fast and efficient legal research specialist with expertise in Indian legal system",
            tools=[self.search_tool],
            llm=self.llm,
            verbose=False,
            max_iter=4
        )

    def drafting_agent(self):
        return Agent(
            role="Document Drafter",
            goal=f"Rapidly draft a {self.document_type} document with suitable format in {self.language}",
            backstory="Expert in quick, accurate legal drafting with knowledge of Indian law requirements and multilingual capabilities",
            tools=[self.search_tool],
            llm=self.llm,
            verbose=False,
            max_iter=5
        )

    def generate_document(self):
        # Research Task (minimized scope)
        research_task = Task(
            description=f"Quickly research essential legal requirements for {self.document_type} with format details either from the knoledgebase or websearch. Focus on key points, max 800 words. Keep the Legal Compliances aligned to India. Complete your research fully in one ot two session",
            agent=self.research_agent(),
            tools=[self.search_tool],
            expected_output="Expansive report based on requirements and your understanding of critical legal requirements"
        )

        # Drafting Task (optimized for speed)
        language_instruction = f"Create the document in {self.language} language."
        if self.language != "English":
            language_instruction += f" Make sure to translate all legal terms and content appropriately for {self.language} speakers while maintaining legal accuracy."
            
        drafting_task = Task(
            description=f"""Draft a {self.document_type} document with user details: {self.user_details}. {language_instruction}
            Use research findings. Incorporate the key legal requirements and format details for a {self.document_type} as identified by the research agent from web sources and from your knowledge.
            Ensure the document complies with Indian legal standards and complete the draft in one or two sessions.
            The document should be properly indented and formatted with consistent spacing throughout.""",
            agent=self.drafting_agent(),
            tools=[self.search_tool],
            expected_output=f"Complete, well-structured legal document in {self.language} with proper formatting and sections"
        )

        # Crew with optimized settings
        crew = Crew(
            agents=[self.research_agent(), self.drafting_agent()],
            tasks=[research_task, drafting_task],
            verbose=False,  # No logging for speed
            process="sequential"  # Explicitly sequential but faster with fewer steps
        )

        result = crew.kickoff()
        return result

def generate_legal_document(document_type, user_details, language="English"):
    try:
        crew = LegalDocumentCrew(document_type, user_details, language)
        document_text = crew.generate_document()
        return document_text.raw
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def download_legal_document(document_text, document_type):
    filename = f"{document_type.lower().replace(' ', '_')}.txt"
    b64 = base64.b64encode(document_text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download {document_type} Document</a>'
    st.markdown(href, unsafe_allow_html=True)