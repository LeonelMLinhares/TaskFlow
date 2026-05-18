#  TaskFlow — Gerenciador de Tarefas para Estudantes

![CI](https://github.com/SEU_USUARIO/taskflow/actions/workflows/ci.yml/badge.svg)
![Versão](https://img.shields.io/badge/versão-1.1.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)

🔗 **[Aplicação publicada — ver no Render](https://dashboard.render.com/web/srv-d856fe9kh4rs73dlkbmg)**

---

##  Problema Real

Estudantes de todos os níveis perdem prazos por falta de organização. Além disso, o clima influencia a produtividade: saber se vai chover amanhã ajuda a decidir entre estudar em casa ou fazer atividades externas.

**TaskFlow** resolve isso com uma ferramenta leve, rápida e sem dependência de conta externa.

---

##  Proposta da Solução

CLI em Python que permite ao estudante:

- Cadastrar tarefas com título, matéria e prazo
- Listar todas as tarefas ou somente as pendentes
- Marcar tarefas como concluídas
- Remover tarefas desnecessárias
- Buscar tarefas por título ou matéria
- **Consultar previsão do tempo** para planejar os estudos (via Open-Meteo API 🌤️)

---

##  Público-alvo

Estudantes do ensino médio, técnico e superior.

---

##  Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| Adicionar tarefa | Cadastra título, matéria e prazo |
| Listar tarefas | Exibe todas ou apenas as pendentes |
| Concluir tarefa | Marca uma tarefa como feita |
| Remover tarefa | Exclui uma tarefa pelo ID |
| Buscar tarefas | Filtra por título ou matéria |
| **Previsão do tempo**  | Consulta clima por cidade via Open-Meteo API |

---

##  API Utilizada

**[Open-Meteo](https://open-meteo.com/)** — gratuita, aberta, sem chave de acesso.

- Geocodificação: converte nome de cidade em coordenadas
- Previsão: temperatura máx/mín e condição climática para até 7 dias

---

##  Tecnologias

- **Python 3.11+**
- **pytest** — testes automatizados
- **ruff** — linting e análise estática
- **GitHub Actions** — CI
- **Open-Meteo API** — previsão do tempo

---

##  Instalação

```bash
git clone https://github.com/LeonelMLinhares/TaskFlow.git
cd taskflow
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

---

##  Como executar

```bash
python main.py
```

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
  6. Previsão do tempo 
  0. Sair
```

Exemplo da previsão do tempo:

```
 Curitiba, Brasil

   2025-08-01
       Chuva leve
       Máx: 18.0°C  |  Mín: 12.0°C

   2025-08-02
       Céu limpo
       Máx: 22.5°C  |  Mín: 13.0°C
```

---

##  Como rodar os testes

```bash
pytest tests/ -v
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
│   ├── tasks.py                  # Lógica de tarefas
│   └── clima.py                  # Integração com Open-Meteo API
├── tests/
│   ├── __init__.py
│   ├── test_tasks.py             # Testes unitários
│   └── test_clima_integracao.py  # Testes de integração (mock)
├── .github/
│   └── workflows/
│       └── ci.yml
├── main.py
├── pyproject.toml
├── requirements.txt
├── CHANGELOG.md
├── .gitignore
└── README.md
```

---

##  Versão atual

**1.1.0** — veja [CHANGELOG.md](./CHANGELOG.md)

---

##  Autor

**Leonel Martins Linhares** — [@LeonelMLinhares](https://github.com/LeonelMLinhares)

🔗 [https://github.com/LeonelMLinhares/TaskFlow](https://github.com/LeonelMLinhares/TaskFlow)
