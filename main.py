"""
Projeto 2 - Gerenciador de Tarefas Automático com IA
Estrutura de Dados: Lista Encadeada Ordenada (Construída)
Linguagem: Python 3
Integração IA: Ollama Modelo llama3
"""
import json
from datetime import datetime
import ollama


class NoTarefa:
    """
    Nó individual da lista encadeada.
    """
    def __init__(self, titulo: str, prazo: str):
        self.titulo = titulo
        self.prazo = prazo  # Formato YYYY-MM-DD
        self.proximo = None  # Ponteiro para o próximo Nó


class ListaEncadeadaTarefa:
    def __init__(self):
        self.cabeca = None 
    
    def insert_ordered(self, titulo: str, prazo: str) -> None:
        novo_no = NoTarefa(titulo, prazo)

        # Caso 1: Lista vazia ou novo nó deve ser a nova cabeça
        if self.cabeca is None or novo_no.prazo < self.cabeca.prazo:
            novo_no.proximo = self.cabeca
            self.cabeca = novo_no
            return

        # Caso 2: Percorre a lista até a posição correta
        atual = self.cabeca
        while atual.proximo is not None and atual.proximo.prazo <= novo_no.prazo:
            atual = atual.proximo
        
        # Conecta os ponteiros fora do laço
        novo_no.proximo = atual.proximo
        atual.proximo = novo_no

    def pop_inicio(self) -> NoTarefa:
        if self.cabeca is None:
            return None
        
        no_removido = self.cabeca
        self.cabeca = self.cabeca.proximo
        no_removido.proximo = None
        return no_removido

    def esta_vazia(self) -> bool:
        return self.cabeca is None

    def exibir_tarefas(self) -> None:
        if self.esta_vazia():
            print("\n--------------------------------------------")
            print("   Nenhuma tarefa cadastrada na lista.")
            print("--------------------------------------------\n")
            return
        
        print("\n===========================================")
        print("     Minhas tarefas (Ordenação por prazo)    ")
        print("=============================================")
        atual = self.cabeca
        posicao = 1
        while atual is not None:
            print(f"{posicao}. [Prazo: {atual.prazo}] -> {atual.titulo}")
            atual = atual.proximo
            posicao += 1
        print("============================================\n")


# ----------------------------------------------------------------------
# INTEGRAÇÃO COM A INTELIGÊNCIA ARTIFICIAL (OLLAMA)
# ----------------------------------------------------------------------

def extrair_tarefa_ia(texto_usuario: str, modelo: str = "llama3") -> dict:
    """
    Envia a frase digitada pelo usuário para o Ollama e força um retorno em JSON estruturado.
    """
    # Obtém a data de hoje e o dia da semana em português
    dias_semana = {
        0: "segunda-feira", 1: "terça-feira", 2: "quarta-feira",
        3: "quinta-feira", 4: "sexta-feira", 5: "sábado", 6: "domingo"
    }
    hoje = datetime.now()
    data_hoje = hoje.strftime("%Y-%m-%d")
    dia_nome = dias_semana[hoje.weekday()]

    prompt = f"""
    Você é um assistente de extração de tarefas.
    Hoje é {dia_nome}, data: {data_hoje}.
    
    Frase do usuário: "{texto_usuario}"

    Instruções para o JSON:
    1. "titulo": o que deve ser feito (resumo claro da ação).
    2. "prazo": calcule a data exata no formato YYYY-MM-DD considerando que HOJE é {dia_nome} ({data_hoje}).
       - Exemplo: Se hoje é {dia_nome} e o usuário disser "próxima sexta-feira", calcule os dias até a próxima sexta-feira a partir de {data_hoje}.
    """

    try:
        response = ollama.chat(
            model=modelo,
            messages=[{"role": "user", "content": prompt}],
            format="json",
            options={"temperature": 0.1}
        )

        conteudo = response["message"]["content"].strip()
        dados = json.loads(conteudo)
        return dados

    except Exception as e:
        print(f"\n [ERRO NA IA] Não foi possível processar a entrada. Detalhes: {e}")
        return None


# -------------------------------------------------------------------
# INTERFACE DO USUÁRIO
# -------------------------------------------------------------------

def main():
    gerenciador = ListaEncadeadaTarefa()

    while True:
        print("\n--- GERENCIADOR DE TAREFAS INTELIGENTE ---")
        print("1. Adicionar Tarefa (Linguagem Natural)")
        print("2. Listar Tarefas (Ordenadas por Prazo)")
        print("3. Concluir Tarefa mais Urgente (Pop)")
        print("4. Sair")
        opcao = input("Escolha uma opção (1-4): ").strip()

        if opcao == "1":
            frase = input("\nDigite a tarefa livremente (ex: 'Enviar e-mail para cliente até sexta'): ")
            print("🤖 Processando com IA via Ollama...")

            dados = extrair_tarefa_ia(frase)

            if dados and "titulo" in dados and "prazo" in dados:
                gerenciador.insert_ordered(dados["titulo"], dados["prazo"])
                print(f"✓ Sucesso! Tarefa '{dados['titulo']}' agendada para {dados['prazo']}.")
            else:
                print("❌ Falha ao extrair dados. Tente digitar de forma mais clara.")

        elif opcao == "2":
            gerenciador.exibir_tarefas()

        elif opcao == "3":
            removida = gerenciador.pop_inicio()
            if removida:
                print(f"\n✓ Tarefa concluída e removida: [{removida.prazo}] {removida.titulo}")
            else:
                print("\nNenhuma tarefa para concluir.")

        elif opcao == "4":
            print("\nSaindo do sistema. Até a próxima!")
            break
        else:
            print("Opção inválida. Digite um número entre 1 e 4.")


if __name__ == "__main__":
    main()