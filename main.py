"""
TaskFlow CLI - Gerenciador de Tarefas para Estudantes.

Interface de linha de comando para organizar tarefas acadêmicas
com previsão do tempo integrada (Open-Meteo API).
"""

import sys

from src.tasks import add_task, complete_task, list_tasks, remove_task, search_tasks
from src.clima import previsao_para_cidade


def print_header():
    print("=" * 55)
    print("       📚 TaskFlow — Gerenciador de Tarefas")
    print("=" * 55)


def print_task(task: dict):
    status = "✅" if task["concluida"] else "⏳"
    print(f"  [{task['id']}] {status} {task['titulo']}")
    print(f"       Matéria: {task['materia']}  |  Prazo: {task['prazo']}")


def print_menu():
    print("\nO que deseja fazer?")
    print("  1. Adicionar tarefa")
    print("  2. Listar tarefas")
    print("  3. Concluir tarefa")
    print("  4. Remover tarefa")
    print("  5. Buscar tarefas")
    print("  6. Previsão do tempo 🌤️")
    print("  0. Sair")
    print()


def cmd_add():
    print("\n--- Nova Tarefa ---")
    titulo = input("Título: ").strip()
    materia = input("Matéria: ").strip()
    prazo = input("Prazo (YYYY-MM-DD): ").strip()
    try:
        task = add_task(titulo, materia, prazo)
        print(f"\n✅ Tarefa #{task['id']} adicionada com sucesso!")
    except ValueError as e:
        print(f"\n❌ Erro: {e}")


def cmd_list():
    print("\n--- Suas Tarefas ---")
    filtro = input("Mostrar apenas pendentes? (s/n): ").strip().lower()
    apenas_pendentes = filtro == "s"
    tasks = list_tasks(apenas_pendentes=apenas_pendentes)
    if not tasks:
        print("  Nenhuma tarefa encontrada.")
    else:
        for task in tasks:
            print_task(task)
            print()


def cmd_complete():
    print("\n--- Concluir Tarefa ---")
    try:
        task_id = int(input("ID da tarefa: ").strip())
        task = complete_task(task_id)
        print(f"\n✅ Tarefa '{task['titulo']}' marcada como concluída!")
    except ValueError as e:
        print(f"\n❌ Erro: {e}")


def cmd_remove():
    print("\n--- Remover Tarefa ---")
    try:
        task_id = int(input("ID da tarefa: ").strip())
        task = remove_task(task_id)
        print(f"\n🗑️  Tarefa '{task['titulo']}' removida com sucesso!")
    except ValueError as e:
        print(f"\n❌ Erro: {e}")


def cmd_search():
    print("\n--- Buscar Tarefas ---")
    termo = input("Digite o termo de busca: ").strip()
    try:
        tasks = search_tasks(termo)
        if not tasks:
            print("  Nenhuma tarefa encontrada.")
        else:
            print(f"  {len(tasks)} tarefa(s) encontrada(s):")
            for task in tasks:
                print_task(task)
                print()
    except ValueError as e:
        print(f"\n❌ Erro: {e}")


def cmd_clima():
    print("\n--- 🌤️  Previsão do Tempo ---")
    print("Consulte o clima para planejar seus dias de estudo!\n")
    cidade = input("Nome da cidade: ").strip()
    try:
        dias_input = input("Quantos dias de previsão? (1-7, padrão 3): ").strip()
        dias = int(dias_input) if dias_input else 3
    except ValueError:
        dias = 3

    print("\n⏳ Consultando Open-Meteo API...")
    try:
        resultado = previsao_para_cidade(cidade, dias=dias)
        print(f"\n📍 {resultado['cidade']}\n")
        for dia in resultado["previsao"]:
            print(f"  📅 {dia['data']}")
            print(f"     {dia['condicao']}")
            print(f"     🌡️  Máx: {dia['temp_max']}°C  |  Mín: {dia['temp_min']}°C")
            print()
    except ValueError as e:
        print(f"\n❌ Erro: {e}")
    except RuntimeError as e:
        print(f"\n⚠️  Falha de conexão: {e}")


def main():
    print_header()
    while True:
        print_menu()
        opcao = input("Opção: ").strip()
        if opcao == "1":
            cmd_add()
        elif opcao == "2":
            cmd_list()
        elif opcao == "3":
            cmd_complete()
        elif opcao == "4":
            cmd_remove()
        elif opcao == "5":
            cmd_search()
        elif opcao == "6":
            cmd_clima()
        elif opcao == "0":
            print("\nAté logo! Bons estudos 🎓")
            sys.exit(0)
        else:
            print("\n⚠️  Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
