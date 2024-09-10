# from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
# from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import openai 
from dotenv import load_dotenv
import os
import shutil
import nltk
import ssl
from pathlib import Path

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context    
nltk.download()
# Load environment variables from APIKEY.env
load_dotenv(Path(".env"))

# Set OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key is None:
    raise ValueError("OpenAI API key not found. Make sure it's set in APIKEY.env.")

openai.api_key = openai_api_key

# Define paths and settings
CHROMA_PATH = "chroma"
DATA_PATH = "data/books"
URLS = [
    "https://science.nasa.gov/mission/mars-exploration-rovers-spirit-and-opportunity/",  # Add actual URLs here
    "https://example.com/article2"
]
verify = False

def main():
    generate_data_store()

def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)

def load_documents():
    # Load documents from local directory
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    local_documents = loader.load()
    
    # Load documents from URLs
    url_loader = UnstructuredURLLoader(urls=URLS)
    url_documents = url_loader.load()

    # Combine both local and URL documents
    documents = local_documents + url_documents
    return documents

def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    document = chunks[10]
    print(document.page_content)
    print(document.metadata)

    return chunks

def save_to_chroma(chunks: list[Document]):
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, OpenAIEmbeddings(), persist_directory=CHROMA_PATH
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

if __name__ == "__main__":
    main()
