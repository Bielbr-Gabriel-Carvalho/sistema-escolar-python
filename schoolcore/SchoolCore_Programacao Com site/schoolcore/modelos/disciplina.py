"""
Módulo: disciplina
-------------------
Define a classe `Disciplina`, que representa uma disciplina do currículo
acadêmico oferecida pela instituição.
"""

from excecoes import DadosInvalidosError


class Disciplina:
    """Representa uma disciplina do currículo acadêmico."""

    def __init__(self, codigo, nome, carga_horaria, periodo,
                 professor_responsavel=None):
        """Inicializa uma nova disciplina.

        Args:
            codigo (str): código único da disciplina (ex.: "ALG101").
            nome (str): nome da disciplina.
            carga_horaria (int): carga horária total, em horas.
            periodo (int): período/semestre em que a disciplina é oferecida.
            professor_responsavel (str | None, opcional): código funcional
                do professor responsável pela disciplina.

        Raises:
            DadosInvalidosError: se algum dado obrigatório for inválido.
        """
        if not codigo or not str(codigo).strip():
            raise DadosInvalidosError("O código da disciplina não pode ser vazio.")
        if not nome or not str(nome).strip():
            raise DadosInvalidosError("O nome da disciplina não pode ser vazio.")

        self._codigo = str(codigo).strip().upper()
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.periodo = periodo
        self.professor_responsavel = professor_responsavel

    # ------------------------------------------------------------------
    # Properties (encapsulamento)
    # ------------------------------------------------------------------

    @property
    def codigo(self):
        """str: código único da disciplina (não pode ser alterado)."""
        return self._codigo

    @property
    def nome(self):
        """str: nome da disciplina."""
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor or not str(valor).strip():
            raise DadosInvalidosError("O nome da disciplina não pode ser vazio.")
        self._nome = str(valor).strip()

    @property
    def carga_horaria(self):
        """int: carga horária total da disciplina, em horas."""
        return self._carga_horaria

    @carga_horaria.setter
    def carga_horaria(self, valor):
        try:
            valor_int = int(valor)
        except (TypeError, ValueError):
            raise DadosInvalidosError("A carga horária deve ser um número inteiro.")
        if valor_int <= 0:
            raise DadosInvalidosError("A carga horária deve ser maior que zero.")
        self._carga_horaria = valor_int

    @property
    def periodo(self):
        """int: período/semestre em que a disciplina é oferecida."""
        return self._periodo

    @periodo.setter
    def periodo(self, valor):
        try:
            valor_int = int(valor)
        except (TypeError, ValueError):
            raise DadosInvalidosError("O período deve ser um número inteiro.")
        if valor_int <= 0:
            raise DadosInvalidosError("O período deve ser maior que zero.")
        self._periodo = valor_int

    @property
    def professor_responsavel(self):
        """str | None: código funcional do professor responsável."""
        return self._professor_responsavel

    @professor_responsavel.setter
    def professor_responsavel(self, valor):
        self._professor_responsavel = valor if valor else None

    # ------------------------------------------------------------------
    # Persistência
    # ------------------------------------------------------------------

    def to_dict(self):
        """Converte a disciplina em um dicionário para persistência em JSON."""
        return {
            "codigo": self._codigo,
            "nome": self._nome,
            "carga_horaria": self._carga_horaria,
            "periodo": self._periodo,
            "professor_responsavel": self._professor_responsavel,
        }

    @classmethod
    def from_dict(cls, dados):
        """Reconstrói um objeto `Disciplina` a partir de um dicionário
        lido de um arquivo JSON.
        """
        return cls(
            codigo=dados["codigo"],
            nome=dados["nome"],
            carga_horaria=dados["carga_horaria"],
            periodo=dados["periodo"],
            professor_responsavel=dados.get("professor_responsavel"),
        )

    def __str__(self):
        responsavel = self._professor_responsavel or "não definido"
        return (f"Disciplina {self._codigo} - {self._nome} | "
                f"CH: {self._carga_horaria}h | Período: {self._periodo} | "
                f"Professor responsável: {responsavel}")
