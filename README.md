Aqui está um **README.md** bem completo para você usar no seu projeto. Ele inclui uma introdução, funcionalidades, requisitos, guia de instalação e uso, além de informações de contato.

---

### **README.md**

```markdown
# Chatbot RAG - Assistente Inteligente IFAC

Este é um projeto de Chatbot desenvolvido para auxiliar no gerenciamento e consulta de resoluções e documentos no IFAC, utilizando inteligência artificial. O sistema suporta o upload de documentos em PDF e responde a perguntas com base no conteúdo enviado.

## 📋 Funcionalidades

- Upload de múltiplos documentos em PDF.
- Geração de respostas com base no conteúdo dos documentos enviados.
- Interface intuitiva e responsiva.
- Busca semântica eficiente utilizando FAISS e embeddings gerados pelo `sentence-transformers`.
- Integração com a API da OpenAI para respostas contextuais.

## 🛠️ Tecnologias Utilizadas

- **Backend**: Flask
- **Banco de Dados**: MongoDB
- **Busca Semântica**: FAISS
- **Processamento de Texto**: PyPDF2, Sentence Transformers
- **Frontend**: HTML, CSS, JavaScript
- **Integração com IA**: OpenAI API

## 🚀 Requisitos

Certifique-se de ter os seguintes requisitos instalados no ambiente local:

- Python 3.8 ou superior
- MongoDB (local ou MongoDB Atlas)
- Virtualenv (opcional, mas recomendado)
- Conta na [OpenAI](https://platform.openai.com/) para obter a chave da API

## 🛠️ Instalação e Configuração

Siga os passos abaixo para configurar e executar o projeto:

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio
```

### 2. Crie e Ative um Ambiente Virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes configurações:

```env
MONGO_URI=mongodb://localhost:27017/
OPENAI_API_KEY=sua-chave-openai-aqui
```

Substitua `MONGO_URI` pelo URI do seu MongoDB, se estiver utilizando o MongoDB Atlas.

### 5. Execute o Banco de Dados

Certifique-se de que o MongoDB está em execução localmente ou conectado ao Atlas.

### 6. Inicialize o Servidor Flask

```bash
python app.py
```

O servidor estará disponível em [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

---

## 🖥️ Uso

### 1. Enviar Documentos

1. Acesse a página principal.
2. Use o botão **"Enviar Resoluções"** para selecionar múltiplos arquivos PDF.
3. Clique em **"Upload Documento"** para processar os arquivos.

### 2. Consultar o Chatbot

1. Digite sua pergunta no campo de texto.
2. Clique no botão **"Enviar"**.
3. Veja a resposta do chatbot exibida na área de respostas.

---

## 📂 Estrutura do Projeto

```
chatbot_project/
├── app.py                     # Arquivo principal do Flask
├── routes/                    # Rotas do Flask
│   ├── upload_routes.py       # Rotas de upload
│   ├── chat_routes.py         # Rotas do chatbot
├── services/                  # Lógica central
│   ├── faiss_service.py       # Gerenciamento do FAISS
│   ├── pdf_service.py         # Extração de texto de PDFs
│   ├── openai_service.py      # Comunicação com a API OpenAI
├── templates/                 # Arquivos HTML
│   ├── index.html             # Página inicial
├── static/                    # Arquivos estáticos
│   ├── css/                   # Estilos CSS
│   │   ├── css.css
│   ├── js/                    # Scripts JavaScript
│   │   ├── script.js
├── utils/                     # Configurações e funções auxiliares
│   ├── config.py              # Configurações globais (MongoDB, OpenAI)
├── requirements.txt           # Dependências do projeto
├── .env                       # Variáveis de ambiente
```

---

## ⚙️ Testes

### 1. Teste de Funcionalidades

- **Upload de Documentos**: Envie um ou mais PDFs para garantir que os documentos são processados corretamente.
- **Respostas do Chatbot**: Faça perguntas relacionadas aos documentos enviados e valide as respostas.

### 2. Teste do Banco de Dados

Verifique se os documentos e embeddings estão salvos corretamente no MongoDB.

---

## 📝 Contribuição

Contribuições são bem-vindas! Siga os passos abaixo:

1. Faça um fork do projeto.
2. Crie uma branch para sua feature: `git checkout -b minha-feature`.
3. Commit suas mudanças: `git commit -m 'Adiciona minha feature'`.
4. Faça o push para a branch: `git push origin minha-feature`.
5. Abra um Pull Request.

---

## 🛡️ Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

---

## 📞 Contato

- **Nome:** Jeder
- **E-mail:** seuemail@ifac.edu.br
- **LinkedIn:** [Seu Perfil](https://www.linkedin.com/in/seu-perfil/)

---

## 🌟 Agradecimentos

- [OpenAI](https://platform.openai.com/) pela API de IA.
- [Sentence Transformers](https://www.sbert.net/) pelos modelos de embeddings.
- Toda a equipe do IFAC pelo apoio ao desenvolvimento deste projeto.
```

---

### **O que está incluído no README**

1. **Descrição detalhada do projeto**.
2. **Guia de instalação e configuração**.
3. **Instruções para uso das funcionalidades principais**.
4. **Estrutura do projeto** para fácil navegação.
5. **Seção de testes** para validar as funcionalidades.
6. Informações de contribuição, licença e contato.

Se precisar de ajustes ou quiser personalizar algo, estou à disposição! 🚀