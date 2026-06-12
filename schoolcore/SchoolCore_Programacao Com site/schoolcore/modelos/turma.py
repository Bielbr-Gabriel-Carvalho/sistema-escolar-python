"""
Módulo: turma
--------------
Define a classe `Turma`, que representa uma turma vinculada a uma
disciplina, um professor e um conjunto de alunos matriculados,
respeitando um limite de capacidade de vagas.
"""

from excecoes import DadosInvalidosError, CapacidadeExcedidaError


class Turma:
    """Representa uma turma de uma disciplina, com controle de vagas."""

    def __init__(self, codigo, disciplina_codigo, professor_codigo, capacidade):
        """Inicializa uma nova turma.

        Args:
            codigo (str): código único da turma (ex.: "T2026-1-ALG101-A").
            disciplina_codigo (str): código da disciplina associada.
            professor_codigo (str | None): código funcional do professor
                responsável pela turma.
            capacidade (int): número máximo de alunos na turma.

        Raises:
            DadosInvalidosError: se algum dado obrigatório for inválido.
        """
        if not codigo or not str(codigo).strip():
            raise DadosInvalidosError("O código da turma não pode ser vazio.")
        if not disciplina_codigo or not str(disciplina_codigo).strip():
            raise DadosInvalidosError("A disciplina da turma não pode ser vazia.")

        self._codigo = str(codigo).strip().upper()
        self._disciplina_codigo = str(disciplina_codigo).strip().upper()
        self.professor_codigo = professor_codigo
        self.capacidade = capacidade

        # Lista de matrículas (números de matrícula dos alunos) com vínculo
        # ativo nesta turma.
        self._alunos_matriculados = []

    # ------------------------------------------------------------------
    # Properties (encapsulamento)
    # ------------------------------------------------------------------

    @property
    def codigo(self):
        """str: código único da turma (não pode ser alterado)."""
        return self._codigo

    @property
    def disciplina_codigo(self):
        """str: código da disciplina associada à turma."""
        return self._disciplina_codigo

    @property
    def professor_codigo(self):
        """str | None: código funcional do professor responsável."""
        return self._professor_codigo

    @professor_codigo.setter
    def professor_codigo(self, valor):
        self._professor_codigo = valor if valor else None

    @property
    def capacidade(self):
        """int: número máximo de alunos permitidos na turma."""
        return self._capacidade

    @capacidade.setter
    def capacidade(self, valor):
        try:
            valor_int = int(valor)
        except (TypeError, ValueError):
            raise DadosInvalidosError("A capacidade deve ser um número inteiro.")
        if valor_int <= 0:
            raise DadosInvalidosError("A capacidade deve ser maior que zero.")
        self._capacidade = valor_int

    @property
    def alunos_matriculados(self):
        """list[str]: lista de matrículas dos alunos vinculados à turma."""
        return self._alunos_matriculados

    @property
    def vagas_disponiveis(self):
        """int: número de vagas ainda disponíveis na turma."""
        return self._capacidade - len(self._alunos_matriculados)

    # ------------------------------------------------------------------
    # Métodos de negócio
    # ------------------------------------------------------------------

    def adicionar_aluno(self, matricula_aluno):
        """Adiciona um aluno à turma, respeitando o limite de capacidade.

        Args:
            matricula_aluno (str): matrícula do aluno a ser adicionado.

        Raises:
            CapacidadeExcedidaError: se a turma já estiver cheia.
        """
        if matricula_aluno in self._alunos_matriculados:
            return  # já está matriculado: operação idempotente
        if self.vagas_disponiveis <= 0:
            raise CapacidadeExcedidaError(
                f"A turma '{self._codigo}' já atingiu a capacidade máxima "
                f"de {self._capacidade} aluno(s)."
            )
        self._alunos_matriculados.append(matricula_aluno)

    def remover_aluno(self, matricula_aluno):
        """Remove o vínculo de um aluno com a turma, caso exista.

        Args:
            matricula_aluno (str): matrícula do aluno a ser removido.
        """
        if matricula_aluno in self._alunos_matriculados:
            self._alunos_matriculados.remove(matricula_aluno)

    # ------------------------------------------------------------------
    # Persistência
    # ------------------------------------------------------------------

    def to_dict(self):
        """Converte a turma em um dicionário para persistência em JSON."""
        return {
            "codigo": self._codigo,
            "disciplina_codigo": self._disciplina_codigo,
            "professor_codigo": self._professor_codigo,
            "capacidade": self._capacidade,
            "alunos_matriculados": self._alunos_matriculados,
        }

    @classmethod
    def from_dict(cls, dados):
        """Reconstrói um objeto `Turma` a partir de um dicionário lido
        de um arquivo JSON.
        """
        turma = cls(
            codigo=dados["codigo"],
            disciplina_codigo=dados["disciplina_codigo"],
            professor_codigo=dados.get("professor_codigo"),
            capacidade=dados["capacidade"],
        )
        turma._alunos_matriculados = dados.get("alunos_matriculados", [])
        return turma

    def __str__(self):
        return (f"Turma {self._codigo} | Disciplina: {self._disciplina_codigo} | "
                f"Professor: {self._professor_codigo or 'não definido'} | "
                f"Vagas: {len(self._alunos_matriculados)}/{self._capacidade}")
