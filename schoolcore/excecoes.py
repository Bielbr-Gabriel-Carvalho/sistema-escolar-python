"""
Módulo: excecoes
-----------------
Define as exceções customizadas utilizadas em todo o sistema SchoolCore.

Centralizar as exceções em um único módulo facilita o tratamento de erros
de forma específica em diferentes pontos do sistema (cadastros, matrículas,
lançamento de notas, persistência de dados, etc.), seguindo a boa prática
de criar hierarquias de exceções próprias da aplicação.
"""


class SchoolCoreError(Exception):
    """Exceção base de toda a aplicação SchoolCore.

    Todas as exceções customizadas do sistema herdam desta classe,
    permitindo capturar qualquer erro específico do domínio com
    `except SchoolCoreError`.
    """
    pass


class DadosInvalidosError(SchoolCoreError):
    """Lançada quando dados fornecidos pelo usuário são inválidos
    (ex.: CPF inválido, nota fora do intervalo permitido, e-mail malformado).
    """
    pass


class RegistroNaoEncontradoError(SchoolCoreError):
    """Lançada quando um registro (aluno, professor, disciplina, turma,
    matrícula etc.) não é encontrado no sistema.
    """
    pass


class RegistroDuplicadoError(SchoolCoreError):
    """Lançada ao tentar cadastrar um registro cuja chave (matrícula,
    código funcional, código de disciplina/turma) já existe.
    """
    pass


class MatriculaDuplicadaError(SchoolCoreError):
    """Lançada ao tentar matricular um aluno em uma turma na qual
    ele já possui matrícula ativa.
    """
    pass


class CapacidadeExcedidaError(SchoolCoreError):
    """Lançada ao tentar matricular um aluno em uma turma que já
    atingiu sua capacidade máxima de vagas.
    """
    pass


class PersistenciaError(SchoolCoreError):
    """Lançada quando ocorre um erro ao salvar ou carregar dados
    persistidos em disco (arquivos JSON).
    """
    pass
