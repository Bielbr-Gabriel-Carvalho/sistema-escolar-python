"""
Módulo: usuario
----------------
Define a classe base `Usuario`, que concentra os atributos e
comportamentos comuns a todos os usuários do sistema SchoolCore.

Conceitos de Programação Orientada a Objetos aplicados:
- Encapsulamento: atributos protegidos (prefixo "_") acessados/alterados
  somente através de properties, com validação de dados.
- Construtor: valida os dados obrigatórios no momento da criação do objeto.
- Herança: serve de classe-mãe para `Aluno` e `Professor`.
"""

from utils import validar_cpf, validar_email, formatar_cpf
from excecoes import DadosInvalidosError


class Usuario:
    """Classe base que representa um usuário genérico do SchoolCore."""

    def __init__(self, nome, cpf, email=""):
        """Inicializa um novo usuário.

        Args:
            nome (str): nome completo do usuário.
            cpf (str): CPF do usuário (validado e armazenado já formatado).
            email (str, opcional): e-mail de contato do usuário.

        Raises:
            DadosInvalidosError: se o nome, CPF ou e-mail forem inválidos.
        """
        self.nome = nome
        self._cpf = self._validar_e_formatar_cpf(cpf)
        self.email = email

    # ------------------------------------------------------------------
    # Properties (encapsulamento dos atributos)
    # ------------------------------------------------------------------

    @property
    def nome(self):
        """str: nome completo do usuário."""
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor or not str(valor).strip():
            raise DadosInvalidosError("O nome não pode ser vazio.")
        self._nome = str(valor).strip()

    @property
    def cpf(self):
        """str: CPF do usuário, sempre formatado (XXX.XXX.XXX-XX)."""
        return self._cpf

    @property
    def email(self):
        """str: e-mail de contato do usuário."""
        return self._email

    @email.setter
    def email(self, valor):
        if valor and not validar_email(valor):
            raise DadosInvalidosError(f"E-mail inválido: '{valor}'.")
        self._email = valor or ""

    # ------------------------------------------------------------------
    # Métodos auxiliares
    # ------------------------------------------------------------------

    @staticmethod
    def _validar_e_formatar_cpf(cpf):
        """Valida o CPF informado e retorna sua versão formatada.

        Raises:
            DadosInvalidosError: se o CPF não for válido.
        """
        if not validar_cpf(cpf):
            raise DadosInvalidosError(f"CPF inválido: '{cpf}'.")
        return formatar_cpf(cpf)

    def to_dict(self):
        """Converte os atributos básicos do usuário em um dicionário,
        utilizado para a persistência dos dados em arquivo JSON.

        Returns:
            dict: dicionário com os dados do usuário.
        """
        return {
            "nome": self._nome,
            "cpf": self._cpf,
            "email": self._email,
        }

    def __str__(self):
        return f"{self._nome} (CPF: {self._cpf})"

    def __repr__(self):
        return f"{self.__class__.__name__}(nome={self._nome!r}, cpf={self._cpf!r})"
