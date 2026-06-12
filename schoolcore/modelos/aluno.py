"""
Módulo: aluno
--------------
Define a classe `Aluno`, que herda de `Usuario` e representa um estudante
da instituição Centro Educacional Horizonte do Saber.

Além dos dados cadastrais, a classe é responsável por gerenciar:
- lançamento de notas parciais e finais por disciplina;
- cálculo automático da média;
- registro de frequência (presenças/faltas) por disciplina;
- cálculo do percentual de frequência;
- emissão do boletim (situação final do aluno em cada disciplina).
"""

from modelos.usuario import Usuario
from utils import validar_nota
from excecoes import DadosInvalidosError

# Constantes de regras de negócio acadêmicas
MEDIA_MINIMA_APROVACAO = 6.0
FREQUENCIA_MINIMA_APROVACAO = 75.0  # em percentual

STATUS_VALIDOS = {"ativo", "trancado", "formado", "inativo"}


class Aluno(Usuario):
    """Representa um aluno matriculado em um curso da instituição."""

    def __init__(self, matricula, nome, cpf, data_nascimento, curso,
                 periodo, status_academico="ativo", email=""):
        """Inicializa um novo aluno.

        Args:
            matricula (str): número de matrícula único do aluno.
            nome (str): nome completo do aluno.
            cpf (str): CPF do aluno.
            data_nascimento (str): data de nascimento no formato DD/MM/AAAA.
            curso (str): nome do curso ao qual o aluno está vinculado.
            periodo (int): período/semestre atual do aluno.
            status_academico (str, opcional): situação acadêmica
                ("ativo", "trancado", "formado" ou "inativo").
            email (str, opcional): e-mail de contato do aluno.

        Raises:
            DadosInvalidosError: se algum dado obrigatório for inválido.
        """
        super().__init__(nome, cpf, email)

        if not matricula or not str(matricula).strip():
            raise DadosInvalidosError("A matrícula do aluno não pode ser vazia.")
        if not curso or not str(curso).strip():
            raise DadosInvalidosError("O curso do aluno não pode ser vazio.")

        self._matricula = str(matricula).strip()
        self._data_nascimento = self._validar_data_nascimento(data_nascimento)
        self._curso = str(curso).strip()
        self.periodo = periodo
        self.status_academico = status_academico

        # Estruturas internas para notas e frequência, organizadas por
        # código de disciplina:
        #   notas[cod_disciplina] = {"parciais": [..], "final": float|None}
        #   frequencias[cod_disciplina] = {"presencas": int, "faltas": int}
        self._notas = {}
        self._frequencias = {}

    # ------------------------------------------------------------------
    # Properties (encapsulamento)
    # ------------------------------------------------------------------

    @property
    def matricula(self):
        """str: número de matrícula único do aluno (não pode ser alterado)."""
        return self._matricula

    @property
    def data_nascimento(self):
        """str: data de nascimento no formato DD/MM/AAAA."""
        return self._data_nascimento

    @property
    def curso(self):
        """str: curso ao qual o aluno está vinculado."""
        return self._curso

    @property
    def periodo(self):
        """int: período/semestre atual do aluno."""
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
    def status_academico(self):
        """str: situação acadêmica do aluno."""
        return self._status_academico

    @status_academico.setter
    def status_academico(self, valor):
        valor = str(valor).strip().lower()
        if valor not in STATUS_VALIDOS:
            raise DadosInvalidosError(
                f"Status acadêmico inválido: '{valor}'. "
                f"Valores aceitos: {', '.join(sorted(STATUS_VALIDOS))}."
            )
        self._status_academico = valor

    @property
    def notas(self):
        """dict: estrutura completa de notas do aluno por disciplina."""
        return self._notas

    @property
    def frequencias(self):
        """dict: estrutura completa de frequência do aluno por disciplina."""
        return self._frequencias

    # ------------------------------------------------------------------
    # Validações específicas
    # ------------------------------------------------------------------

    @staticmethod
    def _validar_data_nascimento(data_nascimento):
        """Valida o formato DD/MM/AAAA da data de nascimento."""
        from datetime import datetime
        try:
            datetime.strptime(str(data_nascimento), "%d/%m/%Y")
        except ValueError:
            raise DadosInvalidosError(
                f"Data de nascimento inválida: '{data_nascimento}'. "
                "Utilize o formato DD/MM/AAAA."
            )
        return str(data_nascimento)

    # ------------------------------------------------------------------
    # Registro de notas
    # ------------------------------------------------------------------

    def _garantir_disciplina_em_notas(self, codigo_disciplina):
        if codigo_disciplina not in self._notas:
            self._notas[codigo_disciplina] = {"parciais": [], "final": None}

    def lancar_nota_parcial(self, codigo_disciplina, nota):
        """Lança uma nota parcial do aluno em uma disciplina.

        Args:
            codigo_disciplina (str): código da disciplina.
            nota (float): valor da nota parcial (0 a 10).

        Raises:
            DadosInvalidosError: se a nota estiver fora do intervalo 0-10.
        """
        if not validar_nota(nota):
            raise DadosInvalidosError("A nota deve estar entre 0 e 10.")
        self._garantir_disciplina_em_notas(codigo_disciplina)
        self._notas[codigo_disciplina]["parciais"].append(float(nota))

    def lancar_nota_final(self, codigo_disciplina, nota):
        """Lança a nota final do aluno em uma disciplina.

        Args:
            codigo_disciplina (str): código da disciplina.
            nota (float): valor da nota final (0 a 10).

        Raises:
            DadosInvalidosError: se a nota estiver fora do intervalo 0-10.
        """
        if not validar_nota(nota):
            raise DadosInvalidosError("A nota deve estar entre 0 e 10.")
        self._garantir_disciplina_em_notas(codigo_disciplina)
        self._notas[codigo_disciplina]["final"] = float(nota)

    def calcular_media(self, codigo_disciplina):
        """Calcula a média final do aluno em uma disciplina.

        A média é calculada considerando a média aritmética das notas
        parciais com peso 1 e a nota final com peso 1 (ponderação simples
        e transparente, adequada ao escopo do projeto acadêmico).

        Args:
            codigo_disciplina (str): código da disciplina.

        Returns:
            float | None: a média calculada, arredondada para 2 casas
            decimais, ou None caso ainda não existam notas suficientes.
        """
        registro = self._notas.get(codigo_disciplina)
        if not registro:
            return None

        parciais = registro["parciais"]
        final = registro["final"]

        valores = list(parciais)
        if final is not None:
            valores.append(final)

        if not valores:
            return None

        media = sum(valores) / len(valores)
        return round(media, 2)

    # ------------------------------------------------------------------
    # Registro de frequência
    # ------------------------------------------------------------------

    def _garantir_disciplina_em_frequencia(self, codigo_disciplina):
        if codigo_disciplina not in self._frequencias:
            self._frequencias[codigo_disciplina] = {"presencas": 0, "faltas": 0}

    def registrar_frequencia(self, codigo_disciplina, presente):
        """Registra a presença ou a falta do aluno em uma aula.

        Args:
            codigo_disciplina (str): código da disciplina.
            presente (bool): True para presença, False para falta.
        """
        self._garantir_disciplina_em_frequencia(codigo_disciplina)
        if presente:
            self._frequencias[codigo_disciplina]["presencas"] += 1
        else:
            self._frequencias[codigo_disciplina]["faltas"] += 1

    def calcular_percentual_frequencia(self, codigo_disciplina):
        """Calcula o percentual de frequência do aluno em uma disciplina.

        Args:
            codigo_disciplina (str): código da disciplina.

        Returns:
            float | None: percentual de frequência (0 a 100), arredondado
            para 2 casas decimais, ou None se não houver registros.
        """
        registro = self._frequencias.get(codigo_disciplina)
        if not registro:
            return None

        total_aulas = registro["presencas"] + registro["faltas"]
        if total_aulas == 0:
            return None

        percentual = (registro["presencas"] / total_aulas) * 100
        return round(percentual, 2)

    # ------------------------------------------------------------------
    # Boletim / situação final
    # ------------------------------------------------------------------

    def situacao_final(self, codigo_disciplina):
        """Determina a situação final do aluno em uma disciplina.

        A regra de negócio considera o aluno aprovado se a média for
        maior ou igual a 6.0 (MEDIA_MINIMA_APROVACAO) E o percentual de
        frequência for maior ou igual a 75% (FREQUENCIA_MINIMA_APROVACAO).

        Args:
            codigo_disciplina (str): código da disciplina.

        Returns:
            str: "Aprovado", "Reprovado por nota", "Reprovado por
            frequência", "Reprovado por nota e frequência" ou
            "Sem dados suficientes".
        """
        media = self.calcular_media(codigo_disciplina)
        frequencia = self.calcular_percentual_frequencia(codigo_disciplina)

        if media is None or frequencia is None:
            return "Sem dados suficientes"

        aprovado_por_nota = media >= MEDIA_MINIMA_APROVACAO
        aprovado_por_frequencia = frequencia >= FREQUENCIA_MINIMA_APROVACAO

        if aprovado_por_nota and aprovado_por_frequencia:
            return "Aprovado"
        if not aprovado_por_nota and not aprovado_por_frequencia:
            return "Reprovado por nota e frequência"
        if not aprovado_por_nota:
            return "Reprovado por nota"
        return "Reprovado por frequência"

    def emitir_boletim(self):
        """Gera o boletim completo do aluno, com média, frequência e
        situação final em cada disciplina cursada.

        Returns:
            list[dict]: lista de dicionários, um para cada disciplina,
            contendo código da disciplina, média, frequência e situação.
        """
        codigos = set(self._notas.keys()) | set(self._frequencias.keys())
        boletim = []
        for codigo in sorted(codigos):
            boletim.append({
                "codigo_disciplina": codigo,
                "media": self.calcular_media(codigo),
                "frequencia": self.calcular_percentual_frequencia(codigo),
                "situacao": self.situacao_final(codigo),
            })
        return boletim

    # ------------------------------------------------------------------
    # Persistência
    # ------------------------------------------------------------------

    def to_dict(self):
        """Converte o aluno (incluindo notas e frequências) em um
        dicionário, para ser salvo em arquivo JSON.
        """
        dados = super().to_dict()
        dados.update({
            "matricula": self._matricula,
            "data_nascimento": self._data_nascimento,
            "curso": self._curso,
            "periodo": self._periodo,
            "status_academico": self._status_academico,
            "notas": self._notas,
            "frequencias": self._frequencias,
        })
        return dados

    @classmethod
    def from_dict(cls, dados):
        """Reconstrói um objeto `Aluno` a partir de um dicionário lido
        de um arquivo JSON.
        """
        aluno = cls(
            matricula=dados["matricula"],
            nome=dados["nome"],
            cpf=dados["cpf"],
            data_nascimento=dados["data_nascimento"],
            curso=dados["curso"],
            periodo=dados["periodo"],
            status_academico=dados.get("status_academico", "ativo"),
            email=dados.get("email", ""),
        )
        aluno._notas = dados.get("notas", {})
        aluno._frequencias = dados.get("frequencias", {})
        return aluno

    def __str__(self):
        return (f"Aluno {self._matricula} - {self._nome} | "
                f"Curso: {self._curso} | Período: {self._periodo} | "
                f"Status: {self._status_academico}")
