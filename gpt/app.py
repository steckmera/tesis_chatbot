from PyPDF2 import PdfReader
import os

##librerias de langchain
#langchain 
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# librerias para el textcontainer
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback

#libreria de response_container
from streamlit_chat import message

# configurar platnilla
from langchain import PromptTemplate

# importar streamlit
import streamlit as st

#configurar streamlit
st.set_page_config(page_title="cahtbot con PDF", layout="wide")
st.markdown("""<style>.block-container {padding-top: 1rem;}</style>""", unsafe_allow_html=True)

OPENAI_API_KEY="XXXXXXXXXXXXXXXXXXXX"
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

#creando las llaves para la session_state
session_state ={
    "responses":[],
    "requests":[]
}

if 'responses' not in st.session_state:
    st.session_state['responses'] = ["Hola, Bienvenidos al ChatbotUEMS \n\n Este es el menú:\n- Admisión\n- Administración\n- Sistemas"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []



### funcion para crear la base de caracteristicas o entremiento
def create_embeddings(pdf):
    #extraeyendo texto del pdf
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        #Dividiendo en trozos el texto extraido del pdf
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        embeddings = OpenAIEmbeddings()

        embeddings_pdf = FAISS.from_texts(chunks, embeddings)

        return embeddings_pdf


    
# cargar el documento en l sidebar
st.sidebar.markdown("<h1 style='text-align: center; color: #176B87;'>Cargar Archivo PDF</h1>", unsafe_allow_html=True)
st.sidebar.write("Carga el archivo .pdf con el cual quieres interactuar")
pdf_doc = st.sidebar.file_uploader("", type="pdf")
st.sidebar.write("---")
clear_button = st.sidebar.button("Limpiar Conversación", key="clear")

#create embeddings
embeddings_pdf=create_embeddings(pdf_doc)


# crear chat 
st.markdown("<h2 style='text-align: center; color: #176B87;text-decoration: underline;'><strong>ChatBot UEMS</strong></h2>", unsafe_allow_html=True)
st.write("---")
#contenedor del chat de historia
response_container = st.container()
#contenedor del texto box
textcontainer = st.container()

#prompt template

##template de respuesta
prompt_template = """Responda la pregunta con la mayor precisión posible, utilizando el contexto proporcionado. Si la respuesta
                    no está contenida, digamos "La pregunta ingresada no la reconozco, 'no tengo información de ello :('" \n\n
                    contexto: \n {context}?\n
                    pregunta: \n {question} \n
                    respuesta:
                    """
prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
)

#creando el campo para el ingreso de la pregunta dle susuario
with textcontainer:
    #formulario del text input
    with st.form(key='my_form', clear_on_submit=True):
        query = st.text_area("Tu:", key='input', height=100)
        submit_button = st.form_submit_button(label='Enviar')
    
    if query:
        with st.spinner("Escribiendo..."):
            #cosine similarity with API word Embeddings
            docs = embeddings_pdf.similarity_search(query)
            

            llm = OpenAI(model_name="gpt-3.5-turbo")
            chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)

            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=query)
                print(cb)
            
        st.session_state.requests.append(query)
        st.session_state.responses.append(response)

# configurando el campo de response_contanier
with response_container:
    if st.session_state['responses']:
        for i in range(len(st.session_state['responses'])):
            #respuesta de bot
            message(st.session_state['responses'][i],key=str(i), avatar_style="pixel-art")
            #pregunta de usuario
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')
            
