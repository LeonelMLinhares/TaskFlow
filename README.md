#  TaskFlow — Gerenciador de Tarefas para Estudantes

![CI](https://github.com/LeonelMLinhares/TaskFlow/actions/workflows/ci.yml/badge.svg)
![Versão](https://img.shields.io/badge/versão-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)

---

##  Problema Real

Estudantes de todos os níveis — ensino médio, técnico e superior — frequentemente perdem prazos de provas, trabalhos e entregas por falta de organização. Agendas físicas se perdem, aplicativos complexos demandam conta e internet, e planilhas são difíceis de manter no dia a dia.

**TaskFlow** resolve isso com uma ferramenta leve, rápida e que funciona offline, diretamente no terminal.

---

##  Proposta da Solução

Uma aplicação CLI (linha de comando) em Python que permite ao estudante:

- Cadastrar tarefas com título, matéria e prazo
- Listar todas as tarefas ou somente as pendentes
- Marcar tarefas como concluídas
- Remover tarefas desnecessárias
- Buscar tarefas por título ou matéria

Os dados são armazenados localmente em um arquivo JSON — sem necessidade de internet ou conta em serviço externo.

---

##  Público-alvo

Estudantes do ensino médio, técnico e superior que desejam controlar suas tarefas acadêmicas de forma simples, rápida e sem dependência de internet.

---

##  Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| Adicionar tarefa | Cadastra título, matéria e prazo |
| Listar tarefas | Exibe todas ou apenas as pendentes |
| Concluir tarefa | Marca uma tarefa como feita |
| Remover tarefa | Exclui uma tarefa pelo ID |
| Buscar tarefas | Filtra por título ou matéria |

---

##  Tecnologias utilizadas

- **Python 3.11+**
- **pytest** — testes automatizados
- **ruff** — linting e análise estática
- **GitHub Actions** — integração contínua (CI)

---

##  Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/LeonelMLinhares/TaskFlow.git
cd taskflow

# 2. (Opcional) Crie e ative um ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 3. Instale as dependências
pip install -r requirements.txt
```

---

##  Como executar

```bash
python main.py
```

O menu interativo será exibido:

```
=======================================================
        TaskFlow — Gerenciador de Tarefas
=======================================================

O que deseja fazer?
  1. Adicionar tarefa
  2. Listar tarefas
  3. Concluir tarefa
  4. Remover tarefa
  5. Buscar tarefas
  0. Sair
```

---

##  Como rodar os testes

```bash
pytest tests/ -v
```

Saída esperada:

```
tests/test_tasks.py::TestAddTask::test_adiciona_tarefa_valida PASSED
tests/test_tasks.py::TestAddTask::test_titulo_vazio_levanta_erro PASSED
...
```

---

##  Como rodar o lint

```bash
ruff check src/ main.py
```

---

##  Estrutura do projeto

```
taskflow/
├── src/
│   ├── __init__.py
│   └── tasks.py          # Lógica principal
├── tests/
│   ├── __init__.py
│   └── test_tasks.py     # Testes automatizados
├── .github/
│   └── workflows/
│       └── ci.yml        # Pipeline de CI
├── main.py               # Ponto de entrada CLI
├── pyproject.toml        # Versão e configurações
├── requirements.txt      # Dependências
├── .gitignore
└── README.md
```

---

##  Versão atual

**1.0.0** — veja [pyproject.toml](./pyproject.toml)

---

##  Autor

Leonel Martins Linhares
- GitHub: [@LeonelMLinhares](https://github.com/LeonelMLinhares)

---

## 🔗 Repositório

[https://github.com/LeonelMLinhares/TaskFlow]([https://github.com/LeonelMLinhares/TaskFlow)
