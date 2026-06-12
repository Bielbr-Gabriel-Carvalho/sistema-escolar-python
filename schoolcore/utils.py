"""
Módulo: utils
--------------
Funções utilitárias de validação e formatação utilizadas pelas
classes de modelo (Aluno, Professor, Usuario, etc.).

Manter essas funções separadas evita duplicação de código (princípio DRY)
e facilita a reutilização e os testes unitários.
"""

import re


def validar_cpf(cpf):
    """Valida um CPF (Cadastro de Pessoa Física) utilizando o algoritmo
    oficial de cálculo dos dígitos verificadores.

    Aceita o CPF com ou sem formatação (pontos e hífen).

    Args:
        cpf (str): número do CPF a ser validado.

    Returns:
        bool: True se o CPF for válido, False caso contrário.
    """
    if cpf is None:
        return False

    cpf_numerico = re.sub(r"[^0-9]", "", str(cpf))

    if len(cpf_numerico) != 11:
        return False

    # CPFs com todos os dígitos iguais (ex.: 111.111.111-11) são inválidos
    if cpf_numerico == cpf_numerico[0] * 11:
        return False

    # Cálculo dos dois dígitos verificadores
    for posicao in range(9, 11):
        soma = sum(
            int(cpf_numerico[indice]) * ((posicao + 1) - indice)
            for indice in range(0, posicao)
        )
        digito_calculado = (soma * 10 % 11) % 10
        if digito_calculado != int(cpf_numerico[posicao]):
            return False

    return True


def formatar_cpf(cpf):
    """Formata um CPF numérico no padrão XXX.XXX.XXX-XX.

    Args:
        cpf (str): número do CPF (com ou sem formatação prévia).

    Returns:
        str: CPF formatado.
    """
    cpf_numerico = re.sub(r"[^0-9]", "", str(cpf))
    return f"{cpf_numerico[0:3]}.{cpf_numerico[3:6]}.{cpf_numerico[6:9]}-{cpf_numerico[9:11]}"


def validar_email(email):
    """Valida um endereço de e-mail por meio de expressão regular simples.

    Args:
        email (str): endereço de e-mail a ser validado.

    Returns:
        bool: True se o formato for válido, False caso contrário.
    """
    padrao = r"^[\w.\-+]+@[\w\-]+\.[\w.\-]+$"
    return re.match(padrao, str(email)) is not None


def validar_nota(nota):
    """Valida se uma nota está dentro do intervalo permitido (0 a 10).

    Args:
        nota (float): valor da nota.

    Returns:
        bool: True se a nota for válida, False caso contrário.
    """
    try:
        valor = float(nota)
    except (TypeError, ValueError):
        return False
    return 0 <= valor <= 10


def linha_separadora(caractere="-", tamanho=60):
    """Retorna uma linha separadora utilizada para formatar a saída no
    terminal (relatórios, boletins, menus, etc.).
    """
    return caractere * tamanho
