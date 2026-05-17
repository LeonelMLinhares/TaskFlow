"""
TaskFlow - Módulo de gerenciamento de tarefas.
"""

import json
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "tasks.json")


def _load_tasks() -> list[dict]:
    """Carrega as tarefas do arquivo JSON."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_tasks(tasks: list[dict]) -> None:
    """Salva as tarefas no arquivo JSON."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def add_task(titulo: str, materia: str, prazo: str) -> dict:
    """
    Adiciona uma nova tarefa.

    Args:
        titulo: Título da tarefa (não pode ser vazio).
        materia: Nome da matéria/disciplina (não pode ser vazio).
        prazo: Data de prazo no formato YYYY-MM-DD.

    Returns:
        Dicionário com os dados da tarefa criada.

    Raises:
        ValueError: Se algum campo obrigatório for inválido.
    """
    if not titulo or not titulo.strip():
        raise ValueError("O título da tarefa não pode ser vazio.")
    if not materia or not materia.strip():
        raise ValueError("A matéria não pode ser vazia.")
    if not prazo or not prazo.strip():
        raise ValueError("O prazo não pode ser vazio.")

    try:
        datetime.strptime(prazo, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("Prazo deve estar no formato YYYY-MM-DD.") from exc

    tasks = _load_tasks()
    task = {
        "id": len(tasks) + 1,
        "titulo": titulo.strip(),
        "materia": materia.strip(),
        "prazo": prazo.strip(),
        "concluida": False,
        "criada_em": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    tasks.append(task)
    _save_tasks(tasks)
    return task


def list_tasks(apenas_pendentes: bool = False) -> list[dict]:
    """
    Lista todas as tarefas.

    Args:
        apenas_pendentes: Se True, retorna apenas tarefas não concluídas.

    Returns:
        Lista de tarefas.
    """
    tasks = _load_tasks()
    if apenas_pendentes:
        tasks = [t for t in tasks if not t["concluida"]]
    return tasks


def complete_task(task_id: int) -> dict:
    """
    Marca uma tarefa como concluída.

    Args:
        task_id: ID da tarefa a ser concluída.

    Returns:
        Dicionário com os dados atualizados da tarefa.

    Raises:
        ValueError: Se a tarefa não for encontrada ou já estiver concluída.
    """
    if task_id <= 0:
        raise ValueError("ID de tarefa inválido.")

    tasks = _load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            if task["concluida"]:
                raise ValueError(f"Tarefa #{task_id} já está concluída.")
            task["concluida"] = True
            _save_tasks(tasks)
            return task

    raise ValueError(f"Tarefa #{task_id} não encontrada.")


def remove_task(task_id: int) -> dict:
    """
    Remove uma tarefa pelo ID.

    Args:
        task_id: ID da tarefa a ser removida.

    Returns:
        Dicionário com os dados da tarefa removida.

    Raises:
        ValueError: Se a tarefa não for encontrada.
    """
    if task_id <= 0:
        raise ValueError("ID de tarefa inválido.")

    tasks = _load_tasks()
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            removed = tasks.pop(i)
            _save_tasks(tasks)
            return removed

    raise ValueError(f"Tarefa #{task_id} não encontrada.")


def search_tasks(termo: str) -> list[dict]:
    """
    Busca tarefas pelo título ou matéria.

    Args:
        termo: Texto para busca (não pode ser vazio).

    Returns:
        Lista de tarefas que correspondem ao termo.

    Raises:
        ValueError: Se o termo de busca for vazio.
    """
    if not termo or not termo.strip():
        raise ValueError("O termo de busca não pode ser vazio.")

    termo_lower = termo.strip().lower()
    tasks = _load_tasks()
    return [
        t
        for t in tasks
        if termo_lower in t["titulo"].lower() or termo_lower in t["materia"].lower()
    ]
