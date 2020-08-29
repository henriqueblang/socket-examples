import socket

# Flag para controlar loop
conversation_running = True

# Endereço no qual a conexão ocorrerá será rede local, porta 12345 (disponível)
address = ('127.0.0.1', 12345)

# Inicializar socket (TCP)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Iniciar conexão com server
client_socket.connect(address)

# Laço de repetição enquanto conversa está ocorrendo
while conversation_running:
    # Esperar mensagem do server
    server_input = client_socket.recv(1024)
    server_input = server_input.decode()

    # Esta mensagem é recebida pelo client ao finalizar a conversa,
    # sinalizando para finalizar a conexão
    if server_input == "finish":
        conversation_running = False

        continue

    # Imprimir opções na tela
    print("\n" * 100)
    print(server_input)

    user_action = input()

    # Enviar resposta ao server
    client_socket.send(user_action.encode())

# Receber mensagem do estado final da conversa
server_input = client_socket.recv(1024)
server_input = server_input.decode()

# Imprimir resultados do teste
print("\n" * 100)
print(server_input)

# Finalizar a conexão
client_socket.close()