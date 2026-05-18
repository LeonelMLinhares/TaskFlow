"""
Testes automatizados para o módulo de tarefas do TaskFlow.
"""

import pytest

import src.tasks as tasks_module
from src.tasks import add_task, complete_task, list_tasks, remove_task, search_tasks


@pytest.fixture(autouse=True)
def temp_data_file(tmp_path, monkeypatch):
    """Redireciona o arquivo de dados para um diretório temporário em cada teste."""
    fake_file = tmp_path / "tasks.json"
    monkeypatch.setattr(tasks_module, "DATA_FILE", str(fake_file))
    yield fake_file


# ──────────────────────────────────────────────
# Testes: add_task
# ──────────────────────────────────────────────

class TestAddTask:
    def test_adiciona_tarefa_valida(self):
        """Caminho feliz: tarefa com todos os campos corretos."""
        task = add_task("Trabalho de Matemática", "Matemática", "2025-12-01")
        assert task["titulo"] == "Trabalho de Matemática"
        assert task["materia"] == "Matemática"
        assert task["prazo"] == "2025-12-01"
        assert task["concluida"] is False
        assert task["id"] == 1

    def test_titulo_vazio_levanta_erro(self):
        """Entrada inválida: título vazio deve levantar ValueError."""
        with pytest.raises(ValueError, match="título"):
            add_task("", "Física", "2025-11-10")

    def test_titulo_apenas_espacos_levanta_erro(self):
        """Entrada inválida: título com apenas espaços."""
        with pytest.raises(ValueError, match="título"):
            add_task("   ", "Física", "2025-11-10")

    def test_materia_vazia_levanta_erro(self):
        """Entrada inválida: matéria vazia deve levantar ValueError."""
        with pytest.raises(ValueError, match="matéria"):
            add_task("Prova final", "", "2025-11-10")

    def test_prazo_formato_invalido_levanta_erro(self):
        """Entrada inválida: prazo fora do formato YYYY-MM-DD."""
        with pytest.raises(ValueError, match="formato"):
            add_task("Redação", "Português", "10/11/2025")

    def test_prazo_vazio_levanta_erro(self):
        """Entrada inválida: prazo vazio deve levantar ValueError."""
        with pytest.raises(ValueError, match="prazo"):
            add_task("Redação", "Português", "")

    def test_ids_incrementais(self):
        """Caso limite: IDs devem ser sequenciais."""
        t1 = add_task("Tarefa 1", "Biologia", "2025-10-01")
        t2 = add_task("Tarefa 2", "Química", "2025-10-02")
        assert t1["id"] == 1
        assert t2["id"] == 2


# ──────────────────────────────────────────────
# Testes: list_tasks
# ──────────────────────────────────────────────

class TestListTasks:
    def test_lista_vazia_sem_tarefas(self):
        """Caminho feliz: lista vazia quando não há tarefas."""
        assert list_tasks() == []

    def test_lista_todas_as_tarefas(self):
        """Caminho feliz: retorna todas as tarefas adicionadas."""
        add_task("T1", "Mat", "2025-09-01")
        add_task("T2", "Fis", "2025-09-02")
        assert len(list_tasks()) == 2

    def test_filtro_apenas_pendentes(self):
        """Caso limite: filtro deve ocultar tarefas concluídas."""
        add_task("T1", "Mat", "2025-09-01")
        add_task("T2", "Fis", "2025-09-02")
        complete_task(1)
        pendentes = list_tasks(apenas_pendentes=True)
        assert len(pendentes) == 1
        assert pendentes[0]["titulo"] == "T2"


# ──────────────────────────────────────────────
# Testes: complete_task
# ──────────────────────────────────────────────

class TestCompleteTask:
    def test_conclui_tarefa_existente(self):
        """Caminho feliz: tarefa marcada como concluída."""
        add_task("Estudar", "História", "2025-08-20")
        task = complete_task(1)
        assert task["concluida"] is True

    def test_tarefa_ja_concluida_levanta_erro(self):
        """Entrada inválida: concluir uma tarefa já concluída."""
        add_task("Estudar", "História", "2025-08-20")
        complete_task(1)
        with pytest.raises(ValueError, match="já está concluída"):
            complete_task(1)

    def test_id_inexistente_levanta_erro(self):
        """Entrada inválida: ID que não existe."""
        with pytest.raises(ValueError, match="não encontrada"):
            complete_task(999)

    def test_id_invalido_levanta_erro(self):
        """Entrada inválida: ID zero ou negativo."""
        with pytest.raises(ValueError, match="inválido"):
            complete_task(0)


# ──────────────────────────────────────────────
# Testes: remove_task
# ──────────────────────────────────────────────

class TestRemoveTask:
    def test_remove_tarefa_existente(self):
        """Caminho feliz: tarefa removida com sucesso."""
        add_task("Deletar", "Arte", "2025-07-15")
        removed = remove_task(1)
        assert removed["titulo"] == "Deletar"
        assert list_tasks() == []

    def test_remove_tarefa_inexistente_levanta_erro(self):
        """Entrada inválida: remover ID que não existe."""
        with pytest.raises(ValueError, match="não encontrada"):
            remove_task(42)

    def test_id_invalido_levanta_erro(self):
        """Entrada inválida: ID negativo."""
        with pytest.raises(ValueError, match="inválido"):
            remove_task(-1)


# ──────────────────────────────────────────────
# Testes: search_tasks
# ──────────────────────────────────────────────

class TestSearchTasks:
    def test_busca_por_titulo(self):
        """Caminho feliz: encontra tarefa pelo título."""
        add_task("Prova de Cálculo", "Matemática", "2025-11-30")
        results = search_tasks("cálculo")
        assert len(results) == 1

    def test_busca_por_materia(self):
        """Caminho feliz: encontra tarefa pela matéria."""
        add_task("Lista de exercícios", "Física", "2025-11-30")
        results = search_tasks("física")
        assert len(results) == 1

    def test_busca_case_insensitive(self):
        """Caso limite: busca deve ignorar maiúsculas/minúsculas."""
        add_task("TRABALHO FINAL", "HISTÓRIA", "2025-12-01")
        assert len(search_tasks("trabalho")) == 1
        assert len(search_tasks("história")) == 1

    def test_busca_sem_resultados(self):
        """Caso limite: busca sem correspondência retorna lista vazia."""
        add_task("Tarefa de Biologia", "Biologia", "2025-10-10")
        assert search_tasks("química") == []

    def test_termo_vazio_levanta_erro(self):
        """Entrada inválida: termo vazio deve levantar ValueError."""
        with pytest.raises(ValueError, match="busca"):
            search_tasks("")
