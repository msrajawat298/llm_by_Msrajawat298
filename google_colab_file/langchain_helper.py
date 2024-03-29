# -*- coding: utf-8 -*-
"""Copy of 8cf82b9c9fecb7a485c673dd1d3ddf68

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eKKfE8X0jFMTO7NdhjaJMCnZ04YZowQZ

### Basic working of Google Palm LLM in LangChain
"""

#Install Dependencies
!pip install langchain==0.0.284 python-dotenv==1.0.0 streamlit==1.22.0 tiktoken==0.4.0 faiss-cpu==1.7.4 protobuf~=3.19.0 google-generativeai InstructorEmbedding sentence-transformers

from langchain.vectorstores import FAISS
from langchain.llms import GooglePalm
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
import logging

# Set the logging level to ignore warnings from the sentence_transformers module
logging.getLogger('sentence_transformers').setLevel(logging.ERROR)

api_key = 'Enter you api Key' # get this free api key from https://makersuite.google.com/
llm = GooglePalm(google_api_key=api_key, temperature=0.1)

"""### Now let's load data from aboutme csv file"""

# Specify the encoding as 'latin-1'
file_encoding = 'latin-1'
loader = CSVLoader(file_path='/content/aboutme.csv', source_column="prompt", encoding=file_encoding)
# Store the loaded data in the 'data' variable
data = loader.load()

"""### Hugging Face Embeddings"""

# Initialize instructor embeddings using the Hugging Face model
instructor_embeddings = HuggingFaceInstructEmbeddings(model_name="deepset/roberta-large-squad2")

"""### Vector store using FAISS"""

vectordb_file_path = '/content/faiss_index'
# Create a FAISS instance for vector database from 'data'
vectordb = FAISS.from_documents(documents=data, embedding=instructor_embeddings)
# Save vector database locally
vectordb.save_local(vectordb_file_path)

# Load the vector database from the local folder
vectordb = FAISS.load_local(vectordb_file_path, instructor_embeddings)

# Create a retriever for querying the vector database
retriever = vectordb.as_retriever(score_threshold=0.7)
rdocs = retriever.get_relevant_documents("how about job placement support?")
rdocs

"""As you can see above, the retriever that was created using FAISS and hugging face embedding is now capable of pulling relavant documents from our original CSV file knowledge store. This is very powerful and it will help us further in our project

##### Embeddings can be created using GooglePalm too. Also for vector database you can use chromadb as well as shown below. During our experimentation, we found hugging face embeddings and FAISS to be more appropriate for our use case

### Create RetrievalQA chain along with prompt template 🚀
"""

prompt_template = """Given the following context and a question, generate an answer based on this context only.
In the result only return response.
In the answer try to provide as much text as possible from "response" section in the source document context without making much changes.
If the answer is not found in the context, kindly state "I don't know. you can email your query to my team on email msrajawat298@gmail.com " Don't try to make up an answer.

CONTEXT: {context}

QUESTION: {question}"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

chain = RetrievalQA.from_chain_type(llm=llm,
                                    chain_type="stuff",
                                    retriever=retriever,
                                    input_key="query",
                                    return_source_documents=True,
                                    chain_type_kwargs={"prompt": PROMPT})

"""### We are all set 👍🏼 Let's ask some questions now"""

chain('Who is Mayank Singh Kushwah?')