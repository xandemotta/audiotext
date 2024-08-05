import tkinter as tk
import speech_recognition as sr
import threading
import time
from transformers import pipeline

# Configuração do modelo para restaurar pontuações
punctuation_model = pipeline("text2text-generation", model="your-model-id")  # Substitua pelo modelo adequado

def add_punctuation(text):
    # Adiciona pontuação ao texto
    return punctuation_model(text)[0]['generated_text']

def real_time_transcription():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Pronto para capturar áudio. Fale agora!")

        while True:
            try:
                # Captura o áudio com um tempo limite de 1 segundo para frase
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=1)
                
                # Transcreve o áudio
                text = recognizer.recognize_google(audio, language='pt-BR')
                
                # Adiciona pontuação ao texto
                text_with_punctuation = add_punctuation(text)
                
                # Atualiza a interface gráfica com o texto transcrito
                text_result.config(state=tk.NORMAL)
                text_result.insert(tk.END, text_with_punctuation + '\n')  # Adiciona o novo texto no final
                text_result.config(state=tk.DISABLED)
                text_result.yview(tk.END)  # Desloca a visualização para mostrar o texto mais recente
                
                # Pausa por 1 segundo para permitir processamento
                time.sleep(1)

            except sr.WaitTimeoutError:
                # Em caso de tempo de espera expirado, apenas continua esperando
                pass

            except sr.UnknownValueError:
                # Se o reconhecimento não conseguir entender o áudio, continua esperando
                print("Não consegui entender o áudio.")  # Para debug, pode ser removido

            except sr.RequestError as e:
                # Se houver problemas com a solicitação à API
                print(f"Erro de solicitação ao serviço de reconhecimento de fala: {e}")  # Para debug, pode ser removido

def start_real_time_transcription():
    threading.Thread(target=real_time_transcription, daemon=True).start()

# Configuração da interface gráfica
root = tk.Tk()
root.title("Transcrição de Áudio em Tempo Real")

# Layout da interface gráfica
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Início da transcrição
button_start = tk.Button(frame, text="Iniciar Transcrição em Tempo Real", command=start_real_time_transcription)
button_start.pack(anchor=tk.W, pady=5)

# Exibição do resultado
text_result = tk.Text(frame, height=10, width=60, state=tk.DISABLED)
text_result.pack(anchor=tk.W, padx=5, pady=5)

# Iniciar a interface gráfica
root.mainloop()
