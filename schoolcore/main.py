"""
Módulo: main
-------------
Ponto de entrada do sistema SchoolCore — Sistema Integrado de Gestão
Escolar (módulo de Programação de Computadores).

Apresenta um menu interativo em modo texto que permite ao usuário
acessar todos os módulos implementados:

    1) Gestão de Alunos
    2) Gestão de Professores
    3) Gestão de Disciplinas
    4) Gestão de Turmas
    5) Matrículas
    6) Módulo Acadêmico (notas, frequência e boletim)
    7) Módulo Gerencial (relatórios)
    0) Sair

Todas as operações são protegidas por blocos try/except, capturando as
exceções customizadas definidas em `excecoes.py` e exibindo mensagens
de erro amigáveis ao usuário, sem interromper a execução do programa.
"""

from sistema import SistemaSchoolCore
from excecoes import SchoolCoreError
from utils import linha_separadora


# ----------------------------------------------------------------------
# Funções auxiliares de entrada de dados
# ----------------------------------------------------------------------

def ler_texto(mensagem, obrigatorio=True):
    """Lê uma string do usuário, repetindo a pergunta caso o campo
    seja obrigatório e o usuário não informe nada.
    """
    while True:
        valor = input(mensagem).strip()
        if valor or not obrigatorio:
            return valor
        print("Este campo é obrigatório. Tente novamente.")


def ler_inteiro(mensagem):
    """Lê um número inteiro do usuário, repetindo a pergunta em caso
    de entrada inválida.
    """
    while True:
        valor = input(mensagem).strip()
        try:
            return int(valor)
        except ValueError:
            print("Valor inválido. Digite um número inteiro.")


def ler_float(mensagem):
    """Lê um número decimal (float) do usuário, repetindo a pergunta
    em caso de entrada inválida.
    """
    while True:
        valor = input(mensagem).strip().replace(",", ".")
        try:
            return float(valor)
        except ValueError:
            print("Valor inválido. Digite um número (ex.: 7.5).")


def ler_opcional(mensagem):
    """Lê um valor opcional. Retorna None se o usuário não digitar nada."""
    valor = input(mensagem).strip()
    return valor if valor else None


def pausar():
    """Pausa a execução até o usuário pressionar ENTER."""
    input("\nPressione ENTER para continuar...")


# ----------------------------------------------------------------------
# Módulo 1: Gestão de Alunos
# ----------------------------------------------------------------------

def menu_alunos(sistema):
    while True:
        print("\n" + linha_separadora("="))
        print("MÓDULO DE GESTÃO DE ALUNOS")
        print(linha_separadora("="))
        print("1 - Cadastrar aluno")
        print("2 - Consultar aluno")
        print("3 - Listar alunos")
        print("4 - Atualizar aluno")
        print("5 - Excluir/inativar aluno")
        print("0 - Voltar ao menu principal")

        opcao = ler_texto("Escolha uma opção: ")

        try:
            if opcao == "1":
                matricula = ler_texto("Matrícula: ")
                nome = ler_texto("Nome completo: ")
                cpf = ler_texto("CPF: ")
                data_nascimento = ler_texto("Data de nascimento (DD/MM/AAAA): ")
                curso = ler_texto("Curso: ")
                periodo = ler_inteiro("Período: ")
                aluno = sistema.cadastrar_aluno(
                    matricula, nome, cpf, data_nascimento, curso, periodo
                )
                print(f"\nAluno cadastrado com sucesso:\n  {aluno}")

            elif opcao == "2":
                matricula = ler_texto("Matrícula do aluno: ")
                aluno = sistema.consultar_aluno(matricula)
                print(f"\n{aluno}")

            elif opcao == "3":
                alunos = sistema.listar_alunos()
                print(f"\nTotal de alunos: {len(alunos)}")
                for aluno in alunos:
                    print(f"  {aluno}")

            elif opcao == "4":
                matricula = ler_texto("Matrícula do aluno a atualizar: ")
                print("Deixe em branco os campos que não deseja alterar.")
                novo_nome = ler_opcional("Novo nome: ")
                novo_email = ler_opcional("Novo e-mail: ")
                novo_curso = ler_opcional("Novo curso: ")
                novo_periodo = ler_opcional("Novo período: ")
                novo_status = ler_opcional(
                    "Novo status (ativo/trancado/formado/inativo): "
                )

                campos = {}
                if novo_nome:
                    campos["nome"] = novo_nome
                if novo_email:
                    campos["email"] = novo_email
                if novo_curso:
                    campos["curso"] = novo_curso
                if novo_periodo:
                    campos["periodo"] = int(novo_periodo)
                if novo_status:
                    campos["status_academico"] = novo_status

                aluno = sistema.atualizar_aluno(matricula, **campos)
                print(f"\nAluno atualizado com sucesso:\n  {aluno}")

            elif opcao == "5":
                matricula = ler_texto("Matrícula do aluno: ")
                confirmar = ler_texto(
                    "Deseja apenas inativar (I) ou excluir definitivamente (E)? [I/E]: "
                ).strip().upper()
                if confirmar == "E":
                    sistema.excluir_aluno(matricula, inativar=False)
                    print("\nAluno removido definitivamente do sistema.")
                else:
                    aluno = sistema.excluir_aluno(matricula, inativar=True)
                    print(f"\nAluno inativado com sucesso:\n  {aluno}")

            elif opcao == "0":
                return

            else:
                print("Opção inválida.")

        except SchoolCoreError as erro:
            print(f"\n[ERRO] {erro}")
        except ValueError:
            print("\n[ERRO] Valor numérico inválido informado.")

        pausar()


# ----------------------------------------------------------------------
# Módulo 2: Gestão de Professores
# ----------------------------------------------------------------------

def menu_professores(sistema):
    while True:
        print("\n" + linha_separadora("="))
        print("MÓDULO DE GESTÃO DE PROFESSORES")
        print(linha_separadora("="))
        print("1 - Cadastrar professor")
        print("2 - Consultar professor")
        print("3 - Listar professores")
        print("4 - Atualizar professor")
        print("0 - Voltar ao menu principal")

        opcao = ler_texto("Escolha uma opção: ")

        try:
            if opcao == "1":
                codigo = ler_texto("Código funcional: ")
                nome = ler_texto("Nome completo: ")
                cpf = ler_texto("CPF: ")
                titulacao = ler_texto(
                    "Titulação (graduado/especialista/mestre/doutor/pós-doutor): "
                )
                area_atuacao = ler_texto("Área de atuação: ")
                professor = sistema.cadastrar_professor(
                    codigo, nome, cpf, titulacao, area_atuacao
                )
                print(f"\nProfessor cadastrado com sucesso:\n  {professor}")

            elif opcao == "2":
                codigo = ler_texto("Código funcional do professor: ")
                professor = sistema.consultar_professor(codigo)
                print(f"\n{professor}")
                if professor.disciplinas_vinculadas:
                    print("  Disciplinas vinculadas: "
                          + ", ".join(professor.disciplinas_vinculadas))
                else:
                    print("  Disciplinas vinculadas: nenhuma")

            elif opcao == "3":
                professores = sistema.listar_professores()
                print(f"\nTotal de professores: {len(professores)}")
                for professor in professores:
                    print(f"  {professor}")

            elif opcao == "4":
                codigo = ler_texto("Código funcional do professor a atualizar: ")
                print("Deixe em branco os campos que não deseja alterar.")
                novo_nome = ler_opcional("Novo nome: ")
                novo_email = ler_opcional("Novo e-mail: ")
                nova_titulacao = ler_opcional(
                    "Nova titulação (graduado/especialista/mestre/doutor/pós-doutor): "
                )
                nova_area = ler_opcional("Nova área de atuação: ")

                campos = {}
                if novo_nome:
                    campos["nome"] = novo_nome
                if novo_email:
                    campos["email"] = novo_email
                if nova_titulacao:
                    campos["titulacao"] = nova_titulacao
                if nova_area:
                    campos["area_atuacao"] = nova_area

                professor = sistema.atualizar_professor(codigo, **campos)
                print(f"\nProfessor atualizado com sucesso:\n  {professor}")

            elif opcao == "0":
                return

            else:
                print("Opção inválida.")

        except SchoolCoreError as erro:
            print(f"\n[ERRO] {erro}")

        pausar()


# ----------------------------------------------------------------------
# Módulo 3: Gestão de Disciplinas
# ----------------------------------------------------------------------

def menu_disciplinas(sistema):
    while True:
        print("\n" + linha_separadora("="))
        print("MÓDULO DE GESTÃO DE DISCIPLINAS")
        print(linha_separadora("="))
        print("1 - Cadastrar disciplina")
        print("2 - Listar disciplinas")
        print("3 - Vincular/alterar professor responsável")
        print("0 - Voltar ao menu principal")

        opcao = ler_texto("Escolha uma opção: ")

        try:
            if opcao == "1":
                codigo = ler_texto("Código da disciplina: ")
                nome = ler_texto("Nome da disciplina: ")
                carga_horaria = ler_inteiro("Carga horária (horas): ")
                periodo = ler_inteiro("Período: ")
                professor = ler_opcional(
                    "Código funcional do professor responsável (opcional): "
                )
                disciplina = sistema.cadastrar_disciplina(
                    codigo, nome, carga_horaria, periodo, professor
                )
                print(f"\nDisciplina cadastrada com sucesso:\n  {disciplina}")

            elif opcao == "2":
                disciplinas = sistema.listar_disciplinas()
                print(f"\nTotal de disciplinas: {len(disciplinas)}")
                for disciplina in disciplinas:
                    print(f"  {disciplina}")

            elif opcao == "3":
                codigo_disciplina = ler_texto("Código da disciplina: ")
                codigo_professor = ler_texto("Código funcional do professor: ")
                disciplina = sistema.vincular_professor_disciplina(
                    codigo_disciplina, codigo_professor
                )
                print(f"\nVínculo atualizado com sucesso:\n  {disciplina}")

            elif opcao == "0":
                return

            else:
                print("Opção inválida.")

        except SchoolCoreError as erro:
            print(f"\n[ERRO] {erro}")

        pausar()


# ----------------------------------------------------------------------
# Módulo 4: Gestão de Turmas
# ----------------------------------------------------------------------

def menu_turmas(sistema):
    while True:
        print("\n" + linha_separadora("="))
        print("MÓDULO DE GESTÃO DE TURMAS")
        print(linha_separadora("="))
        print("1 - Criar turma")
        print("2 - Listar turmas")
        print("0 - Voltar ao menu principal")

        opcao = ler_texto("Escolha uma opção: ")

        try:
            if opcao == "1":
                codigo = ler_texto("Código da turma: ")
                disciplina = ler_texto("Código da disciplina: ")
                professor = ler_opcional(
                    "Código funcional do professor responsável (opcional): "
                )
                capacidade = ler_inteiro("Capacidade de vagas: ")
                turma = sistema.criar_turma(codigo, disciplina, professor, capacidade)
                print(f"\nTurma criada com sucesso:\n  {turma}")

            elif opcao == "2":
                turmas = sistema.listar_turmas()
                print(f"\nTotal de turmas: {len(turmas)}")
                for turma in turmas:
                    print(f"  {turma}")

            elif opcao == "0":
                return

            else:
                print("Opção inválida.")

        except SchoolCoreError as erro:
            print(f"\n[ERRO] {erro}")

        pausar()


# ----------------------------------------------------------------------
# Módulo 5: Matrículas
# ----------------------------------------------------------------------

def menu_matriculas(sistema):
    while True:
        print("\n" + linha_separadora("="))
        print("MÓDULO DE MATRÍCULAS")
        print(linha_separadora("="))
        print("1 - Realizar matrícula")
        print("2 - Cancelar matrícula")
        print("3 - Consultar histórico de matrículas de um aluno")
        print("0 - Voltar ao menu principal")

        opcao = ler_texto("Escolha uma opção: ")

        try:
            if opcao == "1":
                matricula_aluno = ler_texto("Matrícula do aluno: ")
                codigo_turma = ler_texto("Código da turma: ")
                nova = sistema.realizar_matricula(matricula_aluno, codigo_turma)
                print(f"\nMatrícula realizada com sucesso:\n  {nova}")

            elif opcao == "2":
                id_matricula = ler_inteiro("Identificador da matrícula: ")
                matricula = sistema.cancelar_matricula(id_matricula)
                print(f"\nMatrícula cancelada com sucesso:\n  {matricula}")

            elif opcao == "3":
                matricula_aluno = ler_texto("Matrícula do aluno: ")
                historico = sistema.consultar_historico_matricula(matricula_aluno)
                if not historico:
                    print("\nNenhuma matrícula encontrada para este aluno.")
                else:
                    print(f"\nHistórico de matrículas ({len(historico)} registro(s)):")
                    for matricula in historico:
                        print(f"  {matricula}")

            elif opcao == "0":
                return

            else:
                print("Opção inválida.")

        except SchoolCoreError as erro:
            print(f"\n[ERRO] {erro}")

        pausar()


# ----------------------------------------------------------------------
# Módulo 6: Acadêmico (notas, frequência e boletim)
# ----------------------------------------------------------------------

def menu_academico(sistema):
    while True:
        print("\n" + linha_separadora("="))
        print("MÓDULO ACADÊMICO")
        print(linha_separadora("="))
        print("1 - Lançar nota parcial")
        print("2 - Lançar nota final")
        print("3 - Registrar frequência (presença/falta)")
        print("4 - Emitir boletim de um aluno")
        print("0 - Voltar ao menu principal")

        opcao = ler_texto("Escolha uma opção: ")

        try:
            if opcao == "1":
                matricula = ler_texto("Matrícula do aluno: ")
                disciplina = ler_texto("Código da disciplina: ")
                nota = ler_float("Nota parcial (0 a 10): ")
                sistema.lancar_nota_parcial(matricula, disciplina, nota)
                print("\nNota parcial lançada com sucesso.")

            elif opcao == "2":
                matricula = ler_texto("Matrícula do aluno: ")
                disciplina = ler_texto("Código da disciplina: ")
                nota = ler_float("Nota final (0 a 10): ")
                sistema.lancar_nota_final(matricula, disciplina, nota)
                print("\nNota final lançada com sucesso.")

            elif opcao == "3":
                matricula = ler_texto("Matrícula do aluno: ")
                disciplina = ler_texto("Código da disciplina: ")
                resposta = ler_texto("O aluno esteve presente? (S/N): ").strip().upper()
                presente = resposta == "S"
                sistema.registrar_frequencia(matricula, disciplina, presente)
                status = "presença" if presente else "falta"
                print(f"\nFrequência registrada com sucesso ({status}).")

            elif opcao == "4":
                matricula = ler_texto("Matrícula do aluno: ")
                boletim = sistema.emitir_boletim(matricula)
                print(f"\nBoletim do aluno {boletim['matricula']} - {boletim['nome']}")
                print(f"Curso: {boletim['curso']} | Período: {boletim['periodo']}")
                print(linha_separadora("-"))
                if not boletim["disciplinas"]:
                    print("Nenhum dado acadêmico registrado para este aluno.")
                for item in boletim["disciplinas"]:
                    media = item["media"] if item["media"] is not None else "-"
                    frequencia = (
                        f"{item['frequencia']}%"
                        if item["frequencia"] is not None else "-"
                    )
                    print(
                        f"  {item['codigo_disciplina']} - {item['nome_disciplina']}\n"
                        f"    Média: {media} | Frequência: {frequencia} | "
                        f"Situação: {item['situacao']}"
                    )

            elif opcao == "0":
                return

            else:
                print("Opção inválida.")

        except SchoolCoreError as erro:
            print(f"\n[ERRO] {erro}")

        pausar()


# ----------------------------------------------------------------------
# Módulo 7: Gerencial (relatórios)
# ----------------------------------------------------------------------

def menu_gerencial(sistema):
    while True:
        print("\n" + linha_separadora("="))
        print("MÓDULO GERENCIAL - RELATÓRIOS")
        print(linha_separadora("="))
        print("1 - Quantidade de alunos matriculados")
        print("2 - Disciplinas mais ofertadas")
        print("3 - Professores ativos")
        print("4 - Alunos aprovados x reprovados")
        print("5 - Frequência média por turma")
        print("0 - Voltar ao menu principal")

        opcao = ler_texto("Escolha uma opção: ")

        try:
            if opcao == "1":
                total = sistema.relatorio_quantidade_matriculados()
                print(f"\nTotal de matrículas ativas: {total}")

            elif opcao == "2":
                disciplinas = sistema.relatorio_disciplinas_mais_ofertadas()
                if not disciplinas:
                    print("\nNenhuma turma cadastrada.")
                else:
                    print("\nDisciplinas mais ofertadas (por número de turmas):")
                    for codigo, quantidade in disciplinas:
                        print(f"  {codigo}: {quantidade} turma(s)")

            elif opcao == "3":
                professores = sistema.relatorio_professores_ativos()
                print(f"\nProfessores ativos (com disciplinas vinculadas): "
                      f"{len(professores)}")
                for professor in professores:
                    print(f"  {professor}")

            elif opcao == "4":
                resultado = sistema.relatorio_aprovados_reprovados()
                print("\nResultado consolidado de aprovação:")
                print(f"  Aprovados: {resultado['aprovados']}")
                print(f"  Reprovados: {resultado['reprovados']}")
                print(f"  Sem dados suficientes: {resultado['sem_dados']}")

            elif opcao == "5":
                turmas = sistema.relatorio_frequencia_media_por_turma()
                if not turmas:
                    print("\nNenhuma turma cadastrada.")
                else:
                    print("\nFrequência média por turma:")
                    for codigo, media in turmas:
                        media_texto = f"{media}%" if media is not None else "sem dados"
                        print(f"  {codigo}: {media_texto}")

            elif opcao == "0":
                return

            else:
                print("Opção inválida.")

        except SchoolCoreError as erro:
            print(f"\n[ERRO] {erro}")

        pausar()


# ----------------------------------------------------------------------
# Menu principal
# ----------------------------------------------------------------------

def menu_principal():
    """Inicializa o sistema e exibe o menu principal em loop até que
    o usuário escolha a opção de saída.
    """
    sistema = SistemaSchoolCore(diretorio_dados="dados")

    while True:
        print("\n" + linha_separadora("="))
        print("SCHOOLCORE - SISTEMA INTEGRADO DE GESTÃO ESCOLAR")
        print("Centro Educacional Horizonte do Saber")
        print(linha_separadora("="))
        print("1 - Gestão de Alunos")
        print("2 - Gestão de Professores")
        print("3 - Gestão de Disciplinas")
        print("4 - Gestão de Turmas")
        print("5 - Matrículas")
        print("6 - Módulo Acadêmico (notas, frequência e boletim)")
        print("7 - Módulo Gerencial (relatórios)")
        print("0 - Sair")

        opcao = ler_texto("Escolha uma opção: ")

        if opcao == "1":
            menu_alunos(sistema)
        elif opcao == "2":
            menu_professores(sistema)
        elif opcao == "3":
            menu_disciplinas(sistema)
        elif opcao == "4":
            menu_turmas(sistema)
        elif opcao == "5":
            menu_matriculas(sistema)
        elif opcao == "6":
            menu_academico(sistema)
        elif opcao == "7":
            menu_gerencial(sistema)
        elif opcao == "0":
            print("\nEncerrando o SchoolCore. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_principal()
