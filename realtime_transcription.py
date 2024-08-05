from whisper_live.client import TranscriptionClient
import threading
from pynput import keyboard  # Importar a biblioteca correta
from langchain.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv, find_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv(find_dotenv())

# Inicializar o cliente de transcrição com IP e porta
client = TranscriptionClient(
    host="localhost",
    port=9091,
    lang="pt",
    translate=False,
    model_size="small"
)

# Função para iniciar a transcrição com o arquivo selecionado
def start_transcription():
    file_path = "caminho/do/seu/arquivo/audio"  # Substitua pelo caminho do seu arquivo
    if file_path:
        client(file_path)  # Ajuste conforme a documentação do cliente

# Iniciar o cliente de transcrição em uma thread separada
threading.Thread(target=start_transcription).start()

# Definir o template de prompt
template = """
    Você é um chatbot ajudando um humano com transcrições de áudio.
    Você receberá o texto do áudio e deve ajudar o usuário.
    Responda apenas em Português.

    Histórico do Chat: {chat_history}
    Última transcrição: {audio}
    Entrada: {input}
"""

base_prompt = PromptTemplate(
    input_variables=["input"], template=template
)

# Inicializar o modelo de linguagem
llm = ChatOllama(temperature=0, model="llama3:8b-instruct-q8_0")
# Alternativamente, você pode usar a API da Groq
# llm = ChatGroq(temperature=0, model="llama3-8b-8192")

memory = ConversationBufferMemory(memory_key="chat_history", input_key='input')
llm_chain = LLMChain(llm=llm, prompt=base_prompt, memory=memory)

# Definir o comportamento das teclas de atalho
transcript = ""
os.system("cls")  # Limpar o console para Windows. Use "clear" para sistemas Unix.

def on_press(key):
    global transcript
    
    try:
        # Parar a transcrição e salvar o texto
        if key == keyboard.Key.alt_l:
            client.client.close_websocket()  # Ajuste se necessário com base no método real
            transcript = "".join(client.client.text)  # Ajuste se necessário com base no atributo real
            os.system("cls")  # Limpar o console para Windows. Use "clear" para sistemas Unix.
            print(transcript)
            print("\n\n")  
          
        # Ativar o modo de conversa com o LLM
        if key == keyboard.Key.cmd:
            user_input = input("\nVocê: ")
            response = llm_chain.invoke({"input": user_input, "audio": transcript})["text"]
            print(f"\nIA: {response}")
    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def on_release(key):
    # Você pode adicionar funcionalidades adicionais no momento que uma tecla for liberada, se necessário.
    print(f'{key} liberado')

# Iniciar o listener de eventos de teclado
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
