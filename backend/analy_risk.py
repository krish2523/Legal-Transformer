from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
import pytesseract
from pdf2image import convert_from_path
import logging
from langdetect import detect, LangDetectException
from dotenv import load_dotenv


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LegalDocumentProcessor:
    def __init__(self):
        load_dotenv()
        self.llm = ChatOpenAI(
            temperature=0.2, 
            model="gpt-4.1-nano-2025-04-14",
        )
        
        # Supported languages with their codes
        self.supported_languages = {
            "en": "English",
            "zh": "Chinese",
            "es": "Spanish",
            "ar": "Arabic",
            "hi": "Hindi",
            "fr": "French",
            "pt": "Portuguese",
            "ru": "Russian",
            "ja": "Japanese",
            "de": "German",
            "bn": "Bengali"
        }
    def _extract_with_ocr(self, file_path):
        """Extract text from scanned PDFs using OCR"""
        logger.info("Performing OCR extraction")
        try:
            # Convert PDF to images
            images = convert_from_path(file_path)
            
            # Extract text from each image using OCR
            text_parts = []
            for i, image in enumerate(images):
                logger.info(f"Processing page {i+1}")
                text = pytesseract.image_to_string(image)
                text_parts.append(text)
            
            return " ".join(text_parts)
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            raise Exception(f"Could not extract text using OCR: {e}")    
    
    def extract_text_from_pdf(self, file_path):
        """Extract text from PDF using multiple methods based on PDF type"""
        logger.info(f"Extracting text from: {file_path}")
        
        try:
            # First try standard PDF extraction
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            text = " ".join([doc.page_content for doc in documents])
            
            # If the extracted text is too short, it might be a scanned document
            if len(text.strip()) < 100:
                logger.info("Standard extraction yielded little text, trying OCR...")
                text = self._extract_with_ocr(file_path)
            
            return text
        except Exception as e:
            logger.error(f"Error in standard extraction: {e}")
            # Fall back to OCR if standard extraction fails
            return self._extract_with_ocr(file_path)
    
    def detect_language(self, text):
        """Detect the language of the document text"""
        try:
            # Use a sample of the text for faster language detection
            sample = text[:1000]
            lang_code = detect(sample)
            
            # Return the language name if supported, otherwise return "English"
            if lang_code in self.supported_languages:
                return lang_code, self.supported_languages[lang_code]
            return "en", "English"
        except LangDetectException as e:
            logger.warning(f"Language detection failed: {e}. Defaulting to English.")
            return "en", "English"
    
    def analyze_document(self, file_path, target_language="en"):
        """Analyze legal document and identify key components"""
        try:
            text = self.extract_text_from_pdf(file_path)
            
            # Detect the language of the document
            source_lang_code, source_lang_name = self.detect_language(text)
            logger.info(f"Detected document language: {source_lang_name}")
            
            # Create analysis prompt with language instruction
            analysis_prompt = ChatPromptTemplate.from_template("""
            You are a specialized legal document analyzer with expertise in multiple languages. 
            Thoroughly analyze the following legal document which is in {source_language}:

            {document_text}

            Provide a detailed analysis that includes:
            1. Document type and purpose
            2. Key parties involved and their obligations
            3. Critical terms and conditions
            4. Important dates and deadlines
            5. Significant clauses and their implications
            6. Any unusual or non-standard provisions
            7. References to other documents or agreements

            Your response should be thorough yet concise, highlighting the most important aspects of the document.
            Please provide your analysis in {target_language}.
            """)
            
            # Get the target language name
            target_lang_name = self.supported_languages.get(target_language, "English")
            
            # Get the analysis from the LLM
            analysis_chain = analysis_prompt | self.llm
            analysis_result = analysis_chain.invoke({
                "document_text": text,
                "source_language": source_lang_name,
                "target_language": target_lang_name
            })
            
            return {
                "content": analysis_result.content,
                "source_language": source_lang_name,
                "source_language_code": source_lang_code
            }
            
        except Exception as e:
            logger.error(f"Document analysis failed: {e}")
            raise
    
    def assess_risks(self, file_path, analysis_result=None, target_language="en"):
        """Assess risks in the legal document"""
        try:
            # If analysis wasn't provided, get the document text
            if not analysis_result or isinstance(analysis_result, str):
                text = self.extract_text_from_pdf(file_path)
                source_lang_code, source_lang_name = self.detect_language(text)
                analysis_content = analysis_result if analysis_result else text
            else:
                # If analysis is provided as a dictionary with content
                text = analysis_result.get("content", "")
                source_lang_name = analysis_result.get("source_language", "English")
                source_lang_code = analysis_result.get("source_language_code", "en")
                analysis_content = text
                
            # Get the target language name
            target_lang_name = self.supported_languages.get(target_language, "English")
                
            # Create risk assessment prompt
            risk_prompt = ChatPromptTemplate.from_template("""
            You are a specialized legal risk assessor with expertise in multiple languages.
            Based on the following legal document analysis in {source_language}:

            {document_text}

            Provide a detailed risk assessment that includes:
            1. Key risk areas identified in the document
            2. Severity of each risk (Low, Medium, High, Critical)
            3. Potential consequences of each risk
            4. Recommended mitigations for each risk
            5. Compliance considerations and potential regulatory issues
            6. Any ambiguous language or clauses that could lead to disputes
            7. Overall risk level of the document

            Present your assessment in a clear, structured format that prioritizes the most significant risks.
            Please provide your assessment in {target_language}.
            """)
            
            # Get the risk assessment from the LLM
            risk_chain = risk_prompt | self.llm
            risk_assessment = risk_chain.invoke({
                "document_text": analysis_content,
                "source_language": source_lang_name,
                "target_language": target_lang_name
            })
            
            return {
                "content": risk_assessment.content,
                "source_language": source_lang_name,
                "source_language_code": source_lang_code
            }
            
        except Exception as e:
            logger.error(f"Risk assessment failed: {e}")
            raise

