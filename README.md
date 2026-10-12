# Projeto 2 - Gerenciador de Tarefas Automático com IA

Projeto desenvolvido para a disciplina de **Estrutura de Dados**, conectando teoria de estruturas encadeadas com Inteligência Artificial local via **Ollama**.

## 📌 Sobre o Projeto
O sistema permite ao usuário cadastrar tarefas usando linguagem natural (ex: *"Comprar material escolar até a próxima segunda"*). A IA extrai o **título** e o **prazo (YYYY-MM-DD)** e o sistema insere o registro de forma **ordenada por data** em uma **Lista Encadeada**.

## 🚀 Requisitos de Avaliação Atendidos
- **Construção do Zero (70%):** Estrutura de dados desenvolvida totalmente utilizando ponteiros/nós manuais, sem usar `list`, `.append()`, ou bibliotecas nativas de dados do Python.
- **Integração com IA (20%):** Comunicação realizada via biblioteca oficial do `ollama` para estruturar dados em JSON.
- **Qualidade do Código (10%):** Código comentado, tipado e legível.

## 🛠️ Tecnologias Utilizadas
- **Linguagem:** Python 3
- **LLM Local:** Ollama (`llama3` ou `phi3`)

## ⚙️ Como Executar

1. **Instale e execute o Ollama:**
   Certifique-se de que o Ollama está instalado na máquina e baixe o modelo desejado:
   ```bash
   ollama pull llama3
   ```

2. **Instale as dependências Python:**
   ```bash
   pip install ollama
   ```

3. **Execute o projeto:**
   ```bash
   python main.py
   ```