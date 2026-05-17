# Changelog

Todas as mudanças notáveis neste projeto serão documentadas aqui.
Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/)
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [1.1.0] — Entrega Intermediária

### Adicionado
- Integração com a **Open-Meteo API** (gratuita, sem chave) para previsão do tempo
- Novo módulo `src/clima.py` com funções `buscar_coordenadas`, `buscar_previsao` e `previsao_para_cidade`
- Nova opção **6 — Previsão do tempo 🌤️** no menu CLI
- Testes de integração (`tests/test_clima_integracao.py`) com mocks da API
- Suporte à geocodificação automática de cidades (API Open-Meteo Geocoding)
- Mapeamento de códigos WMO para descrições amigáveis em português
- Este arquivo `CHANGELOG.md`

### Alterado
- `main.py` atualizado com o novo comando de clima
- Versão elevada de `1.0.0` para `1.1.0` em `pyproject.toml`
- `README.md` atualizado com link de deploy e nova funcionalidade documentada

---

## [1.0.0] — Entrega Inicial

### Adicionado
- Módulo `src/tasks.py` com funções `add_task`, `list_tasks`, `complete_task`, `remove_task`, `search_tasks`
- Interface CLI interativa (`main.py`) com menu de 5 opções
- Persistência local em arquivo JSON (`data/tasks.json`)
- Testes automatizados (`tests/test_tasks.py`) cobrindo caminho feliz, entradas inválidas e casos limite
- Configuração de linting com **ruff**
- Pipeline de CI com **GitHub Actions** (lint + testes)
- `README.md` completo com instruções de instalação, uso, testes e lint
- Versionamento semântico via `pyproject.toml`
- Declaração de dependências em `requirements.txt`
