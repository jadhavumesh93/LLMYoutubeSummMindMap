# Retrieval-Augmented Knowledge Engine for YouTube Videos

[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/jadhavumesh93/LLMYoutubeSummMindMap)

This repository contains a Streamlit application that allows users to ask questions about a YouTube video. It leverages a Retrieval-Augmented Generation (RAG) pipeline to fetch the video's transcript, create vector embeddings, and generate accurate answers based on the video's content.

## Overview

The application provides a simple interface to input a YouTube video URL and a question. The backend processes the video, indexes its content, and uses Google's Gemini models to understand and answer the query. The system is designed to be persistent; once a video is processed, its knowledge is stored and can be queried again without re-processing, making subsequent queries faster.

## How It Works

The workflow is orchestrated by the `EntryPoint.py` script and is composed of several services:

1.  **Input**: The user provides a YouTube URL and a question through the Streamlit UI (`app.py`).
2.  **Transcript Fetching**: `YoutubeService` validates the URL, extracts the video ID, and retrieves the full transcript using the `youtube-transcript-api`.
3.  **Indexing & Embedding**:
    *   `LLMEmbeddings` checks if the video has already been indexed in the local Chroma vector database (`yt_db/`).
    *   If the video is new, the service takes the transcript, splits it into manageable chunks using `RecursiveCharacterTextSplitter`, and generates vector embeddings for each chunk with Google's `gemini-embedding-001` model.
    *   These embeddings are then stored persistently in the ChromaDB.
4.  **Retrieval & Generation**:
    *   `RAGService` takes the user's question.
    *   It retrieves the most relevant text chunks from ChromaDB based on semantic similarity to the question.
    *   The retrieved context and the original question are passed to a `ChatGoogleGenerativeAI` model (`gemini-2.5-flash-lite`) using a carefully crafted LangChain prompt.
    *   The prompt instructs the model to answer *only* based on the provided context, ensuring the responses are grounded in the video's content.
5.  **Output**: The final generated answer is displayed to the user in the Streamlit interface.

## Tech Stack

*   **Frontend**: Streamlit
*   **Backend**: Python
*   **LLM & Embeddings**: Google Gemini via `langchain-google-genai`
*   **RAG Framework**: LangChain
*   **Vector Store**: ChromaDB
*   **YouTube Interaction**: `youtube_transcript_api`

## Project Structure

```
.
├── app.py                  # Main Streamlit application UI
├── EntryPoint.py           # Orchestrates the entire RAG pipeline
├── requirements.txt        # Python dependencies
├── runtime.txt             # Python version for deployment
├── Services/
│   ├── LLMEmbeddings.py    # Handles embedding, chunking, and ChromaDB storage
│   ├── RAGService.py       # Manages the RAG chain for question-answering
│   └── YoutubeService.py   # Fetches video transcripts and metadata
└── YoutubeUtility/
    └── YoutubeUtility.py   # Helper functions and error codes
```

## Setup and Local Usage

### Prerequisites

*   Python 3.11
*   Git

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/jadhavumesh93/LLMYoutubeSummMindMap.git
    cd LLMYoutubeSummMindMap
    ```

2.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

### Configuration

1.  Create a file named `.env` in the root directory of the project.
2.  Add your Google API key to the `.env` file. You can obtain a key from [Google AI Studio](https://aistudio.google.com/app/apikey).
    ```
    GOOGLE_API_KEY="YOUR_GOOGLE_AI_API_KEY"
    ```

### Running the Application

1.  **Start the Streamlit app:**
    ```sh
    streamlit run app.py
    ```
2.  Open your web browser and navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).
3.  Enter a valid YouTube video URL, type your question, and click "Submit" to get a response.