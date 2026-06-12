"""
Módulo: testes_sistema
------------------------
Script de teste manual/demonstrativo do SistemaSchoolCore.

Este script não faz parte do sistema entregue ao usuário final; serve
apenas para validar, de forma automatizada, que as principais
funcionalidades de cada módulo estão funcionando corretamente
(cadastros, matrículas, lançamento de notas/frequência, boletim e
relatórios), incluindo o tratamento das exceções customizadas.

Execução:
    python testes_sistema.py
"""

import shutil

from sistema import SistemaSchoolCore
from excecoes import (
    RegistroDuplicadoError,
    RegistroNaoEncontradoError,
    MatriculaDuplicadaError,
    CapacidadeExcedidaError,
    DadosInvalidosError,
)


DIRETORIO_TESTE = "dados_teste"


def secao(titulo):
    print("\n" + "=" * 60)
    print(titulo)
    print("=" * 60)


def principal():
    # Garante um ambiente limpo a cada execução do teste
    shutil.rmtree(DIRETORIO_TESTE, ignore_errors=True)

    sistema = SistemaSchoolCore(diretorio_dados=DIRETORIO_TESTE)

    # ------------------------------------------------------------
    secao("1. Cadastro de professores")
    prof1 = sistema.cadastrar_professor(
        "PROF001", "Ana Souza", "529.982.247-25", "doutor", "Engenharia de Software"
    )
    print(prof1)

    prof2 = sistema.cadastrar_professor(
        "PROF002", "Carlos Lima", "111.444.777-35", "mestre", "Banco de Dados"
    )
    print(prof2)

    # Tentativa de cadastro duplicado deve falhar
    try:
        sistema.cadastrar_professor(
            "PROF001", "Outro Nome", "111.444.777-35", "mestre", "TI"
        )
    except RegistroDuplicadoError as erro:
        print(f"[OK] Erro esperado capturado: {erro}")

    # ------------------------------------------------------------
    secao("2. Cadastro de disciplinas")
    disc1 = sistema.cadastrar_disciplina(
        "ENG101", "Engenharia de Requisitos", 60, 3, "PROF001"
    )
    print(disc1)

    disc2 = sistema.cadastrar_disciplina(
        "BD201", "Banco de Dados I", 80, 2, "PROF002"
    )
    print(disc2)

    # ------------------------------------------------------------
    secao("3. Cadastro de alunos")
    aluno1 = sistema.cadastrar_aluno(
        "2026001", "Gabriel Pereira", "390.533.447-05",
        "15/04/2002", "Engenharia de Software", 2
    )
    print(aluno1)

    aluno2 = sistema.cadastrar_aluno(
        "2026002", "Maria Oliveira", "248.438.034-80",
        "20/08/2001", "Engenharia de Software", 2
    )
    print(aluno2)

    # CPF inválido deve falhar
    try:
        sistema.cadastrar_aluno(
            "2026003", "Aluno Inválido", "111.111.111-11",
            "01/01/2000", "Engenharia de Software", 1
        )
    except DadosInvalidosError as erro:
        print(f"[OK] Erro esperado capturado: {erro}")

    # ------------------------------------------------------------
    secao("4. Criação de turmas")
    turma1 = sistema.criar_turma("T2026-1-ENG101-A", "ENG101", "PROF001", 2)
    print(turma1)

    turma2 = sistema.criar_turma("T2026-1-BD201-A", "BD201", "PROF002", 1)
    print(turma2)

    # ------------------------------------------------------------
    secao("5. Matrículas")
    matricula1 = sistema.realizar_matricula("2026001", "T2026-1-ENG101-A")
    print(matricula1)

    matricula2 = sistema.realizar_matricula("2026002", "T2026-1-ENG101-A")
    print(matricula2)

    matricula3 = sistema.realizar_matricula("2026001", "T2026-1-BD201-A")
    print(matricula3)

    # Matrícula duplicada deve falhar
    try:
        sistema.realizar_matricula("2026001", "T2026-1-ENG101-A")
    except MatriculaDuplicadaError as erro:
        print(f"[OK] Erro esperado capturado: {erro}")

    # Capacidade excedida deve falhar (turma2 tem capacidade 1)
    try:
        sistema.realizar_matricula("2026002", "T2026-1-BD201-A")
    except CapacidadeExcedidaError as erro:
        print(f"[OK] Erro esperado capturado: {erro}")

    # ------------------------------------------------------------
    secao("6. Lançamento de notas e frequência")
    sistema.lancar_nota_parcial("2026001", "ENG101", 8.0)
    sistema.lancar_nota_parcial("2026001", "ENG101", 7.0)
    sistema.lancar_nota_final("2026001", "ENG101", 9.0)

    for _ in range(8):
        sistema.registrar_frequencia("2026001", "ENG101", True)
    for _ in range(2):
        sistema.registrar_frequencia("2026001", "ENG101", False)

    sistema.lancar_nota_parcial("2026001", "BD201", 4.0)
    sistema.lancar_nota_final("2026001", "BD201", 5.0)
    for _ in range(5):
        sistema.registrar_frequencia("2026001", "BD201", True)
    for _ in range(5):
        sistema.registrar_frequencia("2026001", "BD201", False)

    # Nota fora do intervalo deve falhar
    try:
        sistema.lancar_nota_parcial("2026001", "ENG101", 15)
    except DadosInvalidosError as erro:
        print(f"[OK] Erro esperado capturado: {erro}")

    # ------------------------------------------------------------
    secao("7. Boletim do aluno 2026001")
    boletim = sistema.emitir_boletim("2026001")
    print(f"Aluno: {boletim['nome']} | Curso: {boletim['curso']}")
    for item in boletim["disciplinas"]:
        print(
            f"  {item['codigo_disciplina']} - {item['nome_disciplina']}: "
            f"média={item['media']}, frequência={item['frequencia']}%, "
            f"situação={item['situacao']}"
        )

    # ------------------------------------------------------------
    secao("8. Cancelamento de matrícula")
    cancelada = sistema.cancelar_matricula(matricula3.id)
    print(cancelada)

    historico = sistema.consultar_historico_matricula("2026001")
    print(f"Histórico do aluno 2026001 ({len(historico)} registro(s)):")
    for m in historico:
        print(f"  {m}")

    # ------------------------------------------------------------
    secao("9. Relatórios gerenciais")
    print("Quantidade de matrículas ativas:",
          sistema.relatorio_quantidade_matriculados())
    print("Disciplinas mais ofertadas:",
          sistema.relatorio_disciplinas_mais_ofertadas())
    print("Professores ativos:")
    for p in sistema.relatorio_professores_ativos():
        print(f"  {p}")
    print("Aprovados/Reprovados:", sistema.relatorio_aprovados_reprovados())
    print("Frequência média por turma:",
          sistema.relatorio_frequencia_media_por_turma())

    # ------------------------------------------------------------
    secao("10. Persistência - recarregando o sistema a partir do disco")
    sistema2 = SistemaSchoolCore(diretorio_dados=DIRETORIO_TESTE)
    print("Alunos carregados:", len(sistema2.listar_alunos()))
    print("Professores carregados:", len(sistema2.listar_professores()))
    print("Disciplinas carregadas:", len(sistema2.listar_disciplinas()))
    print("Turmas carregadas:", len(sistema2.listar_turmas()))
    aluno_recarregado = sistema2.consultar_aluno("2026001")
    print("Boletim recarregado para 2026001:",
          aluno_recarregado.emitir_boletim())

    # ------------------------------------------------------------
    secao("11. Registro não encontrado")
    try:
        sistema.consultar_aluno("9999999")
    except RegistroNaoEncontradoError as erro:
        print(f"[OK] Erro esperado capturado: {erro}")

    secao("TESTES CONCLUÍDOS COM SUCESSO")

    # Limpa o diretório de teste ao final
    shutil.rmtree(DIRETORIO_TESTE, ignore_errors=True)


if __name__ == "__main__":
    principal()
