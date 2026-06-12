"""
Módulo: app
-------------
Aplicação web (Flask) do SchoolCore — Sistema Integrado de Gestão Escolar.

Esta aplicação reaproveita integralmente a camada de regras de negócio
já implementada em `sistema.py` e `modelos/`, oferecendo uma interface
web (HTML) para os módulos de:

    - Painel (visão geral)
    - Gestão de Alunos
    - Gestão de Professores
    - Gestão de Disciplinas
    - Gestão de Turmas
    - Matrículas
    - Módulo Acadêmico (notas, frequência e boletim)
    - Módulo Gerencial (relatórios)

Todas as exceções de negócio definidas em `excecoes.py` são capturadas
e exibidas ao usuário por meio de mensagens "flash", sem expor detalhes
técnicos (stack traces) na interface.

Como executar:
    pip install flask --break-system-packages   (caso ainda não instalado)
    python app.py

Em seguida, acesse http://127.0.0.1:5000 no navegador.
"""

from flask import Flask, render_template, request, redirect, url_for, flash

from sistema import SistemaSchoolCore
from excecoes import SchoolCoreError


app = Flask(__name__)
app.secret_key = "schoolcore-projeto-integrador-2026-1"

# Instância única do sistema, compartilhada por toda a aplicação.
sistema = SistemaSchoolCore(diretorio_dados="dados")


# ----------------------------------------------------------------------
# Filtros de template
# ----------------------------------------------------------------------

@app.template_filter("percentual")
def formatar_percentual(valor):
    """Formata um número como percentual, ou exibe '—' quando None."""
    if valor is None:
        return "—"
    return f"{valor:g}%"


@app.template_filter("numero")
def formatar_numero(valor):
    """Formata um número, ou exibe '—' quando None."""
    if valor is None:
        return "—"
    return f"{valor:g}"


_SITUACAO_SLUGS = {
    "Aprovado": "aprovado",
    "Reprovado por nota": "reprovado-nota",
    "Reprovado por frequência": "reprovado-frequencia",
    "Reprovado por nota e frequência": "reprovado-nota-e-frequencia",
    "Sem dados suficientes": "sem-dados",
}


@app.template_filter("situacao_slug")
def situacao_slug(situacao):
    """Converte a descrição da situação acadêmica em uma classe CSS."""
    return _SITUACAO_SLUGS.get(situacao, "sem-dados")


# ----------------------------------------------------------------------
# Painel (dashboard)
# ----------------------------------------------------------------------

@app.route("/")
def painel():
    total_alunos = len(sistema.listar_alunos())
    total_alunos_ativos = len(sistema.listar_alunos(apenas_ativos=True))
    total_professores = len(sistema.listar_professores())
    total_disciplinas = len(sistema.listar_disciplinas())
    total_turmas = len(sistema.listar_turmas())
    total_matriculas_ativas = sistema.relatorio_quantidade_matriculados()
    aprovacao = sistema.relatorio_aprovados_reprovados()
    disciplinas_ofertadas = sistema.relatorio_disciplinas_mais_ofertadas()[:5]

    return render_template(
        "painel.html",
        total_alunos=total_alunos,
        total_alunos_ativos=total_alunos_ativos,
        total_professores=total_professores,
        total_disciplinas=total_disciplinas,
        total_turmas=total_turmas,
        total_matriculas_ativas=total_matriculas_ativas,
        aprovacao=aprovacao,
        disciplinas_ofertadas=disciplinas_ofertadas,
    )


# ----------------------------------------------------------------------
# Gestão de Alunos
# ----------------------------------------------------------------------

@app.route("/alunos")
def listar_alunos():
    filtro = request.args.get("status", "todos")
    alunos = sistema.listar_alunos()
    if filtro != "todos":
        alunos = [a for a in alunos if a.status_academico == filtro]
    return render_template("alunos.html", alunos=alunos, filtro=filtro)


@app.route("/alunos/novo", methods=["GET", "POST"])
def novo_aluno():
    if request.method == "POST":
        try:
            sistema.cadastrar_aluno(
                matricula=request.form["matricula"],
                nome=request.form["nome"],
                cpf=request.form["cpf"],
                data_nascimento=request.form["data_nascimento"],
                curso=request.form["curso"],
                periodo=request.form["periodo"],
                status_academico=request.form.get("status_academico", "ativo"),
                email=request.form.get("email", ""),
            )
            flash(f"Aluno {request.form['matricula']} cadastrado com sucesso.", "sucesso")
            return redirect(url_for("listar_alunos"))
        except (SchoolCoreError, ValueError) as erro:
            flash(str(erro), "erro")

    return render_template("aluno_form.html", aluno=None)


@app.route("/alunos/<matricula>")
def detalhe_aluno(matricula):
    try:
        aluno = sistema.consultar_aluno(matricula)
    except SchoolCoreError as erro:
        flash(str(erro), "erro")
        return redirect(url_for("listar_alunos"))

    boletim = sistema.emitir_boletim(matricula)
    historico = sistema.consultar_historico_matricula(matricula)
    return render_template(
        "aluno_detalhe.html", aluno=aluno, boletim=boletim, historico=historico
    )


@app.route("/alunos/<matricula>/editar", methods=["GET", "POST"])
def editar_aluno(matricula):
    try:
        aluno = sistema.consultar_aluno(matricula)
    except SchoolCoreError as erro:
        flash(str(erro), "erro")
        return redirect(url_for("listar_alunos"))

    if request.method == "POST":
        try:
            sistema.atualizar_aluno(
                matricula,
                nome=request.form["nome"],
                email=request.form.get("email", ""),
                curso=request.form["curso"],
                periodo=request.form["periodo"],
                status_academico=request.form["status_academico"],
            )
            flash(f"Aluno {matricula} atualizado com sucesso.", "sucesso")
            return redirect(url_for("detalhe_aluno", matricula=matricula))
        except (SchoolCoreError, ValueError) as erro:
            flash(str(erro), "erro")

    return render_template("aluno_form.html", aluno=aluno)


@app.route("/alunos/<matricula>/inativar", methods=["POST"])
def inativar_aluno(matricula):
    try:
        sistema.excluir_aluno(matricula, inativar=True)
        flash(f"Aluno {matricula} inativado.", "sucesso")
    except SchoolCoreError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("listar_alunos"))


@app.route("/alunos/<matricula>/excluir", methods=["POST"])
def excluir_aluno(matricula):
    try:
        sistema.excluir_aluno(matricula, inativar=False)
        flash(f"Aluno {matricula} removido definitivamente.", "sucesso")
    except SchoolCoreError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("listar_alunos"))


# ----------------------------------------------------------------------
# Gestão de Professores
# ----------------------------------------------------------------------

@app.route("/professores")
def listar_professores():
    professores = sistema.listar_professores()
    return render_template("professores.html", professores=professores)


@app.route("/professores/novo", methods=["GET", "POST"])
def novo_professor():
    if request.method == "POST":
        try:
            sistema.cadastrar_professor(
                codigo_funcional=request.form["codigo_funcional"],
                nome=request.form["nome"],
                cpf=request.form["cpf"],
                titulacao=request.form["titulacao"],
                area_atuacao=request.form["area_atuacao"],
                email=request.form.get("email", ""),
            )
            flash(f"Professor {request.form['codigo_funcional']} cadastrado com sucesso.", "sucesso")
            return redirect(url_for("listar_professores"))
        except SchoolCoreError as erro:
            flash(str(erro), "erro")

    return render_template("professor_form.html", professor=None)


@app.route("/professores/<codigo>")
def detalhe_professor(codigo):
    try:
        professor = sistema.consultar_professor(codigo)
    except SchoolCoreError as erro:
        flash(str(erro), "erro")
        return redirect(url_for("listar_professores"))

    disciplinas = []
    for codigo_disciplina in professor.disciplinas_vinculadas:
        try:
            disciplinas.append(sistema.consultar_disciplina(codigo_disciplina))
        except SchoolCoreError:
            continue

    return render_template("professor_detalhe.html", professor=professor, disciplinas=disciplinas)


@app.route("/professores/<codigo>/editar", methods=["GET", "POST"])
def editar_professor(codigo):
    try:
        professor = sistema.consultar_professor(codigo)
    except SchoolCoreError as erro:
        flash(str(erro), "erro")
        return redirect(url_for("listar_professores"))

    if request.method == "POST":
        try:
            sistema.atualizar_professor(
                codigo,
                nome=request.form["nome"],
                email=request.form.get("email", ""),
                titulacao=request.form["titulacao"],
                area_atuacao=request.form["area_atuacao"],
            )
            flash(f"Professor {codigo} atualizado com sucesso.", "sucesso")
            return redirect(url_for("detalhe_professor", codigo=codigo))
        except SchoolCoreError as erro:
            flash(str(erro), "erro")

    return render_template("professor_form.html", professor=professor)


# ----------------------------------------------------------------------
# Gestão de Disciplinas
# ----------------------------------------------------------------------

@app.route("/disciplinas")
def listar_disciplinas():
    disciplinas = sistema.listar_disciplinas()
    nomes_professores = {p.codigo_funcional: p.nome for p in sistema.listar_professores()}
    return render_template(
        "disciplinas.html", disciplinas=disciplinas, nomes_professores=nomes_professores
    )


@app.route("/disciplinas/novo", methods=["GET", "POST"])
def nova_disciplina():
    if request.method == "POST":
        try:
            professor = request.form.get("professor_responsavel") or None
            sistema.cadastrar_disciplina(
                codigo=request.form["codigo"],
                nome=request.form["nome"],
                carga_horaria=request.form["carga_horaria"],
                periodo=request.form["periodo"],
                professor_responsavel=professor,
            )
            flash(f"Disciplina {request.form['codigo']} cadastrada com sucesso.", "sucesso")
            return redirect(url_for("listar_disciplinas"))
        except (SchoolCoreError, ValueError) as erro:
            flash(str(erro), "erro")

    professores = sistema.listar_professores()
    return render_template("disciplina_form.html", professores=professores)


@app.route("/disciplinas/<codigo>/vincular", methods=["POST"])
def vincular_professor(codigo):
    try:
        sistema.vincular_professor_disciplina(codigo, request.form["professor_responsavel"])
        flash(f"Professor vinculado à disciplina {codigo} com sucesso.", "sucesso")
    except SchoolCoreError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("listar_disciplinas"))


# ----------------------------------------------------------------------
# Gestão de Turmas
# ----------------------------------------------------------------------

@app.route("/turmas")
def listar_turmas():
    turmas = sistema.listar_turmas()
    nomes_disciplinas = {d.codigo: d.nome for d in sistema.listar_disciplinas()}
    nomes_professores = {p.codigo_funcional: p.nome for p in sistema.listar_professores()}
    return render_template(
        "turmas.html",
        turmas=turmas,
        nomes_disciplinas=nomes_disciplinas,
        nomes_professores=nomes_professores,
    )


@app.route("/turmas/novo", methods=["GET", "POST"])
def nova_turma():
    if request.method == "POST":
        try:
            professor = request.form.get("professor_codigo") or None
            sistema.criar_turma(
                codigo=request.form["codigo"],
                disciplina_codigo=request.form["disciplina_codigo"],
                professor_codigo=professor,
                capacidade=request.form["capacidade"],
            )
            flash(f"Turma {request.form['codigo']} criada com sucesso.", "sucesso")
            return redirect(url_for("listar_turmas"))
        except (SchoolCoreError, ValueError) as erro:
            flash(str(erro), "erro")

    disciplinas = sistema.listar_disciplinas()
    professores = sistema.listar_professores()
    return render_template("turma_form.html", disciplinas=disciplinas, professores=professores)


# ----------------------------------------------------------------------
# Matrículas
# ----------------------------------------------------------------------

@app.route("/matriculas")
def listar_matriculas():
    matriculas = sorted(sistema._matriculas.values(), key=lambda m: m.id, reverse=True)
    nomes_alunos = {a.matricula: a.nome for a in sistema.listar_alunos()}
    nomes_disciplinas = {d.codigo: d.nome for d in sistema.listar_disciplinas()}
    codigo_disciplina_da_turma = {t.codigo: t.disciplina_codigo for t in sistema.listar_turmas()}

    alunos = sistema.listar_alunos(apenas_ativos=True)
    turmas = sistema.listar_turmas()

    return render_template(
        "matriculas.html",
        matriculas=matriculas,
        nomes_alunos=nomes_alunos,
        nomes_disciplinas=nomes_disciplinas,
        codigo_disciplina_da_turma=codigo_disciplina_da_turma,
        alunos=alunos,
        turmas=turmas,
    )


@app.route("/matriculas/nova", methods=["POST"])
def nova_matricula():
    try:
        sistema.realizar_matricula(
            matricula_aluno=request.form["matricula_aluno"],
            codigo_turma=request.form["codigo_turma"],
        )
        flash("Matrícula realizada com sucesso.", "sucesso")
    except SchoolCoreError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("listar_matriculas"))


@app.route("/matriculas/<int:id_matricula>/cancelar", methods=["POST"])
def cancelar_matricula(id_matricula):
    try:
        sistema.cancelar_matricula(id_matricula)
        flash(f"Matrícula #{id_matricula} cancelada.", "sucesso")
    except SchoolCoreError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("listar_matriculas"))


# ----------------------------------------------------------------------
# Módulo Acadêmico
# ----------------------------------------------------------------------

@app.route("/academico")
def academico():
    alunos = sistema.listar_alunos(apenas_ativos=True)
    disciplinas = sistema.listar_disciplinas()
    return render_template("academico.html", alunos=alunos, disciplinas=disciplinas)


@app.route("/academico/nota-parcial", methods=["POST"])
def lancar_nota_parcial():
    try:
        sistema.lancar_nota_parcial(
            request.form["matricula_aluno"],
            request.form["codigo_disciplina"],
            request.form["nota"],
        )
        flash("Nota parcial lançada com sucesso.", "sucesso")
    except (SchoolCoreError, ValueError) as erro:
        flash(str(erro), "erro")
    return redirect(url_for("academico"))


@app.route("/academico/nota-final", methods=["POST"])
def lancar_nota_final():
    try:
        sistema.lancar_nota_final(
            request.form["matricula_aluno"],
            request.form["codigo_disciplina"],
            request.form["nota"],
        )
        flash("Nota final lançada com sucesso.", "sucesso")
    except (SchoolCoreError, ValueError) as erro:
        flash(str(erro), "erro")
    return redirect(url_for("academico"))


@app.route("/academico/frequencia", methods=["POST"])
def registrar_frequencia():
    try:
        presente = request.form.get("presente") == "sim"
        sistema.registrar_frequencia(
            request.form["matricula_aluno"],
            request.form["codigo_disciplina"],
            presente,
        )
        flash("Frequência registrada com sucesso.", "sucesso")
    except SchoolCoreError as erro:
        flash(str(erro), "erro")
    return redirect(url_for("academico"))


@app.route("/academico/boletim", methods=["GET", "POST"])
def consultar_boletim():
    matricula = request.values.get("matricula_aluno", "").strip()
    if not matricula:
        alunos = sistema.listar_alunos()
        return render_template("boletim.html", boletim=None, alunos=alunos, matricula="")

    try:
        boletim = sistema.emitir_boletim(matricula)
    except SchoolCoreError as erro:
        flash(str(erro), "erro")
        return redirect(url_for("academico"))

    return render_template("boletim.html", boletim=boletim, alunos=None, matricula=matricula)


# ----------------------------------------------------------------------
# Módulo Gerencial (relatórios)
# ----------------------------------------------------------------------

@app.route("/relatorios")
def relatorios():
    total_matriculados = sistema.relatorio_quantidade_matriculados()
    disciplinas_ofertadas = sistema.relatorio_disciplinas_mais_ofertadas()
    professores_ativos = sistema.relatorio_professores_ativos()
    aprovacao = sistema.relatorio_aprovados_reprovados()
    frequencia_por_turma = sistema.relatorio_frequencia_media_por_turma()
    nomes_disciplinas = {d.codigo: d.nome for d in sistema.listar_disciplinas()}

    return render_template(
        "relatorios.html",
        total_matriculados=total_matriculados,
        disciplinas_ofertadas=disciplinas_ofertadas,
        professores_ativos=professores_ativos,
        aprovacao=aprovacao,
        frequencia_por_turma=frequencia_por_turma,
        nomes_disciplinas=nomes_disciplinas,
    )


if __name__ == "__main__":
    app.run(debug=True)
