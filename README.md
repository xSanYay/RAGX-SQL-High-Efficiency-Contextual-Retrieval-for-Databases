# RAGX-SQL-High-Efficiency-Contextual-Retrieval-for-Databases
 
RAGX-SQL is an optimized **Retrieval-Augmented Generation (RAG)** framework designed to efficiently extract and process information from **SQL databases** using **Google Gemini AI**.  
It enables **contextual querying** over SQL databases, leveraging **column-wise retrieval** for enhanced accuracy, with an option for row-wise retrieval.  

---

## 🚀 Features  

- 🔹 **SQL-Based RAG** – Retrieves and processes structured data from SQL databases.  
- 🔹 **Google Gemini AI Integration** – Uses advanced embeddings and conversational AI.  
- 🔹 **FAISS Vector Store** – Efficiently stores and retrieves database content.  
- 🔹 **Optimized Column-Wise Retrieval** – Ensures meaningful query responses.  
- 🔹 *(Optional)* Row-wise retrieval available (commented in code).  

---

## 📦 Installation & Setup:

### 1️⃣ Clone the Repository & Navigate to It  
```bash
https://github.com/xSanYay/RAGX-SQL-High-Efficiency-Contextual-Retrieval-for-Databases.git
cd RAGX-SQL-High-Efficiency-Contextual-Retrieval-for-Databases
```

## 📦 Execution Steps:

### 1️⃣ Place Your SQLite Database  
Move your SQLite database (.db) file to the project directory.  
Update the database path in rag_sql.py inside the main() function.  

### 2️⃣ Run the RAG Pipeline  
python rag_sql.py  

### 3️⃣ Start Asking Questions!  
Once the database is processed, you can enter SQL-related questions in the terminal.  

Example queries:  
> What is the total revenue from orders in 2024?  
> List all employees who joined after 2020.  
> What are the top-selling products?  

## 📦 PROJECT STRUCTURE

📂 SQL-RAG   
 ├── 📄 rag_sql.py               # Main execution file  
 ├── 📄 requirements.txt         # Required dependencies  
 ├── 📄 .env                     # API key storage  
 ├── 📂 faiss_index/             # Vector store (auto-created)  
 ├── 📂 data/                    # SQLite database folder  
 ├── 📄 README.md                # Project documentation  



