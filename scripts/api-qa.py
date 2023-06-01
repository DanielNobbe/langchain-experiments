from langchain.document_loaders import TextLoader, NotebookLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.llms.openai import OpenAI
from langchain.chains.retrieval_qa.base import RetrievalQA


llm = OpenAI(temperature=0, model_name='text-davinci-003')

# loader = TextLoader('/home/daniel/Documents/CentralDocuments/Projects/langchain/docs/index.rst')
loader = NotebookLoader("/home/daniel/Documents/CentralDocuments/Projects/langchain/docs/modules/memory/getting_started.ipynb",
                        include_outputs=True, max_output_length=20, remove_newline=True)

index = VectorstoreIndexCreator().from_loaders([loader])


query = "I want to add memory to my agent that I have a conversation with, in LangChain. How do I add this to my agent? Please provide a short code snippet."

chain = RetrievalQA.from_chain_type(
    llm, retriever=index.vectorstore.as_retriever()
)
print(chain.run(query))
