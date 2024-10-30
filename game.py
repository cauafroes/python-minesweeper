import tkinter as tk
import random

class Embarcacao:
    def __init__(self, nome, tamanho):
        self.nome = nome
        self.tamanho = tamanho
        self.acertos = 0

    def esta_afundado(self):
        return self.acertos >= self.tamanho

class Tabuleiro:
    def __init__(self, tamanho=10):
        self.tamanho = tamanho
        self.grade = [[' ' for _ in range(tamanho)] for _ in range(tamanho)]
        self.embarcacoes = []

    def posicionar_embarcacao(self, embarcacao, x, y, horizontal):
        if horizontal:
            if y + embarcacao.tamanho > self.tamanho:
                return False
            for i in range(embarcacao.tamanho):
                if self.grade[x][y + i] != ' ':
                    return False
            for i in range(embarcacao.tamanho):
                self.grade[x][y + i] = embarcacao
        else:
            if x + embarcacao.tamanho > self.tamanho:
                return False
            for i in range(embarcacao.tamanho):
                if self.grade[x + i][y] != ' ':
                    return False
            for i in range(embarcacao.tamanho):
                self.grade[x + i][y] = embarcacao
        self.embarcacoes.append(embarcacao)
        return True

    def receber_ataque(self, x, y):
        celula = self.grade[x][y]

        if self.grade[x][y] == 'X' or self.grade[x][y] == 'O':
            return False

        if isinstance(celula, Embarcacao):
            celula.acertos += 1
            self.grade[x][y] = 'X'  # Marca como "atingido"
            return "Acertou!"
        else:
            self.grade[x][y] = 'O'  # Marca como "erro"
            return "Errou!"

class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.tabuleiro = Tabuleiro()
        self.frota = {
            "Submarino": 4,
            "Porta-aviões": 1,
            "Destroyer": 2,
        }

class JogoBatalhaNaval:
    def __init__(self):
        self.jogador1 = Jogador("Jogador 1")
        self.jogador2 = Jogador("Jogador 2")
        self.jogador_atual = self.jogador1
        self.oponente = self.jogador2
        self.jogo_iniciado = False
        self.tamanhos_embarcacao = {
            "Submarino": 1,
            "Porta-aviões": 4,
            "Destroyer": 3,
        }

        # Configurar janela Tkinter
        self.janela = tk.Tk()
        self.janela.title("Batalha Naval")

        # Mostrar status de configuração
        self.status_label = tk.Label(self.janela, text=f"{self.jogador_atual.nome}: Coloque suas embarcações", font=("Arial", 14))
        self.status_label.grid(row=0, column=0, columnspan=20)

        # Label de contagem de embarcações afundadas e flutuando
        self.contagem_j1_label = tk.Label(self.janela, text="Embarcações do Jogador 1", font=("Arial", 10), anchor="w", justify="left")
        self.contagem_j1_label.grid(row=13, column=0, columnspan=5, sticky="w")
        
        self.contagem_j2_label = tk.Label(self.janela, text="Embarcações do Jogador 2", font=("Arial", 10), anchor="e", justify="right")
        self.contagem_j2_label.grid(row=13, column=15, columnspan=5, sticky="e")
        
        self.atualizar_contagem_embarcacoes()

        # Criar tabuleiros de configuração para ambos os jogadores
        self.criar_tabuleiro(self.jogador1, 1)
        self.criar_tabuleiro(self.jogador2, 15)

        self.sair_button = tk.Button(self.janela, text="Sair", command=self.sair)
        self.sair_button.grid(row=12, column=3, columnspan=20)

        # Dropdown para escolher o tipo de embarcação
        self.tipo_embarcacao_var = tk.StringVar(self.janela)
        self.tipo_embarcacao_var.set("Submarino")
        self.menu_embarcacao = tk.OptionMenu(self.janela, self.tipo_embarcacao_var, *self.tamanhos_embarcacao.keys())
        self.menu_embarcacao.grid(row=11, column=5, columnspan=5)

        # Botão para definir a orientação da embarcação
        self.orientacao_var = tk.StringVar(self.janela)
        self.orientacao_var.set("Horizontal")
        self.menu_orientacao = tk.OptionMenu(self.janela, self.orientacao_var, "Horizontal", "Vertical")
        self.menu_orientacao.grid(row=11, column=10, columnspan=5)

        # Botão para começar ou reiniciar o jogo
        self.botao_iniciar = tk.Button(self.janela, text="Iniciar Jogo", command=self.iniciar_ou_reiniciar_jogo)
        self.botao_iniciar.grid(row=12, column=0, columnspan=20)

    def criar_tabuleiro(self, jogador, coluna_inicial):
        botoes_tabuleiro = [[None for _ in range(10)] for _ in range(10)]
        for x in range(10):
            for y in range(10):
                btn = tk.Button(self.janela, text=" ", width=2, height=1,
                                command=lambda x=x, y=y, p=jogador: self.posicionar_embarcacao_ou_atacar(p, x, y))
                btn.grid(row=x + 1, column=coluna_inicial + y)
                botoes_tabuleiro[x][y] = btn
        if jogador == self.jogador1:
            self.botoes_tabuleiro_j1 = botoes_tabuleiro
        else:
            self.botoes_tabuleiro_j2 = botoes_tabuleiro

    def posicionar_embarcacao_ou_atacar(self, jogador, x, y):
        if not self.jogo_iniciado:
            self.posicionar_embarcacao(jogador, x, y)
        else:
            if jogador == self.jogador_atual:
                self.atacar(self.oponente, x, y)

    def posicionar_embarcacao(self, jogador, x, y):
        tipo_embarcacao = self.tipo_embarcacao_var.get()
        if jogador.frota[tipo_embarcacao] <= 0:
            self.status_label.config(text=f"{jogador.nome}: Todas as embarcações de {tipo_embarcacao} já foram posicionadas!")
            return

        tamanho_embarcacao = self.tamanhos_embarcacao[tipo_embarcacao]
        horizontal = self.orientacao_var.get() == "Horizontal"
        embarcacao = Embarcacao(tipo_embarcacao, tamanho_embarcacao)

        if jogador.tabuleiro.posicionar_embarcacao(embarcacao, x, y, horizontal):
            jogador.frota[tipo_embarcacao] -= 1
            self.status_label.config(text=f"{jogador.nome}: {tipo_embarcacao} posicionado!")
            self.atualizar_contagem_embarcacoes()

            if all(contagem == 0 for contagem in self.jogador1.frota.values()) and all(contagem == 0 for contagem in self.jogador2.frota.values()):
                self.botao_iniciar.config(state="normal")
                self.status_label.config(text="Ambos os jogadores posicionaram suas embarcações. Pronto para começar!")
        else:
            self.status_label.config(text=f"{jogador.nome}: Posição inválida para o {tipo_embarcacao}")

    def iniciar_jogo(self):
        self.jogo_iniciado = True
        self.botao_iniciar.config(text="Iniciar Jogo")
        self.botao_iniciar.config(state="disabled")
        self.menu_embarcacao.config(state="disabled")
        self.menu_orientacao.config(state="disabled")
        self.jogador_atual = self.jogador1
        self.status_label.config(text=f"{self.jogador_atual.nome}: Ataque o tabuleiro do adversário")

    def atacar(self, oponente, x, y):
        resultado = oponente.tabuleiro.receber_ataque(x, y)

        if resultado == False:
            self.status_label.config(text=f"{self.jogador_atual.nome}: Posição inválida")
            return

        botoes_tabuleiro_oponente = self.botoes_tabuleiro_j2 if self.jogador_atual == self.jogador1 else self.botoes_tabuleiro_j1
        botoes_tabuleiro_oponente[x][y].config(text="X" if resultado == "Acertou!" else "O", bg="red" if resultado == "Acertou!" else "blue")

        if all(embarcacao.esta_afundado() for embarcacao in oponente.tabuleiro.embarcacoes):
            self.status_label.config(text=f"{self.jogador_atual.nome} venceu!")
            return

        self.status_label.config(text=f"{self.jogador_atual.nome}: {resultado}")
        self.jogador_atual, self.oponente = self.oponente, self.jogador_atual
        self.atualizar_contagem_embarcacoes()

    def atualizar_contagem_embarcacoes(self):
        contagem_j1_texto = "Embarcações de Jogador 1:\n"
        contagem_j2_texto = "Embarcações de Jogador 2:\n"

        # Count embarcacoes for Jogador 1
        embarcacoes_j1 = {}
        for emb in self.jogador1.tabuleiro.embarcacoes:
            if emb.nome not in embarcacoes_j1:
                embarcacoes_j1[emb.nome] = {'total': 0, 'afundados': 0}
            embarcacoes_j1[emb.nome]['total'] += 1
            if emb.esta_afundado():
                embarcacoes_j1[emb.nome]['afundados'] += 1

        # Count embarcacoes for Jogador 2
        embarcacoes_j2 = {}
        for emb in self.jogador2.tabuleiro.embarcacoes:
            if emb.nome not in embarcacoes_j2:
                embarcacoes_j2[emb.nome] = {'total': 0, 'afundados': 0}
            embarcacoes_j2[emb.nome]['total'] += 1
            if emb.esta_afundado():
                embarcacoes_j2[emb.nome]['afundados'] += 1

        # Update text for Jogador 1
        for tipo, contagem in embarcacoes_j1.items():
            flutuando = contagem['total'] - contagem['afundados']
            contagem_j1_texto += f"{tipo}: {flutuando} flutuando, {contagem['afundados']} afundados\n"

        # Update text for Jogador 2
        for tipo, contagem in embarcacoes_j2.items():
            flutuando = contagem['total'] - contagem['afundados']
            contagem_j2_texto += f"{tipo}: {flutuando} flutuando, {contagem['afundados']} afundados\n"

        # Configure labels
        self.contagem_j1_label.config(text=contagem_j1_texto)
        self.contagem_j2_label.config(text=contagem_j2_texto)

    def iniciar_ou_reiniciar_jogo(self):
        if not self.jogo_iniciado:
            self.iniciar_jogo()
        else:
            self.__init__()

    def sair(self):
        self.janela.destroy()

jogo = JogoBatalhaNaval()
jogo.janela.mainloop()
