# 📦 Sistema de Controle de Estoque

Sistema web de controle de estoque desenvolvido em Python com Flask, permitindo o gerenciamento de produtos, usuários e movimentações de estoque.

O projeto foi desenvolvido com foco em organização do código, autenticação, controle de acesso por perfil, integração com banco de dados MySQL e disponibilização de uma API REST.

---

## 🚀 Funcionalidades

### 👤 Autenticação e usuários

- Login de usuários
- Logout
- Criação do primeiro administrador pelo terminal
- Cadastro de novos usuários
- Autenticação com senha criptografada
- Controle de acesso por perfil
- Perfis:
  - Administrador
  - Comum

### 📦 Produtos

Usuários administradores podem:

- Cadastrar produtos
- Visualizar produtos
- Editar produtos
- Excluir produtos
- Definir quantidade em estoque
- Definir quantidade mínima
- Visualizar produtos com estoque baixo

Usuários comuns podem:

- Visualizar os produtos
- Consultar o estoque
- Visualizar produtos com estoque baixo

### 🔄 Movimentações de estoque

Administradores podem:

- Registrar entrada de produtos
- Registrar saída de produtos
- Controlar a quantidade disponível
- Registrar o usuário responsável pela movimentação
- Consultar o histórico de movimentações

Usuários comuns não possuem permissão para realizar ou consultar movimentações.

---

## 🔐 Controle de acesso

O sistema possui dois níveis de acesso:

| Funcionalidade | Administrador | Usuário Comum |
|---|:---:|:---:|
| Visualizar estoque | ✅ | ✅ |
| Visualizar produtos | ✅ | ✅ |
| Visualizar estoque baixo | ✅ | ✅ |
| Cadastrar produto | ✅ | ❌ |
| Editar produto | ✅ | ❌ |
| Excluir produto | ✅ | ❌ |
| Entrada de estoque | ✅ | ❌ |
| Saída de estoque | ✅ | ❌ |
| Visualizar movimentações | ✅ | ❌ |
| Cadastrar usuários | ✅ | ❌ |

---

## 🛠️ Tecnologias utilizadas

### Backend

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Login
- Flask-JWT-Extended
- SQLAlchemy
- Alembic
- Werkzeug
- Python-dotenv

### Banco de dados

- MySQL

### API

- REST API
- JSON
- JWT (JSON Web Token)

### Testes

- Pytest
- Postman

### Outras ferramentas

- Git
- GitHub
- VS Code

---

## 📁 Estrutura do projeto

```text
Controle-de-Estoque/
│
├── app/
│   ├── api/
│   │   └── routes.py
│   │
│   ├── core/
│   │   └── routes.py
│   │
│   ├── estoque/
│   │   ├── routes.py
│   │   └── service.py
│   │
│   ├── models/
│   │   ├── estoque.py
│   │   ├── produto.py
│   │   └── usuario.py
│   │
│   ├── services/
│   │   ├── estoque_service.py
│   │   └── produto_service.py
│   │
│   ├── usuario/
│   │   ├── routes.py
│   │   └── service.py
│   │
│   ├── utils/
│   │   └── auth.py
│   │
│   ├── extensions/
│   │   ├── db.py
│   │   ├── jwt.py
│   │   ├── login.py
│   │   └── migrate.py
│   │
│   ├── templates/
│   │
│   ├── static/
│   │
│   └── __init__.py
│
├── migrations/
├── tests/
│
├── criar_admin.py
├── run.py
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

A estrutura pode variar de acordo com a versão atual do projeto.

## ⚙️ Instalação
### 1. Clone o repositório
```bash
git clone https://github.com/Ingridxisto/Controle-de-Estoque.git
```

#### Entre na pasta:

```bash
cd Controle-de-Estoque
```

### 2. Crie um ambiente virtual

#### No Windows:

```bash
python -m venv venv
```

#### Ative o ambiente virtual:

```bash
venv\Scripts\activate
```

#### No Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

##🗄️ Configuração do banco de dados

O projeto utiliza MySQL.

#### Crie um banco de dados no MySQL, por exemplo:

```bash
CREATE DATABASE controle_estoque;
```

#### Depois configure as variáveis de ambiente no arquivo .env.

Exemplo:

```bash
SECRET_KEY=sua_chave_secreta
DATABASE_URL=mysql+pymysql://usuario:senha@localhost/controle_estoque
```

O arquivo .env não deve ser enviado para o GitHub.

## 🔄 Migrações do banco

Depois de configurar o banco de dados, execute:

```bash
flask db upgrade
```

Esse comando cria/atualiza as tabelas de acordo com as migrações do projeto.

## 👑 Criando o primeiro administrador

O projeto possui um script para criar o primeiro administrador.

Execute:

```bash
python criar_admin.py
```

O terminal solicitará:

```bash
Nome do administrador:
Email do administrador:
Senha do administrador:
Confirme a senha:
```

A senha não fica armazenada no código-fonte.

Após a criação, o administrador poderá acessar o sistema e cadastrar os demais usuários pela interface web.

## ▶️ Executando o sistema

Execute:

```bash
python run.py
```

O sistema estará disponível em:

```bash
http://127.0.0.1:5000
```

Faça login utilizando as credenciais do administrador criadas anteriormente.

## 🌐 API REST

O projeto também possui uma API REST protegida por JWT.

```bash
Login
POST /api/login
```

Exemplo:

```bash
{
    "email": "admin@email.com",
    "senha": "sua_senha"
}
```

A API retorna um token JWT que deve ser utilizado nas requisições autenticadas.

## 📦 Produtos

#### Listar produtos

```bash
GET /api/produtos
```

Requer autenticação JWT.

#### Buscar produto

```bash
GET /api/produtos/<produto_id>
```

Requer autenticação JWT.

#### Criar produto

```bash
POST /api/produtos
```

Apenas administradores.

#### Exemplo:

```bash
{
    "nome": "Notebook",
    "descricao": "Notebook para uso profissional",
    "valor": 3500,
    "quantidade": 10,
    "quantidade_minima": 3
}
```

#### Atualizar produto

```bash
PUT /api/produtos/<produto_id>
```

Apenas administradores.

#### Excluir produto

```bash
DELETE /api/produtos/<produto_id>
```

Apenas administradores.

## 🔄 Movimentações

#### Registrar movimentação

```bash
POST /api/movimentacoes
```

Apenas administradores.

Exemplo:

```bash
{
    "produto_id": 1,
    "tipo": "entrada",
    "quantidade": 5
}
```

#### Consultar movimentações

```bash
GET /api/movimentacoes
```

Apenas administradores.

## 🔒 Segurança

O projeto possui algumas medidas de segurança, incluindo:

🔐 Senhas armazenadas utilizando hash  
🔑 Autenticação de usuários  
👥 Controle de acesso por perfil  
🎫 Autenticação JWT para a API  
🛡️ Proteção de rotas administrativas  
🔒 Variáveis sensíveis armazenadas no .env  
🚫 .env incluído no .gitignore  
✅ Validação dos dados recebidos pela API  
✅ Validação de quantidade e valores de produtos  
🛡️ Proteção contra acesso não autorizado às funcionalidades administrativas  

## 🧪 Testes

As funcionalidades da aplicação foram testadas utilizando:

- Interface web  
- Banco de dados MySQL  
- Postman  

Foram realizados testes de:

- Login de administrador  
- Login de usuário comum  
- Cadastro de usuários  
- Cadastro de produtos  
- Edição de produtos  
- Exclusão de produtos  
- Entrada de estoque  
- Saída de estoque  
- Consulta de produtos  
- Consulta de movimentações  
- Permissões de administrador  
- Permissões de usuário comum  
- Endpoints da API  
- Autenticação JWT  
- Validação de dados  

## 📌 Objetivo do projeto

Este projeto foi desenvolvido como forma de aplicar conhecimentos de desenvolvimento backend, incluindo:

- Desenvolvimento de aplicações web com Flask
- Arquitetura e organização de código
- APIs REST
- Autenticação e autorização
- Banco de dados relacionais
ORM com SQLAlchemy
- Migrações com Alembic/Flask-Migrate
- Controle de usuários e permissões
- Manipulação e validação de dados
- Testes de API utilizando Postman

## 👩‍💻 Autora

Ingrid Xisto

Desenvolvedora Back-end Python

Tecnologias de interesse:

🐍 Python  
🌶️ Flask  
🎸 Django  
⚡ FastAPI  
🗄️ SQL  
🔗 APIs REST  
💻 Desenvolvimento de sistemas  
🤖 Inteligência Artificial  

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais e de portfólio.
