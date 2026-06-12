"""
Módulo: matricula
------------------
Define a classe `Matricula`, que representa o vínculo acadêmico entre
um aluno e uma turma, incluindo a data da matrícula e seu status
(ativa ou cancelada).
"""

from datetime import datetime

from excecoes import DadosInvalidosError

STATUS_VALIDOS = {"ativa", "cancelada"}


class Matricula:
    """Representa a matrícula de um aluno em uma turma."""

    def __init__(self, id_matricula, matricula_aluno, codigo_turma,
                 data_matricula=None, status="ativa"):
        """Inicializa uma nova matrícula.

        Args:
            id_matricula (int): identificador único da matrícula,
                gerado automaticamente pelo sistema.
            matricula_aluno (str): matrícula do aluno vinculado.
            codigo_turma (str): código da turma vinculada.
            data_matricula (str, opcional): data da matrícula no formato
                DD/MM/AAAA. Se não informada, utiliza a data atual.
            status (str, opcional): status da matrícula ("ativa" ou
                "cancelada").

        Raises:
            DadosInvalidosError: se algum dado obrigatório for inválido.
        """
        if not matricula_aluno or not str(matricula_aluno).strip():
            raise DadosInvalidosError("A matrícula do aluno não pode ser vazia.")
        if not codigo_turma or not str(codigo_turma).strip():
            raise DadosInvalidosError("O código da turma não pode ser vazio.")

        self._id = int(id_matricula)
        self._matricula_aluno = str(matricula_aluno).strip()
        self._codigo_turma = str(codigo_turma).strip().upper()
        self._data_matricula = data_matricula or datetime.now().strftime("%d/%m/%Y")
        self.status = status

    # ------------------------------------------------------------------
    # Properties (encapsulamento)
    # ------------------------------------------------------------------

    @property
    def id(self):
        """int: identificador único da matrícula."""
        return self._id

    @property
    def matricula_aluno(self):
        """str: matrícula do aluno vinculado a este registro."""
        return self._matricula_aluno

    @property
    def codigo_turma(self):
        """str: código da turma vinculada a este registro."""
        return self._codigo_turma

    @property
    def data_matricula(self):
        """str: data em que a matrícula foi realizada (DD/MM/AAAA)."""
        return self._data_matricula

    @property
    def status(self):
        """str: status atual da matrícula ('ativa' ou 'cancelada')."""
        return self._status

    @status.setter
    def status(self, valor):
        valor_normalizado = str(valor).strip().lower()
        if valor_normalizado not in STATUS_VALIDOS:
            raise DadosInvalidosError(
                f"Status de matrícula inválido: '{valor}'. "
                f"Valores aceitos: {', '.join(sorted(STATUS_VALIDOS))}."
            )
        self._status = valor_normalizado

    # ------------------------------------------------------------------
    # Métodos de negócio
    # ------------------------------------------------------------------

    def cancelar(self):
        """Marca esta matrícula como cancelada."""
        self._status = "cancelada"

    def esta_ativa(self):
        """bool: True se a matrícula estiver com status 'ativa'."""
        return self._status == "ativa"

    # ------------------------------------------------------------------
    # Persistência
    # ------------------------------------------------------------------

    def to_dict(self):
        """Converte a matrícula em um dicionário para persistência em JSON."""
        return {
            "id": self._id,
            "matricula_aluno": self._matricula_aluno,
            "codigo_turma": self._codigo_turma,
            "data_matricula": self._data_matricula,
            "status": self._status,
        }

    @classmethod
    def from_dict(cls, dados):
        """Reconstrói um objeto `Matricula` a partir de um dicionário
        lido de um arquivo JSON.
        """
        return cls(
            id_matricula=dados["id"],
            matricula_aluno=dados["matricula_aluno"],
            codigo_turma=dados["codigo_turma"],
            data_matricula=dados.get("data_matricula"),
            status=dados.get("status", "ativa"),
        )

    def __str__(self):
        return (f"Matrícula #{self._id} | Aluno: {self._matricula_aluno} | "
                f"Turma: {self._codigo_turma} | Data: {self._data_matricula} | "
                f"Status: {self._status}")
