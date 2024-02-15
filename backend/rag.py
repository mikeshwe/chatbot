import argparse
import xlsxwriter

from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter

from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.schema import Document
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import LLMChain

from langchain.chat_models import ChatOpenAI

from dotenv import load_dotenv, find_dotenv
import openai
import os
import json
import csv
import sys
from openai import OpenAI


BASE_MODEL = "gpt-3.5-turbo-1106"
FT_MODEL = "ft:gpt-3.5-turbo-1106:personal::8fCOiWsF"
TEMPERATURE = 0.5
EMBEDDINGS_MODEL = "text-embedding-ada-002"

# Load JSON file from local storage
def load_json_file(file_path):
    with open(file_path) as file:
        json_data = json.load(file)
    return json_data

def load_tsv_file(tsv_file_path):
    datalist = []
    with open(tsv_file_path,encoding='latin-1') as file:
        tsv_reader= csv.reader(file, delimiter="\t")
        for row in tsv_reader:
            if len(row) >= 2:
                key = row[0].strip()
                value = row[1].strip()
                data = {"title":key,"summary":value}
                datalist.append(data)
    return datalist    


# This class holds a document in a form that the Chroma database likes. Namely, there's page_content with the 
# actual payload you want to index in the database, and metadata--here, just a title
class My_Document:
  def __init__(self,summary, title):
    self.page_content = summary
    self.metadata = {"title":title}

# Extract summary and title fields from JSON, and load into documents for vector database
def extract_fields(data):
    documents = []
    for item in data:
        if "summary" in item and "title" in item:
            summary = item["summary"]
            title = item["title"]
            # print ('title: '+title+'\n'+'summary: '+summary+'\n')
            document = My_Document(summary, title)
            documents.append(document)
    #print ("number of documents: ", len(documents))
    return documents


# Load documents and embeddings into Chroma database
def load_into_chroma(documents, database_name):
    chroma = Chroma(database_name)
    embeddings = OpenAIEmbeddings(model=EMBEDDINGS_MODEL)

    # split it into chunks
    #text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0, separators=[" ", ",", "\n"])
    docs = text_splitter.split_documents(documents)

    db = chroma.from_documents(docs, embeddings,persist_directory="./chroma_db")
    return db




def show_similar_docs(db,query):
    similar_docs = find_similiar_docs(db,query,k=2,score=True)

    #print the top k results
    i = 0 
    for doc in similar_docs:
        print(i,": ",doc)
        i = i+1
    print()

# returns the k most-similar docs in the vector db to the query.
# For debugging purposes, this function can optionally return
# a score of how well the doc matched the query
def find_similiar_docs(db,query, k, score):
    if score:
        similar_docs = db.similarity_search_with_score(query, k=k)
    else:
        similar_docs = db.similarity_search(query, k=k)
    return similar_docs

# query the LLM reference by the QA chain, using the similar_docs as context
def get_answer(db,query,chain):
    similar_docs = find_similiar_docs(db,query, k=2, score=False)
    answer = chain.run(input_documents=similar_docs, question=query)
    return answer

# do a single Q&A interaction with the LLM, feeding it documents
# relevant to the query
def qa(db,query,model):
    llm = ChatOpenAI(model_name=model,temperature=TEMPERATURE)
    
    preamble = "You are a chatbot assistant for Stanford Federal Credit Union.  \
        You always answer in the first person singular (e.g., I, me, my ) or plural voice (e.g, we, our, us). \
        You don't answer in the third person (e.g., they, them, theirs). \
        You answer using a brand voice that makes your customers feel Appreciated, Respected, and Valued. \
        The brand voice should also demonstrate the credit union's value of community and adapting to a \
        customer's needs through their life time of events. \
        Your answer should inlcude as much information as you have so that you can answer the customer's \
        question as completely as possible. \
        Answer this question from a customer: "

    chain = load_qa_chain(llm, chain_type="stuff")
    answer = get_answer(db,preamble+query,chain)
    #print("custom answer: \n")
    return (answer)

def qa_base(query,model):
    llm = ChatOpenAI(model_name=model,temperature=TEMPERATURE)
    prompt = PromptTemplate(
        input_variables=["product"], # bit of a hack for a null prompt
        template=query+"{product}",
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    print(chain.run("")+"\n")



# rewrite the query n ways``
def qrewrite (query,model,n):
    queries = [query]
    llm = ChatOpenAI(model_name=model,temperature=TEMPERATURE)
    rephrase = "What are "+str(n) + " different ways to ask this question: "
    format = ". Return the results in JSON array like this: [question1, question2, question3]."
    prompt = PromptTemplate(
        input_variables=["product"], # bit of a hack for a null prompt
        template=rephrase + query + format + "{product}"
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    query_list = chain.run("")
    return json.loads(query_list) # convert json string to python list query_list

def create_db(file_path):
    data = load_tsv_file(file_path)
    documents = extract_fields(data)
    database_name = "my_database"  # Replace with your desired Chroma database name
    db = load_into_chroma(documents, database_name)
    return db

def run_rag(query,model):  
    db = Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings(model=EMBEDDINGS_MODEL))
    answer = qa(db,query,model)
    print (answer)


def parse_args():
    parser = argparse.ArgumentParser(description="RAG demo")
    
    parser.add_argument("--rag", action="store_true", help="Enable RAG (Retrieval-Augmented Generation)")
    parser.add_argument("--fine_tune", action="store_true", help="Enable fine-tuning")
    parser.add_argument("--query", type=str, help="Specify a query")

    args = parser.parse_args()
    
    global USE_RAG
    global QUERY 
    global FINE_TUNE

    if args.rag:
        USE_RAG = True
    else:
        USE_RAG = False

    if args.fine_tune:
        FINE_TUNE = True
    else:
        FINE_TUNE = False
 
    if args.query:
        QUERY = args.query
    else:
        print("No query specified.")


# in_filepath = tsv of prompts
def run_all_queries(in_filepath,out_filepath,model):
    workbook = xlsxwriter.Workbook(out_filepath)
    worksheet = workbook.add_worksheet()

    with open(in_filepath,encoding='latin-1') as infile:
        tsv_reader= csv.reader(infile, delimiter="\t")
        row_num = 0
        for row in tsv_reader:
            row_num = row_num + 1
            query = row[0].strip()
            db = Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings(model=EMBEDDINGS_MODEL))
            answer = qa(db,query,model=model)
            cell1 = "A"+str(row_num)
            cell2 = "B"+str(row_num)
            worksheet.write(cell1,query)
            worksheet.write(cell2,answer)
            print((query+" | "+answer+"\n"))

    workbook.close()

def run_query(query):
    
    if FINE_TUNE:
        model = FT_MODEL
    else:
        model = BASE_MODEL

    if USE_RAG:
        run_rag(query,model)
    else:
        qa_base(query,model)


# Main function
def main():
    _ = load_dotenv(find_dotenv()) # read the local .env file
    openai.api_key  = os.getenv('OPENAI_API_KEY')  
    parse_args()
    run_query(query=QUERY)
    #create_db(file_path = "docs/sfcu_faq2.tsv") # Run this once to persist the docs in Chroma
    #run_all_queries(in_filepath="docs/sfcu_faq2.tsv",out_filepath='docs/sfcu_tuned_results.xslx',model=FT_MODEL)
if __name__ == "__main__":
    main()






