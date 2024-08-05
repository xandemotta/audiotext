import tkinter as tk
import speech_recognition as sr
import threading
import time
import requests

# Configurações
API_URL = 'http://localhost:5000'
TOKEN = None  # Token global

# Função para atualizar o status na interface gráfica
def update_status(message):
    status_label.config(text=message)
    root.update_idletasks()  # Atualiza a interface gráfica

# Função para fazer login e obter o token
def login(cliente_id, senha):
    global TOKEN
    try:
        response = requests.post(f'{API_URL}/login', json={
            'cliente_id': cliente_id,
            'senha': senha,
        })
        data = response.json()

        if data.get('acesso') == 'permitido':
            TOKEN = data.get('token')
            update_status('Login bem-sucedido! Token armazenado.')
        else:
            update_status('Login falhou. Verifique suas credenciais.')
    except Exception as e:
        update_status(f'Erro ao fazer login: {e}')

# Função de transcrição em tempo real
def real_time_transcription():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Pronto para capturar áudio. Fale agora!")
        
        buffer_text = ""
        silent_duration = 2.0  # Duração do silêncio para finalizar a transcrição
        last_audio_time = time.time()
        
        while True:
            try:
                update_status("Detectando áudio...")
                
                # Captura o áudio e considera a duração da frase
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                current_time = time.time()
                
                if current_time - last_audio_time > silent_duration:
                    update_status("Processando...")
                    
                    try:
                        # Transcreve o áudio
                        text = recognizer.recognize_google(audio, language='pt-BR')
                        buffer_text += text + ' '
                        
                        text_result.config(state=tk.NORMAL)
                        text_result.delete(1.0, tk.END)  # Limpa a área de texto
                        text_result.insert(tk.END, buffer_text)
                        text_result.config(state=tk.DISABLED)
                        text_result.yview(tk.END)
                        
                        last_audio_time = current_time
                    
                    except sr.UnknownValueError:
                        update_status("Não consegui entender o áudio.")
                    except sr.RequestError as e:
                        update_status(f"Erro de solicitação: {e}")
                        time.sleep(5)  # Pausa para evitar repetidos erros
                
                update_status("Aguardando áudio...")
            
            except sr.WaitTimeoutError:
                update_status("Aguardando áudio...")

# Função para iniciar a transcrição em tempo real
def start_real_time_transcription():
    if TOKEN is None:
        update_status("Você precisa fazer login primeiro.")
        return
    
    threading.Thread(target=real_time_transcription, daemon=True).start()

# Função para fazer login via interface gráfica
def login_action():
    cliente_id = entry_cliente_id.get()
    senha = entry_senha.get()
    login(cliente_id, senha)

# Configuração da interface gráfica
root = tk.Tk()
root.title("Transcrição de Áudio em Tempo Real")

# Layout da interface gráfica
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Campos de login
tk.Label(frame, text="Cliente ID:").pack(anchor=tk.W, pady=5)
entry_cliente_id = tk.Entry(frame)
entry_cliente_id.pack(anchor=tk.W, pady=5)

tk.Label(frame, text="Senha:").pack(anchor=tk.W, pady=5)
entry_senha = tk.Entry(frame, show='*')
entry_senha.pack(anchor=tk.W, pady=5)

button_login = tk.Button(frame, text="Login", command=login_action)
button_login.pack(anchor=tk.W, pady=5)

# Início da transcrição
button_start = tk.Button(frame, text="Iniciar Transcrição em Tempo Real", command=start_real_time_transcription)
button_start.pack(anchor=tk.W, pady=5)

# Exibição do resultado
text_result = tk.Text(frame, height=10, width=60, state=tk.DISABLED)
text_result.pack(anchor=tk.W, padx=5, pady=5)

# Status de captura de áudio
status_label = tk.Label(frame, text="Aguardando áudio...", font=("Arial", 12))
status_label.pack(anchor=tk.W, pady=5)

# Iniciar a interface gráfica
root.mainloop()
