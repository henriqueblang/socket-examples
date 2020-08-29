import random

# Classe que abstrai uma pergunta do teste
class Question:
    def __init__(self, text, answer, options):
        self.text = text
        self.answer = answer

        # Guardar todas as alternativas na lista choices
        self.choices = options
        self.choices.append(self.answer)

        # Embaralhar alternativas
        random.shuffle(self.choices)

    # Retorna texto da alternativa dada a letra
    def get_choice_by_letter(self, letter):
        # O índice na lista é calculado pela subtração do valor decimal
        # na tabela ASCII da letra por 97 ('a')
        index = ord(letter) - 97

        # Se o índice estiver fora dos limites, retorna string vazia
        if index < 0 or index >= len(self.choices):
            return ""

        return self.choices[index]

    # Retorna booleano que indica se a alternativa dada é igual a correta
    def is_choice_correct(self, choice):
        return choice == self.answer

    # Formatar pergunta para melhor visualização na impressão
    def format(self, mark=None):
        format_question = self.text + "\n"

        for i in range(len(self.choices)):
            letter = chr(i + 97)

            format_question += "\t" + letter + "."

            # A alternativa marcada é indicada por um 'x' dentro dos parênteses
            format_question += " (" + (mark is not None and (mark == letter and "x") or " ") + ") "

            format_question += self.choices[i]
            format_question += "\n"

        return format_question