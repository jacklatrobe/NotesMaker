# NoteMaker - Main program file
# This file reads in VTT files from the transcripts directory, cleans up the transcripts,
# summarizes them using OpenAI, and writes the summaries to text files in the minutes directory.

# Imports - see requirements.txt
import os
from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import CharacterTextSplitter
import re
import uuid
import logging
from dotenv import load_dotenv


# Configuration variables - create .env
load_dotenv(".notesmaker.env")
API_VERSION = os.getenv("API_VERSION")
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))


# Define the directories
transcripts_dir = './transcripts'
minutes_dir = './minutes'

# Define common filler words
filler_words = [
    "umm", "um", "uhh", "uh", "hmm", "like", "so", "actually", "basically", "seriously",
    "literally", "anyway", "anyways", "kinda", "well", "yeah", "clearly", "indeed", "honestly", "frankly",
]

# Checks if a matching minutes exist for each transcript, and returns a list of tasks
def create_jobs_from_transcripts(transcripts_dir, minutes_dir):
    # Loop through all files in the directory
    jobs = []
    for filename in os.listdir(transcripts_dir):
        # Check if the file is a .vtt file
        if filename.endswith('.vtt'):
            # Create the full file path
            trans_filepath = os.path.join(transcripts_dir, filename)
            mins_filepath = os.path.join(minutes_dir, filename).replace(".vtt", ".txt")
            job_uuid = uuid.uuid4()

            # If a minutes already exists for this transcript, skip this one
            if os.path.isfile(mins_filepath):
                continue
            else:
                jobs.append({
                    "job_id" : job_uuid,
                    "transcript_filepath" : trans_filepath,
                    "minutes_filepath" : mins_filepath
                })
        return jobs
    
def create_transcript_from_vtt(transcript_path):
    transcript = []
    with open(transcript_path, 'r') as f:
            # Read the file line by line
            for line in f:
                # Define the regex pattern
                pattern = r'<v (.*?),(.*?)>'
                # Search for the pattern at the start of the line
                match = re.match(pattern, line)
                caption = re.sub(pattern, '', line)
                caption = caption.replace("</v>","")
                # If the pattern was found
                if match:
                    # Extract the last name and first name
                    last_name, first_name = match.groups()
                    # Split the line into tokens
                    words = caption.split(" ")
                    # remove all tokens that are not alphabetic
                    words = [word for word in words if word.isalpha()]
                    # strip out any filler words.
                    words = [word for word in words if word.lower() not in filler_words]
                    # Join the words back into a sentence
                    sentence = ' '.join(words)
                    if len(sentence) > 3:
                        transcript.append({
                            "first_name" : first_name,
                            "last_name" : last_name,
                            "message_text" : sentence
                        })
    return transcript

def summarise_chunk(llm, chunk):
    logging.info("Processing transcript chunk ({chars} lines)".format(chars=len(chunk)))
    # Define summary prompt
    prompt_template = """The following are lines from the transcript of a video call
    {chunk}
    Group lines by the same speaker or topic together, and produce a succinct bullet point summary of this part of the discussion.
    Bullet points:"""

    # Define chain for minutes summary
    prompt  = PromptTemplate.from_template(prompt_template)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    minutes_section = llm_chain.run(chunk=chunk)

    # Return the section to the minutes
    return minutes_section

def get_title(llm, text: str):
    # Define summary prompt
    prompt_template = """The following are lines from the transcript of a video call
    {text}
    Based on these lines, suggest a short title that accurately captures the content of the call.
    Helpful Answer:"""
    # Define LLM chain for title summary
    prompt  = PromptTemplate.from_template(prompt_template)
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # Only feed in the first chunk of the final transcript
    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=CHUNK_SIZE,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    texts = text_splitter.create_documents(text)

    title = llm_chain.run(text=str(texts[0].page_content))

    logging.info("Generated summary of minutes for title: {title}".format(title=title))
    return title

def format_minutes(llm, minutes, names):
    # Generate a title from the summarised minutes
    title = get_title(llm, minutes)

    # Format the final minutes doc
    minutes_doc = "Title: {title}\n\nAttendees:\n{names}\n\nMinutes:\n{minutes}".format(title=title, names=names, minutes=minutes)
    return minutes_doc

def write_minutes(minutes_path, text):
    logging.info("Writing minutes to {filepath}".format(filepath=minutes_path))
    try:
        with open(minutes_path, 'w') as f:
            f.write(text)
            f.close()
        return True
    except:
        raise "Error writing file"

# Loops through transcripts and produces clean meeting minutes
def main():
    # Define a logger
    logging.basicConfig(level=logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # Create LLM connection
    llm = AzureChatOpenAI(
        temperature=0.1,
        max_tokens=1000,
        openai_api_type="azure",
        api_key=API_KEY,
        api_version=API_VERSION,
        azure_endpoint=BASE_URL,
        azure_deployment=DEPLOYMENT_NAME)
    
    # Create jobs for each new transcript file
    jobs = create_jobs_from_transcripts(transcripts_dir, minutes_dir)
    job_count = len(jobs)
    logging.info("Got {job_count} transcripts to process to minutes - starting".format(job_count=job_count))

    # Process each file that needs to be summarised
    for job in jobs:
        logging.info("Processing transcript: {path}".format(path=job["transcript_filepath"]))
        transcript = create_transcript_from_vtt(job["transcript_filepath"])

        # Extract names from transcript
        names = []
        logging.info("Extracting names from transcript...")
        for line in transcript:
            names.append("{f} {l}".format(f=line["first_name"], l=line["last_name"]))
        names = set(names)
        logging.info("Extracted {name_count} names from the transcript".format(name_count=len(names)))
        names=" - " + "\n - ".join(list(names))

        # Now loop through the transcript
        minutes = []
        chunk = []
        for line in transcript:
            chunk.append(line)
            if len(str(chunk)) > CHUNK_SIZE:
                # Once a chunk is big enough, summarise it
                minutes_section = summarise_chunk(llm, chunk)

                # Append the section to the minutes
                minutes.append(minutes_section)

                # Clear the chunk now it's been summarised
                chunk = []
            
        # Gotta catch the last few lines incase there is a half chunk
        last_section = summarise_chunk(llm, chunk)
        minutes.append(last_section)
        minutes = "\n".join(minutes)

        # Format and write the minutes file
        minutes_doc = format_minutes(llm, minutes, names)
        write_minutes(job["minutes_filepath"], minutes_doc)
        

if __name__ == "__main__":
    main()