import random
import socket

# Criar opções de conversa com o chatbot
CHATBOT = (
    {
        "text": "débito",
        "options": (
            {
                "text": "consumo mensal",
                "output": f"Seu consumo mensal é R${random.randint(100, 800)}."
            },
            {
                "text": "encerrar",
                "output": "Sua sessão foi finalizada."
            }
        )
    },
    {
        "text": "crédito",
        "options": (
            {
                "text": "consumo mensal",
                "output": f"Seu consumo mensal é R${random.randint(100, 800)}."
            },
            {
                "text": "valor da fatura",
                "output": f"Seu valor da fatura é R${random.randint(1000, 2000)}."
            },
            {
                "text": "encerrar",
                "output": "Sua sessão foi finalizada."
            }
        )
    }
)

print("Server running.")

# Guardar estrutura atual da conversa
conversation_structure = CHATBOT

# Flag para controlar loop
conversation_running = True

# Endereço no qual a conexão ocorrerá será rede local, porta 12345 (disponível)
address = ('127.0.0.1', 12345)

# Inicializar socket (TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associar socket com endereço
server_socket.bind(address)

# Configurar quantidade de clients que o server pode escutar simultaneamente
server_socket.listen(1)

# Aguardar client para iniciar conversa
conn, address = server_socket.accept()

# Laço de repetição enquanto conversa está ocorrendo
while conversation_running:
    print(f"Sending options to client...")

    # Construir string com as opções de conversa
    conversation_str = ""

    conversation_str += "Type:\n"

    # Iterar opções e concatenar na string
    for i in range(len(conversation_structure)):
        conversation_option = conversation_structure[i]

        conversation_str += str(i + 1) + " for " + conversation_option["text"] + "\n"

    # Enviar opções para o client
    conn.send(conversation_str.encode())

    # Receber resposta do client
    client_input = conn.recv(1024)

    client_input = client_input.decode()

    # Conferir se opção de conversa é um número
    try:
        client_input = int(client_input)
    except ValueError:
        continue

    # Conferir se opção de conversa está dentro dos limites
    if client_input < 1 or client_input > len(conversation_structure):
        continue

    # Obter estrutura da opção correspondente à entrada do usuário
    option = conversation_structure[client_input - 1]

    # Obter chave correspondente a estrutura do próximo estado de conversa
    next_conversation_state = "options" in option and "options" or "output"

    # Obter estrutura do próximo estado de conversa
    conversation_structure = option[next_conversation_state]

    # Se a estrutura for a string "output" (saída), implica em um estado final de conversa
    if next_conversation_state == "output":
        # Alterar flag para finalizar laço de repetição
        conversation_running = False

# Enviar mensagem para o client sinalizando que a conversa terminou
conn.send("finish".encode())

# Enviar para o client a mensagem, armazenada em conversation_structure
conn.send(conversation_structure.encode())

# Finalizar conexão
conn.close()