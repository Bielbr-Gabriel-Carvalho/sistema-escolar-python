# SchoolCore 

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
├── app.py                  # Aplicação web (Flask) — site completo
├── main.py                  # Interface de linha de comando (menu principal)
├── sistema.py                # Classe SistemaSchoolCore (regras de negócio)
├── persistencia.py            # Persistência dos dados em arquivos JSON
├── excecoes.py                # Exceções customizadas do sistema
├── utils.py                    # Funções utilitárias (validação de CPF, e-mail, etc.)
├── testes_sistema.py            # Script de testes automatizados de demonstração
├── modelos/
│   ├── __init__.py
│   ├── usuario.py                # Classe base Usuario (herança)
│   ├── aluno.py                   # Classe Aluno (notas, frequência, boletim)
│   ├── professor.py               # Classe Professor
│   ├── disciplina.py              # Classe Disciplina
│   ├── turma.py                    # Classe Turma (controle de vagas)
│   └── matricula.py                # Classe Matricula
├── templates/                    # Páginas HTML (Jinja2) do site
├── static/css/style.css           # Estilo visual do site
└── dados/                          # Gerado automaticamente: arquivos JSON persistidos
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

Requisitos: **Python 3.10+**.

### 5.1 Versão em linha de comando (terminal)

Não são necessárias bibliotecas externas.

```bash
cd schoolcore
python main.py
```

Para executar os testes automatizados de demonstração:

```bash
python testes_sistema.py
```

### 5.2 Versão web (site)

A interface web foi construída com **Flask** e reaproveita integralmente
as classes e regras de negócio de `sistema.py` e `modelos/` — é a mesma
lógica do sistema em linha de comando, apenas com uma camada visual.

1. Instale o Flask (uma única vez):

   ```bash
   pip install flask
   ```

   Caso apareça um erro de ambiente gerenciado externamente, use:

   ```bash
   pip install flask --break-system-packages
   ```

2. Execute o servidor:

   ```bash
   cd schoolcore
   python app.py
   ```

3. Abra o navegador em **http://127.0.0.1:5000**.

A interface web possui 8 módulos navegáveis pela barra lateral: Painel,
Alunos, Professores, Disciplinas, Turmas, Matrículas, Acadêmico (notas,
frequência e boletim) e Relatórios. Todos os dados são salvos
automaticamente na pasta `dados/` (mesmos arquivos JSON utilizados pela
versão em terminal — é possível alternar entre as duas versões livremente).

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

  # isso e o meu primeiro site e sistema complexo que criei
  

