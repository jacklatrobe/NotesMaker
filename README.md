# NotesMaker
Note-taking is a critical skill that is essential in almost every aspect of life, from education and work to personal life. However, taking notes is not always an easy task, and it can be time-consuming, especially in large meetings, conferences, or presentations. Additionally, maintaining lengthy notes or transcripts of such events can be overwhelming, and it can be challenging to extract the key points, insights, and action items from such lengthy documents.

This is where NotesMaker comes into play. NotesMaker is a Python tool that can take VTT files and turn them into shorter, cleaner transcripts for GPT summarisation. The tool is designed to make note-taking and summarisation easier, faster, and more efficient. By using NoteMaker, users can extract the most critical information from lengthy transcripts, allowing them to focus on the key takeaways and actions.

One of the significant benefits of NoteMaker is that it can save users a significant amount of time and effort. Instead of manually going through lengthy transcripts to extract the key takeaways, users can simply use NoteMaker to get an accurate summary of the most important points. This feature is especially useful for busy professionals, students, or anyone who attends multiple meetings, conferences or presentations daily.

Another benefit of NoteMaker is that it can help users maintain more accurate and consistent notes. The tool ensures that the notes are summarised accurately, removing any room for human error or misinterpretation. Users can also save the summarised notes in the minutes directory, providing a record of the meeting or event for future reference. These minutes can be used to track progress, review action items, and provide a historical record of important events and decisions.

## Requirements

To run this program, the following dependencies are required:
- NTLK
- LangChain
- OpenAI
- Python

## File Structure

The following files are included in this project:
- `main.py` - the main program file
- `requirements.txt` - contains the necessary dependencies to run the program
- `transcripts/*.vtt` - upload Teams VTT transcripts here
- `minutes/*.txt` - program writes meeting minutes here

## Usage

The first time you run NoteTaker, you will need to uncomment the NTLK download line in main.py, then comment it out again once complete.

1. Clone the repository to your local machine.
2. Install the dependencies by running `pip install -r requirements.txt` in the terminal.
3. Add the VTT files to the `transcripts` directory.
4. Run `main.py` to generate the meeting minutes. The program will create a new text file in the `minutes` directory for each VTT file found in the `transcripts` directory. 

## License
Created by the Latrobe Consulting Grouper under an MIT license: https://opensource.org/license/mit/ 