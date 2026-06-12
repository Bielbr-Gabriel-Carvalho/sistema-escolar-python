"""
Módulo: persistencia
----------------------
Define a classe `GerenciadorPersistencia`, responsável por salvar e
carregar os dados do sistema SchoolCore em arquivos no formato JSON.

Cada entidade (alunos, professores, disciplinas, turmas e matrículas)
é armazenada em um arquivo JSON próprio dentro do diretório de dados,
o que mantém a persistência simples, legível e independente de um
servidor de banco de dados externo (atendendo ao requisito de
"persistência de dados" da disciplina de Programação de Computadores).
"""

import json
import os

from excecoes import PersistenciaError


class GerenciadorPersistencia:
    """Gerencia a leitura e a escrita dos dados do sistema em arquivos JSON."""

    def __init__(self, diretorio_dados="dados"):
        """Inicializa o gerenciador de persistência.

        Args:
            diretorio_dados (str): caminho do diretório onde os arquivos
                JSON serão armazenados. É criado automaticamente caso
                não exista.
        """
        self._diretorio_dados = diretorio_dados
        try:
            os.makedirs(self._diretorio_dados, exist_ok=True)
        except OSError as erro:
            raise PersistenciaError(
                f"Não foi possível criar o diretório de dados "
                f"'{self._diretorio_dados}': {erro}"
            )

    def _caminho_arquivo(self, nome_arquivo):
        """Monta o caminho completo de um arquivo JSON dentro do
        diretório de dados.
        """
        return os.path.join(self._diretorio_dados, f"{nome_arquivo}.json")

    def salvar(self, nome_arquivo, dados):
        """Salva uma lista de dicionários em um arquivo JSON.

        Args:
            nome_arquivo (str): nome do arquivo (sem extensão), ex.:
                "alunos", "professores", "disciplinas", "turmas",
                "matriculas".
            dados (list): lista de dicionários a serem persistidos.

        Raises:
            PersistenciaError: se ocorrer algum erro de escrita em disco.
        """
        caminho = self._caminho_arquivo(nome_arquivo)
        try:
            with open(caminho, "w", encoding="utf-8") as arquivo:
                json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        except (IOError, OSError, TypeError) as erro:
            raise PersistenciaError(
                f"Erro ao salvar dados em '{caminho}': {erro}"
            )

    def carregar(self, nome_arquivo):
        """Carrega uma lista de dicionários a partir de um arquivo JSON.

        Args:
            nome_arquivo (str): nome do arquivo (sem extensão).

        Returns:
            list: lista de dicionários carregados. Retorna uma lista
            vazia caso o arquivo ainda não exista (primeira execução
            do sistema).

        Raises:
            PersistenciaError: se o arquivo existir, mas não puder ser
                lido ou estiver com conteúdo corrompido.
        """
        caminho = self._caminho_arquivo(nome_arquivo)
        if not os.path.exists(caminho):
            return []

        try:
            with open(caminho, "r", encoding="utf-8") as arquivo:
                conteudo = json.load(arquivo)
                if not isinstance(conteudo, list):
                    raise PersistenciaError(
                        f"O arquivo '{caminho}' não contém uma lista válida."
                    )
                return conteudo
        except (IOError, OSError) as erro:
            raise PersistenciaError(f"Erro ao ler o arquivo '{caminho}': {erro}")
        except json.JSONDecodeError as erro:
            raise PersistenciaError(
                f"O arquivo '{caminho}' está corrompido e não pôde "
                f"ser interpretado como JSON: {erro}"
            )
