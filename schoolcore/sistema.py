"""
Módulo: sistema
----------------
Define a classe `SistemaSchoolCore`, que atua como fachada (facade) de
todas as regras de negócio do sistema acadêmico SchoolCore.

A classe orquestra as entidades de domínio (Aluno, Professor, Disciplina,
Turma e Matricula) e a camada de persistência, oferecendo métodos de
alto nível para:
    - Gestão de Alunos     (cadastrar, consultar, listar, excluir)
    - Gestão de Professores (cadastrar, consultar, listar)
    - Gestão de Disciplinas (cadastrar, listar)
    - Gestão de Turmas      (criar, listar)
    - Módulo de Matrículas  (realizar, cancelar, consultar histórico)
    - Módulo Acadêmico      (notas, frequência, boletim)
    - Módulo Gerencial      (relatórios para a coordenação)

Todas as operações tratam erros por meio das exceções customizadas
definidas em `excecoes.py`.
"""

from modelos.aluno import Aluno
from modelos.professor import Professor
from modelos.disciplina import Disciplina
from modelos.turma import Turma
from modelos.matricula import Matricula
from persistencia import GerenciadorPersistencia
from excecoes import (
    RegistroNaoEncontradoError,
    RegistroDuplicadoError,
    MatriculaDuplicadaError,
)


class SistemaSchoolCore:
    """Fachada principal do sistema acadêmico SchoolCore."""

    def __init__(self, diretorio_dados="dados"):
        """Inicializa o sistema, criando o gerenciador de persistência
        e carregando todos os dados previamente salvos em disco.

        Args:
            diretorio_dados (str): diretório onde os arquivos JSON de
                dados são armazenados.
        """
        self._persistencia = GerenciadorPersistencia(diretorio_dados)

        # Estruturas em memória, indexadas pela chave natural de cada entidade
        self._alunos = {}        # matricula -> Aluno
        self._professores = {}   # codigo_funcional -> Professor
        self._disciplinas = {}   # codigo -> Disciplina
        self._turmas = {}        # codigo -> Turma
        self._matriculas = {}    # id -> Matricula

        self._proximo_id_matricula = 1

        self._carregar_dados()

    # ==================================================================
    # MÓDULO DE GESTÃO DE ALUNOS
    # ==================================================================

    def cadastrar_aluno(self, matricula, nome, cpf, data_nascimento,
                        curso, periodo, status_academico="ativo", email=""):
        """Cadastra um novo aluno no sistema.

        Args:
            matricula (str): matrícula única do aluno.
            nome (str): nome completo.
            cpf (str): CPF do aluno.
            data_nascimento (str): data de nascimento (DD/MM/AAAA).
            curso (str): curso do aluno.
            periodo (int): período/semestre atual.
            status_academico (str, opcional): situação acadêmica.
            email (str, opcional): e-mail de contato.

        Returns:
            Aluno: o objeto aluno recém-criado.

        Raises:
            RegistroDuplicadoError: se já existir um aluno com a mesma matrícula.
            DadosInvalidosError: se algum dado for inválido (propagada de Aluno).
        """
        matricula_normalizada = str(matricula).strip()
        if matricula_normalizada in self._alunos:
            raise RegistroDuplicadoError(
                f"Já existe um aluno cadastrado com a matrícula "
                f"'{matricula_normalizada}'."
            )

        aluno = Aluno(matricula_normalizada, nome, cpf, data_nascimento,
                       curso, periodo, status_academico, email)
        self._alunos[aluno.matricula] = aluno
        self.salvar_dados()
        return aluno

    def consultar_aluno(self, matricula):
        """Consulta um aluno pela matrícula.

        Args:
            matricula (str): matrícula do aluno.

        Returns:
            Aluno: o aluno encontrado.

        Raises:
            RegistroNaoEncontradoError: se nenhum aluno com a matrícula
                informada for encontrado.
        """
        matricula_normalizada = str(matricula).strip()
        aluno = self._alunos.get(matricula_normalizada)
        if aluno is None:
            raise RegistroNaoEncontradoError(
                f"Nenhum aluno encontrado com a matrícula "
                f"'{matricula_normalizada}'."
            )
        return aluno

    def listar_alunos(self, apenas_ativos=False):
        """Lista todos os alunos cadastrados.

        Args:
            apenas_ativos (bool, opcional): se True, retorna apenas alunos
                com status_academico igual a "ativo".

        Returns:
            list[Aluno]: lista de alunos, ordenada pela matrícula.
        """
        alunos = sorted(self._alunos.values(), key=lambda a: a.matricula)
        if apenas_ativos:
            alunos = [a for a in alunos if a.status_academico == "ativo"]
        return alunos

    def atualizar_aluno(self, matricula, **campos):
        """Atualiza um ou mais campos de um aluno já cadastrado.

        Args:
            matricula (str): matrícula do aluno a ser atualizado.
            **campos: campos a atualizar. Aceita "nome", "email",
                "curso", "periodo" e "status_academico".

        Returns:
            Aluno: o aluno atualizado.

        Raises:
            RegistroNaoEncontradoError: se o aluno não existir.
            DadosInvalidosError: se algum valor for inválido.
        """
        aluno = self.consultar_aluno(matricula)

        if "nome" in campos:
            aluno.nome = campos["nome"]
        if "email" in campos:
            aluno.email = campos["email"]
        if "curso" in campos and campos["curso"]:
            aluno._curso = str(campos["curso"]).strip()
        if "periodo" in campos:
            aluno.periodo = campos["periodo"]
        if "status_academico" in campos:
            aluno.status_academico = campos["status_academico"]

        self.salvar_dados()
        return aluno

    def excluir_aluno(self, matricula, inativar=True):
        """Exclui (ou inativa) um aluno do sistema.

        Args:
            matricula (str): matrícula do aluno.
            inativar (bool, opcional): se True (padrão), apenas altera o
                status acadêmico do aluno para "inativo", preservando o
                histórico. Se False, remove o registro definitivamente.

        Returns:
            Aluno | None: o aluno inativado, ou None se foi removido
            definitivamente.

        Raises:
            RegistroNaoEncontradoError: se o aluno não existir.
        """
        aluno = self.consultar_aluno(matricula)

        if inativar:
            aluno.status_academico = "inativo"
            self.salvar_dados()
            return aluno

        del self._alunos[aluno.matricula]
        self.salvar_dados()
        return None

    # ==================================================================
    # MÓDULO DE GESTÃO DE PROFESSORES
    # ==================================================================

    def cadastrar_professor(self, codigo_funcional, nome, cpf, titulacao,
                             area_atuacao, email=""):
        """Cadastra um novo professor no sistema.

        Args:
            codigo_funcional (str): código funcional único do professor.
            nome (str): nome completo.
            cpf (str): CPF do professor.
            titulacao (str): titulação acadêmica.
            area_atuacao (str): área de atuação/especialização.
            email (str, opcional): e-mail de contato.

        Returns:
            Professor: o objeto professor recém-criado.

        Raises:
            RegistroDuplicadoError: se já existir um professor com o
                mesmo código funcional.
        """
        codigo_normalizado = str(codigo_funcional).strip()
        if codigo_normalizado in self._professores:
            raise RegistroDuplicadoError(
                f"Já existe um professor cadastrado com o código "
                f"funcional '{codigo_normalizado}'."
            )

        professor = Professor(codigo_normalizado, nome, cpf, titulacao,
                               area_atuacao, email)
        self._professores[professor.codigo_funcional] = professor
        self.salvar_dados()
        return professor

    def consultar_professor(self, codigo_funcional):
        """Consulta um professor pelo código funcional.

        Args:
            codigo_funcional (str): código funcional do professor.

        Returns:
            Professor: o professor encontrado.

        Raises:
            RegistroNaoEncontradoError: se o professor não existir.
        """
        codigo_normalizado = str(codigo_funcional).strip()
        professor = self._professores.get(codigo_normalizado)
        if professor is None:
            raise RegistroNaoEncontradoError(
                f"Nenhum professor encontrado com o código funcional "
                f"'{codigo_normalizado}'."
            )
        return professor

    def listar_professores(self):
        """Lista todos os professores cadastrados.

        Returns:
            list[Professor]: lista ordenada pelo código funcional.
        """
        return sorted(self._professores.values(), key=lambda p: p.codigo_funcional)

    def atualizar_professor(self, codigo_funcional, **campos):
        """Atualiza um ou mais campos de um professor já cadastrado.

        Args:
            codigo_funcional (str): código funcional do professor.
            **campos: campos a atualizar. Aceita "nome", "email",
                "titulacao" e "area_atuacao".

        Returns:
            Professor: o professor atualizado.

        Raises:
            RegistroNaoEncontradoError: se o professor não existir.
        """
        professor = self.consultar_professor(codigo_funcional)

        if "nome" in campos:
            professor.nome = campos["nome"]
        if "email" in campos:
            professor.email = campos["email"]
        if "titulacao" in campos:
            professor.titulacao = campos["titulacao"]
        if "area_atuacao" in campos and campos["area_atuacao"]:
            professor._area_atuacao = str(campos["area_atuacao"]).strip()

        self.salvar_dados()
        return professor

    # ==================================================================
    # MÓDULO DE GESTÃO DE DISCIPLINAS
    # ==================================================================

    def cadastrar_disciplina(self, codigo, nome, carga_horaria, periodo,
                              professor_responsavel=None):
        """Cadastra uma nova disciplina no sistema.

        Args:
            codigo (str): código único da disciplina.
            nome (str): nome da disciplina.
            carga_horaria (int): carga horária total, em horas.
            periodo (int): período/semestre da disciplina.
            professor_responsavel (str | None, opcional): código
                funcional do professor responsável.

        Returns:
            Disciplina: o objeto disciplina recém-criado.

        Raises:
            RegistroDuplicadoError: se já existir disciplina com o mesmo código.
            RegistroNaoEncontradoError: se o professor responsável informado
                não existir.
        """
        codigo_normalizado = str(codigo).strip().upper()
        if codigo_normalizado in self._disciplinas:
            raise RegistroDuplicadoError(
                f"Já existe uma disciplina cadastrada com o código "
                f"'{codigo_normalizado}'."
            )

        if professor_responsavel:
            professor = self.consultar_professor(professor_responsavel)
        else:
            professor = None

        disciplina = Disciplina(codigo_normalizado, nome, carga_horaria,
                                 periodo, professor_responsavel)
        self._disciplinas[disciplina.codigo] = disciplina

        if professor is not None:
            professor.vincular_disciplina(disciplina.codigo)

        self.salvar_dados()
        return disciplina

    def consultar_disciplina(self, codigo):
        """Consulta uma disciplina pelo código.

        Args:
            codigo (str): código da disciplina.

        Returns:
            Disciplina: a disciplina encontrada.

        Raises:
            RegistroNaoEncontradoError: se a disciplina não existir.
        """
        codigo_normalizado = str(codigo).strip().upper()
        disciplina = self._disciplinas.get(codigo_normalizado)
        if disciplina is None:
            raise RegistroNaoEncontradoError(
                f"Nenhuma disciplina encontrada com o código "
                f"'{codigo_normalizado}'."
            )
        return disciplina

    def listar_disciplinas(self):
        """Lista todas as disciplinas cadastradas.

        Returns:
            list[Disciplina]: lista ordenada pelo código da disciplina.
        """
        return sorted(self._disciplinas.values(), key=lambda d: d.codigo)

    def vincular_professor_disciplina(self, codigo_disciplina, codigo_professor):
        """Vincula (ou substitui) o professor responsável por uma disciplina.

        Args:
            codigo_disciplina (str): código da disciplina.
            codigo_professor (str): código funcional do professor.

        Returns:
            Disciplina: a disciplina atualizada.

        Raises:
            RegistroNaoEncontradoError: se a disciplina ou o professor
                não existirem.
        """
        disciplina = self.consultar_disciplina(codigo_disciplina)
        professor_novo = self.consultar_professor(codigo_professor)

        # Remove o vínculo anterior, se existir
        if disciplina.professor_responsavel:
            try:
                professor_antigo = self.consultar_professor(
                    disciplina.professor_responsavel
                )
                professor_antigo.desvincular_disciplina(disciplina.codigo)
            except RegistroNaoEncontradoError:
                pass

        disciplina.professor_responsavel = professor_novo.codigo_funcional
        professor_novo.vincular_disciplina(disciplina.codigo)

        self.salvar_dados()
        return disciplina

    # ==================================================================
    # MÓDULO DE GESTÃO DE TURMAS
    # ==================================================================

    def criar_turma(self, codigo, disciplina_codigo, professor_codigo, capacidade):
        """Cria uma nova turma vinculada a uma disciplina.

        Args:
            codigo (str): código único da turma.
            disciplina_codigo (str): código da disciplina associada.
            professor_codigo (str | None): código funcional do professor
                responsável pela turma.
            capacidade (int): número máximo de alunos.

        Returns:
            Turma: o objeto turma recém-criado.

        Raises:
            RegistroDuplicadoError: se já existir turma com o mesmo código.
            RegistroNaoEncontradoError: se a disciplina ou o professor
                informados não existirem.
        """
        codigo_normalizado = str(codigo).strip().upper()
        if codigo_normalizado in self._turmas:
            raise RegistroDuplicadoError(
                f"Já existe uma turma cadastrada com o código "
                f"'{codigo_normalizado}'."
            )

        # Garante que a disciplina exista
        self.consultar_disciplina(disciplina_codigo)

        # Garante que o professor exista, caso informado
        if professor_codigo:
            self.consultar_professor(professor_codigo)

        turma = Turma(codigo_normalizado, disciplina_codigo,
                       professor_codigo, capacidade)
        self._turmas[turma.codigo] = turma
        self.salvar_dados()
        return turma

    def consultar_turma(self, codigo):
        """Consulta uma turma pelo código.

        Args:
            codigo (str): código da turma.

        Returns:
            Turma: a turma encontrada.

        Raises:
            RegistroNaoEncontradoError: se a turma não existir.
        """
        codigo_normalizado = str(codigo).strip().upper()
        turma = self._turmas.get(codigo_normalizado)
        if turma is None:
            raise RegistroNaoEncontradoError(
                f"Nenhuma turma encontrada com o código '{codigo_normalizado}'."
            )
        return turma

    def listar_turmas(self):
        """Lista todas as turmas cadastradas.

        Returns:
            list[Turma]: lista ordenada pelo código da turma.
        """
        return sorted(self._turmas.values(), key=lambda t: t.codigo)

    # ==================================================================
    # MÓDULO DE MATRÍCULAS
    # ==================================================================

    def realizar_matricula(self, matricula_aluno, codigo_turma):
        """Realiza a matrícula de um aluno em uma turma.

        Args:
            matricula_aluno (str): matrícula do aluno.
            codigo_turma (str): código da turma.

        Returns:
            Matricula: o registro de matrícula criado.

        Raises:
            RegistroNaoEncontradoError: se o aluno ou a turma não existirem.
            MatriculaDuplicadaError: se o aluno já possuir matrícula ativa
                nessa turma.
            CapacidadeExcedidaError: se a turma já estiver com a
                capacidade máxima de alunos.
        """
        aluno = self.consultar_aluno(matricula_aluno)
        turma = self.consultar_turma(codigo_turma)

        # Impede matrícula duplicada (mesma turma com matrícula ativa)
        for matricula in self._matriculas.values():
            if (matricula.matricula_aluno == aluno.matricula
                    and matricula.codigo_turma == turma.codigo
                    and matricula.esta_ativa()):
                raise MatriculaDuplicadaError(
                    f"O aluno '{aluno.matricula}' já possui matrícula "
                    f"ativa na turma '{turma.codigo}'."
                )

        # Pode levantar CapacidadeExcedidaError
        turma.adicionar_aluno(aluno.matricula)

        nova_matricula = Matricula(self._proximo_id_matricula,
                                    aluno.matricula, turma.codigo)
        self._matriculas[nova_matricula.id] = nova_matricula
        self._proximo_id_matricula += 1

        self.salvar_dados()
        return nova_matricula

    def cancelar_matricula(self, id_matricula):
        """Cancela uma matrícula existente.

        Args:
            id_matricula (int): identificador da matrícula.

        Returns:
            Matricula: a matrícula cancelada.

        Raises:
            RegistroNaoEncontradoError: se a matrícula não existir.
        """
        id_normalizado = int(id_matricula)
        matricula = self._matriculas.get(id_normalizado)
        if matricula is None:
            raise RegistroNaoEncontradoError(
                f"Nenhuma matrícula encontrada com o identificador "
                f"'{id_normalizado}'."
            )

        matricula.cancelar()

        # Remove o aluno da turma, liberando a vaga
        try:
            turma = self.consultar_turma(matricula.codigo_turma)
            turma.remover_aluno(matricula.matricula_aluno)
        except RegistroNaoEncontradoError:
            pass

        self.salvar_dados()
        return matricula

    def consultar_historico_matricula(self, matricula_aluno):
        """Consulta o histórico de matrículas de um aluno.

        Args:
            matricula_aluno (str): matrícula do aluno.

        Returns:
            list[Matricula]: lista de matrículas (ativas e canceladas)
            do aluno, ordenadas pelo identificador.

        Raises:
            RegistroNaoEncontradoError: se o aluno não existir.
        """
        aluno = self.consultar_aluno(matricula_aluno)
        historico = [
            m for m in self._matriculas.values()
            if m.matricula_aluno == aluno.matricula
        ]
        return sorted(historico, key=lambda m: m.id)

    # ==================================================================
    # MÓDULO ACADÊMICO (notas, frequência e boletim)
    # ==================================================================

    def lancar_nota_parcial(self, matricula_aluno, codigo_disciplina, nota):
        """Lança uma nota parcial de um aluno em uma disciplina.

        Args:
            matricula_aluno (str): matrícula do aluno.
            codigo_disciplina (str): código da disciplina.
            nota (float): valor da nota (0 a 10).

        Returns:
            Aluno: o aluno atualizado.

        Raises:
            RegistroNaoEncontradoError: se o aluno ou a disciplina não existirem.
            DadosInvalidosError: se a nota for inválida.
        """
        aluno = self.consultar_aluno(matricula_aluno)
        disciplina = self.consultar_disciplina(codigo_disciplina)
        aluno.lancar_nota_parcial(disciplina.codigo, nota)
        self.salvar_dados()
        return aluno

    def lancar_nota_final(self, matricula_aluno, codigo_disciplina, nota):
        """Lança a nota final de um aluno em uma disciplina.

        Args:
            matricula_aluno (str): matrícula do aluno.
            codigo_disciplina (str): código da disciplina.
            nota (float): valor da nota (0 a 10).

        Returns:
            Aluno: o aluno atualizado.

        Raises:
            RegistroNaoEncontradoError: se o aluno ou a disciplina não existirem.
            DadosInvalidosError: se a nota for inválida.
        """
        aluno = self.consultar_aluno(matricula_aluno)
        disciplina = self.consultar_disciplina(codigo_disciplina)
        aluno.lancar_nota_final(disciplina.codigo, nota)
        self.salvar_dados()
        return aluno

    def registrar_frequencia(self, matricula_aluno, codigo_disciplina, presente):
        """Registra a presença ou falta de um aluno em uma disciplina.

        Args:
            matricula_aluno (str): matrícula do aluno.
            codigo_disciplina (str): código da disciplina.
            presente (bool): True para presença, False para falta.

        Returns:
            Aluno: o aluno atualizado.

        Raises:
            RegistroNaoEncontradoError: se o aluno ou a disciplina não existirem.
        """
        aluno = self.consultar_aluno(matricula_aluno)
        disciplina = self.consultar_disciplina(codigo_disciplina)
        aluno.registrar_frequencia(disciplina.codigo, presente)
        self.salvar_dados()
        return aluno

    def emitir_boletim(self, matricula_aluno):
        """Emite o boletim acadêmico completo de um aluno.

        Args:
            matricula_aluno (str): matrícula do aluno.

        Returns:
            dict: dicionário contendo os dados do aluno e a lista de
            disciplinas com média, frequência e situação final.

        Raises:
            RegistroNaoEncontradoError: se o aluno não existir.
        """
        aluno = self.consultar_aluno(matricula_aluno)
        boletim = aluno.emitir_boletim()

        # Enriquece o boletim com o nome da disciplina, quando disponível
        for item in boletim:
            try:
                disciplina = self.consultar_disciplina(item["codigo_disciplina"])
                item["nome_disciplina"] = disciplina.nome
            except RegistroNaoEncontradoError:
                item["nome_disciplina"] = "(disciplina não encontrada)"

        return {
            "matricula": aluno.matricula,
            "nome": aluno.nome,
            "curso": aluno.curso,
            "periodo": aluno.periodo,
            "disciplinas": boletim,
        }

    # ==================================================================
    # MÓDULO GERENCIAL (relatórios para a coordenação)
    # ==================================================================

    def relatorio_quantidade_matriculados(self):
        """Calcula a quantidade total de matrículas ativas no sistema.

        Returns:
            int: número de matrículas com status "ativa".
        """
        return sum(1 for m in self._matriculas.values() if m.esta_ativa())

    def relatorio_disciplinas_mais_ofertadas(self):
        """Calcula quantas turmas existem para cada disciplina,
        permitindo identificar as disciplinas mais ofertadas.

        Returns:
            list[tuple[str, int]]: lista de tuplas (código da disciplina,
            quantidade de turmas), ordenada da disciplina mais ofertada
            para a menos ofertada.
        """
        contagem = {}
        for turma in self._turmas.values():
            contagem[turma.disciplina_codigo] = contagem.get(
                turma.disciplina_codigo, 0
            ) + 1
        return sorted(contagem.items(), key=lambda item: item[1], reverse=True)

    def relatorio_professores_ativos(self):
        """Lista os professores que possuem ao menos uma disciplina vinculada.

        Returns:
            list[Professor]: lista de professores com disciplinas vinculadas,
            ordenada pelo código funcional.
        """
        ativos = [
            p for p in self._professores.values()
            if len(p.disciplinas_vinculadas) > 0
        ]
        return sorted(ativos, key=lambda p: p.codigo_funcional)

    def relatorio_aprovados_reprovados(self):
        """Calcula a quantidade de situações de "Aprovado" e "Reprovado"
        (em qualquer uma das modalidades) entre todos os alunos e
        disciplinas com dados suficientes.

        Returns:
            dict: dicionário com as chaves "aprovados", "reprovados" e
            "sem_dados", contendo a contagem de cada situação.
        """
        resultado = {"aprovados": 0, "reprovados": 0, "sem_dados": 0}
        for aluno in self._alunos.values():
            for item in aluno.emitir_boletim():
                situacao = item["situacao"]
                if situacao == "Aprovado":
                    resultado["aprovados"] += 1
                elif situacao == "Sem dados suficientes":
                    resultado["sem_dados"] += 1
                else:
                    resultado["reprovados"] += 1
        return resultado

    def relatorio_frequencia_media_por_turma(self):
        """Calcula a frequência média dos alunos de cada turma.

        A frequência média é calculada a partir da frequência de cada
        aluno matriculado na disciplina associada à turma.

        Returns:
            list[tuple[str, float | None]]: lista de tuplas (código da
            turma, frequência média em percentual), ordenada pelo
            código da turma. O valor é None se não houver dados
            suficientes para calcular a média.
        """
        resultado = []
        for turma in sorted(self._turmas.values(), key=lambda t: t.codigo):
            percentuais = []
            for matricula_aluno in turma.alunos_matriculados:
                aluno = self._alunos.get(matricula_aluno)
                if aluno is None:
                    continue
                percentual = aluno.calcular_percentual_frequencia(
                    turma.disciplina_codigo
                )
                if percentual is not None:
                    percentuais.append(percentual)

            if percentuais:
                media = round(sum(percentuais) / len(percentuais), 2)
            else:
                media = None

            resultado.append((turma.codigo, media))
        return resultado

    # ==================================================================
    # PERSISTÊNCIA DE DADOS
    # ==================================================================

    def salvar_dados(self):
        """Persiste todas as estruturas em memória nos arquivos JSON
        do diretório de dados.
        """
        self._persistencia.salvar(
            "alunos", [a.to_dict() for a in self._alunos.values()]
        )
        self._persistencia.salvar(
            "professores", [p.to_dict() for p in self._professores.values()]
        )
        self._persistencia.salvar(
            "disciplinas", [d.to_dict() for d in self._disciplinas.values()]
        )
        self._persistencia.salvar(
            "turmas", [t.to_dict() for t in self._turmas.values()]
        )
        self._persistencia.salvar(
            "matriculas", [m.to_dict() for m in self._matriculas.values()]
        )

    def _carregar_dados(self):
        """Carrega todas as estruturas a partir dos arquivos JSON do
        diretório de dados, reconstruindo os objetos de domínio.

        Caso seja a primeira execução do sistema (arquivos ainda não
        existem), todas as estruturas permanecem vazias.
        """
        for dados_aluno in self._persistencia.carregar("alunos"):
            aluno = Aluno.from_dict(dados_aluno)
            self._alunos[aluno.matricula] = aluno

        for dados_professor in self._persistencia.carregar("professores"):
            professor = Professor.from_dict(dados_professor)
            self._professores[professor.codigo_funcional] = professor

        for dados_disciplina in self._persistencia.carregar("disciplinas"):
            disciplina = Disciplina.from_dict(dados_disciplina)
            self._disciplinas[disciplina.codigo] = disciplina

        for dados_turma in self._persistencia.carregar("turmas"):
            turma = Turma.from_dict(dados_turma)
            self._turmas[turma.codigo] = turma

        maior_id = 0
        for dados_matricula in self._persistencia.carregar("matriculas"):
            matricula = Matricula.from_dict(dados_matricula)
            self._matriculas[matricula.id] = matricula
            maior_id = max(maior_id, matricula.id)

        self._proximo_id_matricula = maior_id + 1
