# Paciência Educacional

**Paciência Educacional** é um projeto acadêmico desenvolvido para a disciplina de **Estruturas de Dados e Análise de Algoritmos** do Mestrado em Computação Aplicada.

O objetivo deste projeto é demonstrar o funcionamento prático de estruturas de dados (Pilhas, Filas, Listas Ligadas) e algoritmos de ordenação e busca através de um jogo interativo (Paciência/Solitaire).

## 🎯 Objetivo Acadêmico

Este não é um projeto comercial. Ele foi desenhado como um Objeto de Aprendizagem onde os alunos podem jogar Solitaire na metade da tela, enquanto na outra metade observam, em tempo real:
- O estado das **Estruturas de Dados**;
- O **Pseudocódigo** das operações com destaque na linha atual;
- Os **Logs** detalhados mostrando as variáveis em cada passo;
- Uma comparação analítica entre Algoritmos de Ordenação (**Bubble Sort, Merge Sort e Quick Sort**).

---

## 🛠️ Stack Tecnológica

O projeto foi dividido em duas partes, implementadas "do zero" sem o uso das bibliotecas embutidas equivalentes para garantir a demonstração explícita de como as estruturas funcionam nos bastidores.

### Backend (Python + FastAPI)
* **Python 3.10+**: Linguagem base para as estruturas de dados.
* **FastAPI**: Criação rápida e robusta de endpoints REST.
* **Pydantic**: Validação de dados (Type hints).
* **Pytest**: Bateria de testes unitários.
* **Estruturas Desenvolvidas**: 
  * `NoEncadeado`
  * `PilhaCartas` (LIFO)
  * `FilaCartas` (FIFO)
  * `ListaLigadaCartas` (Duplamente Encadeada)
* **Algoritmos**: Iterativo vs Recursivo (Embaralhamento), Bubble Sort, Merge Sort, Quick Sort.

### Frontend (React + TypeScript)
* **React 19**: Biblioteca de UI moderna.
* **Vite**: Ferramenta de build rápida.
* **Tailwind CSS**: Estilização baseada em utilitários.
* **Framer Motion**: Animações fluidas das cartas.
* **Axios**: Comunicação eficiente com a API do Backend.
* **Howler**: Sons interativos do jogo.

---

## 🚀 Como Executar Localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/paciencia-educacional.git
cd paciencia-educacional
```

### 2. Configurar o Backend

Abra um terminal e acesse a pasta `backend`:

```bash
cd backend

# Recomenda-se criar um ambiente virtual (venv)
python -m venv .venv

# Ativar no Windows:
.venv\Scripts\activate
# Ativar no Linux/Mac:
source .venv/bin/activate

# Instalar dependências
pip install -e ".[dev]"
# Ou usar o requirements.txt
pip install -r requirements.txt

# Executar a API (estará disponível em http://localhost:8000)
python -m uvicorn main:app --reload --port 8000
```
> A documentação Swagger interativa pode ser vista em [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Configurar o Frontend

Em um **novo terminal**, acesse a pasta `frontend`:

```bash
cd frontend

# Instalar as dependências
npm install --legacy-peer-deps

# Iniciar o servidor de desenvolvimento React
npm run dev
```

Abra o seu navegador em [http://localhost:5173](http://localhost:5173).

---

## 🌐 Como Acessar Online (Deploy)

A arquitetura do projeto permite o deploy independente do Backend e Frontend.
Os arquivos de configuração base já estão presentes nas pastas:

* **Backend**: Pode ser hospedado na plataforma **Railway** (usando `railway.toml` e `Procfile`) ou **Render**.
* **Frontend**: Pode ser hospedado na **Vercel** (usando o `vercel.json`) ou **Netlify**. Lembre-se de definir a variável de ambiente `VITE_API_URL` com a URL do Backend em produção.

---

## 📚 Referências

- [Visualgo.net](https://visualgo.net/en/sorting) - Para referência visual de algoritmos de ordenação.
- Material de Aula - Mestrado em Computação Aplicada.
- [FastAPI Documentation](https://fastapi.tiangolo.com/).
- [React Documentation](https://react.dev/).