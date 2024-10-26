# 🛒 Loja Online - E-commerce com Painel Admin

Este projeto é uma aplicação web de e-commerce desenvolvida com **Flask**, que inclui uma interface pública e um painel administrativo para gerenciar produtos e usuários. A estrutura do projeto é organizada para facilitar a manutenção e escalabilidade.

---

## 📂 Estrutura do Projeto

```bash
.
├── app.py                   # Arquivo principal para execução da aplicação
├── config.py                # Configuração da aplicação
├── instance/
│   └── database.db          # Banco de dados SQLite
├── loja/                    # Diretório principal do projeto
│   ├── __init__.py          # Inicialização da aplicação Flask
│   ├── ext/                 # Extensões e configurações adicionais
│   │   ├── extensions.py    # Registro de extensões (SQLAlchemy, etc.)
│   │   ├── models.py        # Definição dos modelos de dados
│   │   └── routes.py        # Rotas principais da aplicação
│   ├── static/              # Arquivos estáticos (CSS, JS, Imagens)
│   │   ├── css/             # Arquivos CSS para estilização
│   │   ├── img/             # Imagens do site e produtos
│   │   └── scripts/         # Scripts JavaScript
│   └── templates/           # Templates HTML para as páginas
│       └── *.html           # Ex.: admin.html, login.html, index.html
├── requirements.txt         # Dependências do projeto
```
## 🔍 Introdução
O projeto é um sistema completo de e-commerce que oferece:

Catálogo de produtos.
Login e registro de usuários.
Painel administrativo para gerenciar produtos e usuários.
Banco de dados SQLite para armazenar os dados.
Este projeto foi criado para aprender e praticar conceitos de Flask e desenvolvimento web com HTML, CSS e JavaScript.

## 🛠️ Tecnologias Usadas
- Python 3.8+: Linguagem principal para o backend.
- Flask: Framework web para criar a aplicação.
- SQLite: Banco de dados usado no ambiente de desenvolvimento.
- Tailwind CSS: Biblioteca CSS para estilização rápida e responsiva.
- JavaScript: Funcionalidades interativas no frontend.
- HTML5 + Jinja2: Templates dinâmicos para as páginas.

## 🚀 Instruções de Uso
### 📋 Pré-requisitos
Antes de começar, você precisará ter instalado:

- Python 3.8+: [Download Python](https://www.python.org/downloads/)
- Git: [Download Git](https://github.com)

### ⚙️ Instalação
1. Clone este repositório:
   ```
   git clone https://github.com/Codeemserie/e-comerce
   cd ecommerce-admin-panel
   ```
   
2. Crie um ambiente virtual:
    ```
    python -m venv venv
    ```
3.Ative o ambiente virtual:
  - Windows:
      ```
      venv\Scripts\activate
      ```
  - macOS/Linux:
      ```
      source venv/bin/activate
      ```

4. instale as dependências:
   ```
   pip install -r requirements.txt
   ```

## 📂 Estrutura dos Diretórios
  - app.py: Arquivo principal para execução do projeto.
  - config.py: Configurações da aplicação (banco de dados, chaves secretas, etc.).
  - instance/database.db: Arquivo do banco de dados SQLite.
  - loja/: Diretório principal do projeto contendo módulos e rotas.
  - static/: Diretório para arquivos estáticos (CSS, JS, Imagens).
  - templates/: Templates HTML para renderização das páginas.
   
## 📜 Licença
Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para mais informações.
