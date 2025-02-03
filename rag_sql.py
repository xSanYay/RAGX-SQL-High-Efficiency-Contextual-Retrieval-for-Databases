import sqlite3
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Remeber to set up Google Gemini API key
genai_api_key = os.getenv("GOOGLE_API_KEY")
if not genai_api_key:
    raise ValueError("Google API key not found in environment variables. Please set it.")

# Configure Google Gemini key from their developer platform
import google.generativeai as genai
genai.configure(api_key=genai_api_key)

# Function to retrieve all table names from the database
def get_all_tables(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    connection.close()
    return [table[0] for table in tables]

# Function to extract all data (row-wise retrieval by default)
def get_all_db_text(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    tables = get_all_tables(db_path)
    all_text = ""

    for table in tables:
        rows = cursor.execute(f"SELECT * FROM {table};").fetchall()
        for row in rows:
            row_text = " | ".join([str(value) for value in row])
            all_text += f"{table}: {row_text}\n"  

    connection.close()
    return all_text

# # Uncomment to enable column-wise retrieval (retrieves structured column info)
# def get_all_db_text(db_path):
#     connection = sqlite3.connect(db_path)
#     cursor = connection.cursor()
#     tables = get_all_tables(db_path)
#     all_text = ""

#     for table in tables:
#         columns = [column[1] for column in cursor.execute(f"PRAGMA table_info({table});").fetchall()]
#         rows = cursor.execute(f"SELECT * FROM {table};").fetchall()
#         for row in rows:
#             row_text = " | ".join([f"{columns[i]}: {row[i]}" for i in range(len(row))])
#             all_text += row_text + "\n"  

#     connection.close()
#     return all_text

# Function to split extracted data into chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return text_splitter.split_text(text)

# Function to create and save a FAISS vector store
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    print("Vector store saved locally as 'faiss_index'.")

# Function to create a conversational chain
def get_conversational_chain():
    prompt_template = """
    Context:\n{context}\n
    Question:\n{question}\n
    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    return load_qa_chain(model, chain_type="stuff", prompt=prompt)

# Function to process user queries
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = vector_store.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    print("\nReply: ", response["output_text"])

def main():
    db_file = "path/to/your/database.db"  # Update with your actual database path

    print("Processing SQL database...")
    raw_text = get_all_db_text(db_file)
    text_chunks = get_text_chunks(raw_text)
    get_vector_store(text_chunks)
    print("SQL database processed and vector store created.")

    while True:
        user_question = input("\nEnter your question (or type 'exit' to quit): ")
        if user_question.lower() == "exit":
            print("Exiting. Goodbye!")
            break
        user_input(user_question)

if __name__ == "__main__":
    main()
