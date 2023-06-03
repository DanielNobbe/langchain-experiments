from langchain.document_loaders import TextLoader, NotebookLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms.openai import OpenAI
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.docstore.base import Docstore
import os


class DirectoryDocstore(Docstore):
    def __init__(self, directory: str, recursive=False):
        # Load all files in directory
        # Should we limit this to only doc files? Model should be able to deal with random files
        # Maybe limit to text files in any case
        self.files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if self.check_text_file(file_path):
                    self.files.append(file_path)
            if not recursive:
                # break after first list if we dont need to recurse deeper
                break
        self._build_search_index()

    @staticmethod
    def check_text_file(file_path):
        try:
            with open(file_path, "r") as f:
                for l in f:
                    continue
                return True
        except UnicodeDecodeError:
            return False # Fond non-text data

    def _build_search_index(self):
        # Builds index based on file names and titles of files in self.files
        for file_path in self.files:
            file_name = os.path.basename(file_path)
            print(file_name)
            # Extract first line, which is probably the title
            
            first_line = self.get_first_line(file_path)
            print(first_line)
        # now we need to make each of these a mutable object, like a 'Document', and make a dict
        # with both first line and file name pointing to the same object
        # Or we concatenate them and use a partial match, which will probably prevent duplicates overwriting
        # NOTE: We could use the relative path rather than the file name since it's more unique
        # NOTE: And then instruct the model that it can look for files directly using the relative path
        # --> Or should it just navigate through the folders? Let's try out

    @staticmethod
    def get_first_line(file_path):
        with open(file_path, "r") as f:
            for l in f:
                return l

    def search(self, search: str):
        # Search should search in some way through the:
        # title of doc file
        # doc file name
        # Maybe summary of doc, or some entity extraction
        pass


# llm = OpenAI(temperature=0, model_name='text-davinci-003')

# loader = TextLoader('/home/daniel/Documents/CentralDocuments/Projects/langchain/docs/index.rst')
# loader = NotebookLoader("/home/daniel/Documents/CentralDocuments/Projects/langchain/docs/modules/memory/getting_started.ipynb",
#                         include_outputs=True, max_output_length=20, remove_newline=True)

# index = VectorstoreIndexCreator().from_loaders([loader])


# query = "I want to add memory to my agent that I have a conversation with, in LangChain. How do I add this to my agent? Please provide a short code snippet."

# chain = RetrievalQA.from_chain_type(
#     llm, retriever=index.vectorstore.as_retriever()
# )
# print(chain.run(query))

# Use agent react-docstore --> Requires to put the docs in a docstore, which is possible
# This separates the resulting hits by a single blank line, but it might be better to separate it into double blank lines
# docstores are not very well documented, need to maybe make a new one

docs_path = '/home/daniel/Documents/CentralDocuments/Projects/langchain/docs/'
docstore = DirectoryDocstore(docs_path)