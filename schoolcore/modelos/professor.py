"""
Módulo: professor
------------------
Define a classe `Professor`, que herda de `Usuario` e representa um
docente da instituição Centro Educacional Horizonte do Saber.
"""

from modelos.usuario import Usuario
from excecoes import DadosInvalidosError

TITULACOES_VALIDAS = {
    "graduado", "especialista", "mestre", "doutor", "pós-doutor"
}


class Professor(Usuario):
    """Representa um professor vinculado à instituição."""

    def __init__(self, codigo_funcional, nome, cpf, titulacao,
                 area_atuacao, email=""):
        """Inicializa um novo professor.

        Args:
            codigo_funcional (str): código funcional único do professor.
            nome (str): nome completo do professor.
            cpf (str): CPF do professor.
            titulacao (str): titulação acadêmica (graduado, especialista,
                mestre, doutor ou pós-doutor).
            area_atuacao (str): área de atuação/especialização do professor.
            email (str, opcional): e-mail de contato.

        Raises:
            DadosInvalidosError: se algum dado obrigatório for inválido.
        """
        super().__init__(nome, cpf, email)

        if not codigo_funcional or not str(codigo_funcional).strip():
            raise DadosInvalidosError(
                "O código funcional do professor não pode ser vazio."
            )
        if not area_atuacao or not str(area_atuacao).strip():
            raise DadosInvalidosError("A área de atuação não pode ser vazia.")

        self._codigo_funcional = str(codigo_funcional).strip()
        self.titulacao = titulacao
        self._area_atuacao = str(area_atuacao).strip()

        # Lista de códigos das disciplinas vinculadas a este professor
        self._disciplinas_vinculadas = []

    # ------------------------------------------------------------------
    # Properties (encapsulamento)
    # ------------------------------------------------------------------

    @property
    def codigo_funcional(self):
        """str: código funcional único do professor (não pode ser alterado)."""
        return self._codigo_funcional

    @property
    def titulacao(self):
        """str: titulação acadêmica do professor."""
        return self._titulacao

    @titulacao.setter
    def titulacao(self, valor):
        valor_normalizado = str(valor).strip().lower()
        if valor_normalizado not in TITULACOES_VALIDAS:
            raise DadosInvalidosError(
                f"Titulação inválida: '{valor}'. "
                f"Valores aceitos: {', '.join(sorted(TITULACOES_VALIDAS))}."
            )
        self._titulacao = valor_normalizado

    @property
    def area_atuacao(self):
        """str: área de atuação/especialização do professor."""
        return self._area_atuacao

    @property
    def disciplinas_vinculadas(self):
        """list[str]: lista de códigos das disciplinas vinculadas
        a este professor.
        """
        return self._disciplinas_vinculadas

    # ------------------------------------------------------------------
    # Métodos de negócio
    # ------------------------------------------------------------------

    def vincular_disciplina(self, codigo_disciplina):
        """Vincula uma disciplina a este professor, evitando duplicidade.

        Args:
            codigo_disciplina (str): código da disciplina a ser vinculada.
        """
        if codigo_disciplina not in self._disciplinas_vinculadas:
            self._disciplinas_vinculadas.append(codigo_disciplina)

    def desvincular_disciplina(self, codigo_disciplina):
        """Remove o vínculo de uma disciplina deste professor, caso exista.

        Args:
            codigo_disciplina (str): código da disciplina a ser desvinculada.
        """
        if codigo_disciplina in self._disciplinas_vinculadas:
            self._disciplinas_vinculadas.remove(codigo_disciplina)

    # ------------------------------------------------------------------
    # Persistência
    # ------------------------------------------------------------------

    def to_dict(self):
        """Converte o professor em um dicionário para persistência em JSON."""
        dados = super().to_dict()
        dados.update({
            "codigo_funcional": self._codigo_funcional,
            "titulacao": self._titulacao,
            "area_atuacao": self._area_atuacao,
            "disciplinas_vinculadas": self._disciplinas_vinculadas,
        })
        return dados

    @classmethod
    def from_dict(cls, dados):
        """Reconstrói um objeto `Professor` a partir de um dicionário
        lido de um arquivo JSON.
        """
        professor = cls(
            codigo_funcional=dados["codigo_funcional"],
            nome=dados["nome"],
            cpf=dados["cpf"],
            titulacao=dados["titulacao"],
            area_atuacao=dados["area_atuacao"],
            email=dados.get("email", ""),
        )
        professor._disciplinas_vinculadas = dados.get("disciplinas_vinculadas", [])
        return professor

    def __str__(self):
        return (f"Professor {self._codigo_funcional} - {self._nome} | "
                f"Titulação: {self._titulacao} | Área: {self._area_atuacao}")
