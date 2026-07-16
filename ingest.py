"""
ingest.py

Loads PDF documents
Splits them into chunks
Creates embeddings
Stores them in FAISS
"""

import os

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from config import (
    DATA_FOLDER,
    VECTOR_DB,
    CHUNK_SIZE,
    CHUNK_OVERLAP
)

from services.embedding_service import EmbeddingService

from utils.logger import logger
from utils.helper import ensure_directory


def load_documents():

    logger.info("Loading PDF documents...")

    loader = PyPDFDirectoryLoader(DATA_FOLDER)

    documents = loader.load()

    logger.info(f"Loaded {len(documents)} pages.")

    return documents


def split_documents(documents):

    logger.info("Splitting documents into chunks...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(documents)

    logger.info(f"Created {len(chunks)} chunks.")

    return chunks


def create_vector_database(chunks):

    logger.info("Creating embeddings...")

    embeddings = EmbeddingService().get_embeddings()

    db = FAISS.from_documents(
        chunks,
        embeddings
    )

    ensure_directory(VECTOR_DB)

    db.save_local(VECTOR_DB)

    logger.info("Vector database created successfully.")


def main():

    try:

        documents = load_documents()

        if len(documents) == 0:

            logger.warning("No PDF files found.")

            print("No PDF files found inside data folder.")

            return

        chunks = split_documents(documents)

        create_vector_database(chunks)

        print("\nVector Database Created Successfully!")

    except Exception as e:

        logger.exception(e)

        print(e)


if __name__ == "__main__":

    main()