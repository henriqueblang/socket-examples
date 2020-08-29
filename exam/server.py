import socket
import time

from question import Question

# Criar "folha de testes" (questões)
TEST_SHEET = (
    Question(
        text="Marque a alternativa que contém os protocolos presentes na camada de transporte do modelo de referência TCP/IP.",
        answer="TCP e UDP.",
        options=["FTP e SMTP.", "DNS e IP.", "TELNET e SMTP."]
    ),
    Question(
        text="No século XXI houve a criação de diversas redes sociais para diferentes públicos e finalidades. Sobre redes sociais para profissionais, assinale a alternativa correta.",
        answer="LinkedIn",
        options=["Facebook", "Orkut", "Twitter"]
    )
)

print("Server running.")

# Lista que armazena respostas da prova.
answers = [None] * len(TEST_SHEET)

# Flag para controlar loop
test_running = True

# Endereço no qual a conexão ocorrerá será rede local, porta 12345 (disponível)
address = ('127.0.0.1', 12345)

# Inicializar socket (TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associar socket com endereço
server_socket.bind(address)

# Configurar quantidade de clients que o server pode escutar simultaneamente
server_socket.listen(1)

# Aguardar client para iniciar prova
conn, address = server_socket.accept()

# Laço de repetição enquanto teste está ocorrendo
while test_running:
    print(f"Sending questions to client... [{sum(answer is not None for answer in answers)}/{len(answers)}] answered.")

    # Construir string com as perguntas do teste
    test_text = ""

    test_text += "Type <number letter> to answer a question. E.g.: 1 a\n"
    test_text += "Type <finish> to finish the test.\n"

    # Iterar perguntas do teste e concatenar na string
    for i in range(len(TEST_SHEET)):
        test_text += str(i + 1) + ") " + TEST_SHEET[i].format(answers[i]) + "\n"

    # Enviar perguntas para o client
    conn.send(test_text.encode())

    # Receber resposta do client
    client_input = conn.recv(1024)

    client_input = client_input.decode()

    # Se a mensagem for para encerrar o teste, alterar flag para finalizar
    # laço de repetição
    if client_input == "finish":
        test_running = False

        continue

    # Separar a string recebida do client por espaços
    client_answer = client_input.split()

    # Caso o client envie uma resposta que não siga o padrão proposto,
    # ignorar
    if len(client_answer) != 2:
        continue

    # Separar número da questão e alternativa escolhida
    question_number, question_letter = client_answer[0], client_answer[1]

    # Conferir se o número da questão recebido é realmente um número
    try:
        question_number = int(question_number)
    except ValueError:
        continue

    # Colocar alternativa escolhida em minúsculo
    question_letter = question_letter.lower()

    # Conferir se o número da questão e a alternativa escolhida estão dentro dos limites
    if question_number < 1 or question_number > len(TEST_SHEET) or not question_letter.isalpha():
        continue

    # Salvar resposta
    answers[question_number - 1] = question_letter

# Enviar mensagem para o client sinalizando que a prova terminou
conn.send("finish".encode())

# Construir string de resultados
result_text = ""
wrong_answers = []

print("\nCorrecting answers...")

# Iterar respostas do teste
for i in range(len(answers)):
    answer = answers[i]
    question = TEST_SHEET[i]

    # Se não houver resposta para a iésima questão, adicionar resposta
    # na lista de respostas incorretas
    if answer is None:
        wrong_answers.append(question)

        continue

    # Obter texto da alternativa escolhida
    choice = question.get_choice_by_letter(answer)

    # Se a resposta escolhida for diferente da correta, adicionar resposta
    # na lista de respostas incorretas
    if not question.is_choice_correct(choice):
        wrong_answers.append(question)

# Calcular número de respostas corretas
correct_answers_count = len(TEST_SHEET) - len(wrong_answers)

# Calcular nota final (0-100)
grade = round((correct_answers_count * 100) / len(TEST_SHEET))

print(f"[{correct_answers_count}/{len(TEST_SHEET)}] correct answers. Grade: {grade}.")

result_text += "Your final grade is: " + str(grade) + ".\n"

if grade == 100:
    result_text += " Congratulations!"
else:
    result_text += "Questions you answered incorrectly:\n"

    for question in wrong_answers:
        result_text += "\n" + question.text + "\n"
        result_text += "\t" + question.answer
        result_text += "\n"

# Enviar string de resultados para o client
conn.send(result_text.encode())

# Finalizar conexão
conn.close()