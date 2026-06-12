# SchoolCore — Módulo de Programação de Computadores

Sistema acadêmico desenvolvido em **Python**, utilizando **Programação
Orientada a Objetos**, no contexto do Projeto Integrador SchoolCore
(semestre 2026.1), referente à disciplina **Programação de Computadores**.

## 1. Objetivo

Implementar, em Python, a camada de software responsável pelo
gerenciamento básico das operações acadêmicas da instituição fictícia
*Centro Educacional Horizonte do Saber*, conforme especificado na
solicitação do cliente do projeto SchoolCore.

## 2. Estrutura do projeto

```
schoolcore/
├── main.py                # Interface de linha de comando (menu principal)
├── sistema.py              # Classe SistemaSchoolCore (regras de negócio)
├── persistencia.py          # Persistência dos dados em arquivos JSON
├── excecoes.py              # Exceções customizadas do sistema
├── utils.py                 # Funções utilitárias (validação de CPF, e-mail, etc.)
├── testes_sistema.py        # Script de testes automatizados de demonstração
├── modelos/
│   ├── __init__.py
│   ├── usuario.py            # Classe base Usuario (herança)
│   ├── aluno.py               # Classe Aluno (notas, frequência, boletim)
│   ├── professor.py           # Classe Professor
│   ├── disciplina.py          # Classe Disciplina
│   ├── turma.py                # Classe Turma (controle de vagas)
│   └── matricula.py            # Classe Matricula
└── dados/                     # Gerado automaticamente: arquivos JSON persistidos
```

## 3. Conceitos de Orientação a Objetos aplicados

- **Encapsulamento**: todos os atributos são protegidos (prefixo `_`) e
  acessados/alterados por meio de *properties*, com validação de dados
  (ex.: CPF, e-mail, notas, capacidade de turma).
- **Construtores**: cada classe valida seus dados obrigatórios no
  momento da criação do objeto, lançando exceções customizadas em caso
  de erro.
- **Herança**: `Aluno` e `Professor` herdam de `Usuario`, reaproveitando
  atributos e comportamentos comuns (nome, CPF, e-mail).
- **Tratamento de exceções**: hierarquia própria de exceções
  (`excecoes.py`), todas derivadas de `SchoolCoreError`, capturadas e
  tratadas de forma amigável na interface de linha de comando.
- **Persistência de dados**: cada entidade é salva em um arquivo JSON
  individual dentro da pasta `dados/`, recarregado automaticamente na
  inicialização do sistema.

## 4. Funcionalidades implementadas

### Gestão de Alunos
Cadastrar, consultar, listar, atualizar e excluir/inativar alunos.

### Gestão de Professores
Cadastrar, consultar, listar e atualizar professores, com vínculo a
disciplinas.

### Gestão de Disciplinas
Cadastrar, listar e vincular/alterar o professor responsável por uma
disciplina.

### Gestão de Turmas
Criar e listar turmas, com controle automático de capacidade de vagas.

### Matrículas
Realizar matrícula, cancelar matrícula, consultar histórico e impedir
matrícula duplicada (mesmo aluno na mesma turma).

### Módulo Acadêmico
Lançamento de notas parciais e finais com cálculo automático de média,
registro de presença/falta com cálculo de percentual de frequência, e
emissão de boletim com situação final (Aprovado / Reprovado por nota /
Reprovado por frequência / Reprovado por nota e frequência).

### Módulo Gerencial
Relatórios de quantidade de alunos matriculados, disciplinas mais
ofertadas, professores ativos, alunos aprovados/reprovados e frequência
média por turma.

## 5. Como executar

Requisitos: **Python 3.10+** (não são necessárias bibliotecas externas).

```bash
cd schoolcore
python main.py
```

Para executar os testes automatizados de demonstração:

```bash
python testes_sistema.py
```

## 6. Regras de negócio principais

- Um aluno só é considerado **Aprovado** em uma disciplina se obtiver
  média ≥ 6,0 **e** frequência ≥ 75%.
- A média da disciplina é calculada pela média aritmética simples entre
  as notas parciais lançadas e a nota final (quando informada).
- Não é permitida matrícula duplicada (mesmo aluno, mesma turma, com
  matrícula ativa).
- Toda turma possui um limite de capacidade de vagas, que não pode ser
  excedido ao realizar novas matrículas.
- Ao excluir um aluno, o padrão do sistema é **inativá-lo**
  (status = "inativo"), preservando seu histórico acadêmico; a exclusão
  definitiva é uma opção alternativa.

## 7. Possíveis evoluções futuras

- Substituição da camada de persistência em JSON pela integração com
  MongoDB (via PyMongo), conforme especificado para a disciplina de
  Laboratório de Banco de Dados.
- Construção de uma interface gráfica ou web, consumindo as mesmas
  classes de `sistema.py` e `modelos/`.
- Implementação de autenticação de usuários (login/senha) para os
  diferentes perfis (secretaria, professores, coordenação).
