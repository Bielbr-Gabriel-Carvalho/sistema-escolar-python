"""
Pacote: modelos
----------------
Contém as classes de domínio (entidades) do sistema SchoolCore:

- Usuario   : classe base para Aluno e Professor (herança)
- Aluno     : representa um estudante da instituição
- Professor : representa um docente da instituição
- Disciplina: representa uma disciplina do currículo
- Turma     : representa uma turma de uma disciplina em um período
- Matricula : representa o vínculo entre um aluno e uma turma
"""

from modelos.usuario import Usuario
from modelos.aluno import Aluno
from modelos.professor import Professor
from modelos.disciplina import Disciplina
from modelos.turma import Turma
from modelos.matricula import Matricula

__all__ = [
    "Usuario",
    "Aluno",
    "Professor",
    "Disciplina",
    "Turma",
    "Matricula",
]
