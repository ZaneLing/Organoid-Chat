# 用Doc_QA2跑
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
from tempfile import NamedTemporaryFile
from langchain.llms import LlamaCpp
from langchain.embeddings import LlamaCppEmbeddings,HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.document_loaders import TextLoader, PyPDFLoader, PyMuPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document
from langchain_community.llms.ollama import Ollama
from langchain.chains import ConversationalRetrievalChain,conversational_retrieval
from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationBufferMemory
import json
import uuid
from langchain_core.output_parsers import StrOutputParser
import time
from langchain import hub
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
import os
from langchain_core.runnables import RunnableParallel

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

# ### llm and embedding model
llm_model = Ollama(model='llama3.1')
embedding_model = HuggingFaceEmbeddings(model_name='/home/ljc/czy/embedding_model/all-MiniLM-L6-v2',
                                            model_kwargs={'device': 'cuda:2'})
print('### {} Embedding model: HuggingFaceEmbedding(local_models-all-MiniLM-L6-v2)'.format(get_current_time()))
print('### {} QA LLM model: Ollama(model=llama3)'.format(get_current_time()))

# ### prompt construct
prompt = hub.pull("rlm/rag-prompt")
example_messages = prompt.invoke({"context": "filler context", "question": "filler question"}).to_messages()
print('### {} RAG prompt {}'.format(get_current_time(), example_messages[0].content))

def pdftoText(uploaded_file):
    docs = []
    for pdf in uploaded_file:
        pr = PyMuPDFLoader(pdf)
        for page in pr.pages:
            text = page.extract_text()
            doc = Document(page_content=text)
            doc.metadata["source"] = pdf.name
            docs.append(doc)
    return docs

def wrap_result(data):
    return JSONResponse(content={"response":data},status_code=200)

#global all_splits
all_splits = []
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CHROMA_PERSIST_DIR = "./chroma_db"
# if not os.path.exists(CHROMA_PERSIST_DIR):
#     os.makedirs(CHROMA_PERSIST_DIR)
#vectorstore = PersistentChroma(persist_directory=CHROMA_PERSIST_DIR)
# vectorstore = Chroma

@app.get("/")
async def index():
    """
    注册一个根路径
    :return:
    """
    return {"message": "Hello World"}

@app.route("/generate/id", methods=['POST'])
def generate_id():
    return wrap_result(str(uuid.uuid4()))

@app.post("/upload")
# async def upload_file(file: UploadFile = File(...)):
async def upload_file(
    username: str = Form(...), 
    conversationTitle: str = Form(...),
    files: List[UploadFile] = File(...)):
    
    print("### {} 到达upload".format(get_current_time()))

    print("### 保存的用户名是")
    print(username)
    print("### 保存的会话名是")
    print(conversationTitle)

    # Create the user-specific directory structure
    base_dir = f"tmpfile/{username}/{conversationTitle}"
    os.makedirs(base_dir, exist_ok=True)

    docs = []
    for file in files:
        save_path = f"{base_dir}/{file.filename}"
        with open(save_path, "wb") as f:
            while content := await file.read(1024):
                f.write(content)
        
        loader = PyPDFLoader(save_path)
        docs.extend(loader.load())


    # ### text splitting
    print('### {} text splitting start.'.format(get_current_time()))
    start_time = time.time()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
    # all_splits.extend(text_splitter.split_documents(docs))
    all_splits = text_splitter.split_documents(docs)
    end_time = time.time()
    print('### {} text split end, time-consuming {}'.format(get_current_time(), end_time - start_time))
    
    # ### indexing store
    print('### {} split text embedding start.'.format(get_current_time()))
    start_time = time.time()
    # vectorstore = Chroma.from_documents(documents=all_splits, embedding=embedding_model,persist_directory=CHROMA_PERSIST_DIR)
    # 如下改
    #Chroma.from_documents(documents=all_splits, embedding=embedding_model, persist_directory=CHROMA_PERSIST_DIR)
    db = FAISS.from_documents(all_splits,embedding_model)
     # FAISS index storage path for the user and conversation
    faiss_dir = f"faiss_index/{username}/{conversationTitle}"
    os.makedirs(faiss_dir, exist_ok=True)

    if len(os.listdir(faiss_dir)) == 0:
        db.save_local(faiss_dir)
    else:
        dc = FAISS.load_local(faiss_dir,embedding_model,allow_dangerous_deserialization=True)
        db.merge_from(dc) 
        db.save_local(faiss_dir)

    end_time = time.time()
    print('### {} split text embedding end, time-consuming {}'.format(get_current_time(), end_time - start_time))
    
    return JSONResponse(content={"response":"文件上传成功，可以开始提问了！"},status_code=200)

        

@app.post("/generate/")
async def generate_response(
    question: str = Form(...),  # 从FormData接收`question`
    username: str = Form(...),  # 从FormData接收`username`
    conversationTitle: str = Form(...)  # 从FormData接收`conversationTitle`
):
    print(f"### {get_current_time()} 问题来了: {question}")
    print(f"### 用户名: {username}, 对话标题: {conversationTitle}")

    if not question:
        return JSONResponse(status_code=400,content={"error":"Question not provided"})
   
    # ### retrieval and generation
    print('### {} retrieval and generation start.'.format(get_current_time()))
    start_time = time.time()

    faiss_index_path = f"faiss_index/{username}/{conversationTitle}/index.faiss"
    
    # 检查路径是否存在
    if not os.path.exists(faiss_index_path):
        return {"error": f"Index not found for {username} and {conversationTitle}"}
    
    # 加载FAISS索引
    vectorstore = FAISS.load_local(f"faiss_index/{username}/{conversationTitle}", embedding_model, allow_dangerous_deserialization=True)

    #vectorstore = Chroma(persist_directory="CHROMA_PERSIST_DIR", embedding_function=embedding_model)
    #vectorstore = FAISS.load_local("faiss_index",embedding_model,allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    # rag_chain = (
    #         {"context": retriever | format_docs, "question": RunnablePassthrough()}
    #         | prompt
    #         | llm_model
    #         | StrOutputParser()
    # )
    # answer = rag_chain.invoke(question)

    rag_chain_from_docs = (
            RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
            | prompt
            | llm_model
            | StrOutputParser()
    )
    rag_chain_with_source = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)

    result = rag_chain_with_source.invoke(question)
    answer = "回答：<br>"+str(result['answer'])+'<br>'+"来源：<br>"+str(result['context'])
    end_time = time.time()
    print('### {} retrieval and generation end, time-consuming {}'.format(get_current_time(), end_time - start_time))
    print('###',result)

    # return {"response":answer}
    return {"response":result}
    
@app.get("/filebase")
async def list_files():
    fold_path = "tmpfile"
    try:
        files = os.listdir(fold_path)
        file_list = [file for file in files if os.path.isfile(os.path.join(fold_path,file))]
        return JSONResponse(content={"response":file_list})
    except Exception as e:
        return JSONResponse(content={"error":str(e)},status_code=500)

