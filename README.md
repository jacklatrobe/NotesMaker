# NoteMaker
NoteMaker is a powerful tool designed to automate the process of creating meeting minutes from video call transcripts. Utilizing advanced natural language processing capabilities, NoteMaker reads in VTT (Web Video Text Tracks) files, cleans up the transcripts by removing filler words, and summarizes the content. These summaries are then written to text files, making it easy to capture the essence of meetings without manual effort.

## Features
- **Transcript Cleanup:** Removes common filler words and non-essential parts of speech to clean up the transcript.
- **Automatic Summarization:** Uses OpenAI's natural language processing to generate concise summaries of each transcript.
- **Minutes Generation:** Writes the summaries into neatly formatted minutes in text files for easy review and distribution.

## Getting Started

### Prerequisites
- Python 3.8 or later
- An Azure account with an OpenAI resource created
- `.env` file with necessary API keys and endpoints

### Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/jacklatrobe/NoteMaker.git
    cd NoteMaker
    ```

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up environment variables**
    Create a `.notesmaker.env` file in the root directory with the following content, replacing placeholders with your actual Azure OpenAI resource values:
    ```bash
    API_VERSION=<YOUR_API_VERSION>
    BASE_URL=<YOUR_BASE_URL>
    API_KEY=<YOUR_API_KEY>
    DEPLOYMENT_NAME=<DEPLOYMENT_NAME>
    CHUNK_SIZE=7500
    ```


### Usage

1. **Prepare your transcripts**
    Place your `.vtt` transcript files in the `./transcripts` directory.

2. **Run NoteMaker**
    Execute the main script to process the transcripts and generate minutes:
    ```bash
    python notemaker.py
    ```
    Processed minutes will be saved in the `./minutes` directory, with each summary corresponding to its source transcript file.

## Configuration
- `API_VERSION`, `BASE_URL`, `API_KEY`, `DEPLOYMENT_NAME`: Configure these variables in your `.notesmaker.env` file to match your Azure OpenAI setup.
- `CHUNK_SIZE`: Adjust the chunk size for processing large transcripts. The default is set to 7500 but can be modified based on the size of your transcripts and the desired level of detail in summaries - this will primarily be limited by the maximum token model available to you.
- A note on LLMs - this is built to use Azure OpenAI, but porting this to use another LLM via LangChain's wrapper should be quickly possible.

## License
Distributed under the MIT License. 

## Contact
Jack Latrobe - Latrobe Consulting Group
- jack@latrobe.group
- Project Link: [https://github.com/jacklatrobe/NoteMaker](https://github.com/jacklatrobe/NoteMaker)
