from dns.e164 import query

from spfcproject import app, database, criptografia
from flask import render_template, flash, redirect, url_for, request
from spfcproject.forms import FormCadastroAtleta, FormCriarConta, FormLogin, FormEditarPerfil, FormEdicaoAtleta
from spfcproject.models import Usuario, Atleta
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image
from datetime import datetime


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form_cadastro_atleta = FormCadastroAtleta()
    if form_cadastro_atleta.validate_on_submit():
        atleta = Atleta(nome_completo=form_cadastro_atleta.nome_completo.data.title(), data_nascimento=form_cadastro_atleta.data_nascimento.data, cpf=form_cadastro_atleta.cpf.data, rg=form_cadastro_atleta.rg.data, sexo=form_cadastro_atleta.sexo.data, nacionalidade=form_cadastro_atleta.nacionalidade.data.title(), naturalidade=form_cadastro_atleta.naturalidade.data.title(), endereco=form_cadastro_atleta.endereco.data.title(), ddd=form_cadastro_atleta.ddd.data, telefone=form_cadastro_atleta.telefone.data, email=form_cadastro_atleta.email.data, nome_responsavel=form_cadastro_atleta.nome_responsavel.data.title(), telefone_responsavel=form_cadastro_atleta.telefone_responsavel.data, ddd_responsavel=form_cadastro_atleta.ddd_responsavel.data)
        database.session.add(atleta)
        current_user.atletas_cadastrados += 1
        database.session.commit()
        flash(f'{form_cadastro_atleta.nome_completo.data.title()} cadastrado com sucesso!', 'alert-success')
        return redirect(url_for('home'))
    return render_template('home.html', form_cadastro_atleta=form_cadastro_atleta)


@app.route('/exibir-atletas')
@login_required
def exibir_atletas():
    with app.app_context():
        atleta_existe = Atleta.query.all()
        lista_atletas = Atleta.query.order_by(Atleta.id.desc())
    return render_template('exibir-atletas.html', lista_atletas=lista_atletas, atleta_existe=atleta_existe)


@app.route('/cadastrospfc', methods=['GET', 'POST'])
def cadastrospfc():
    form_cadastrospfc = FormCriarConta()
    if form_cadastrospfc.validate_on_submit():
        senha_criptografada = criptografia.generate_password_hash(form_cadastrospfc.senha.data)
        usuario = Usuario(username=form_cadastrospfc.username.data, email=form_cadastrospfc.email.data, senha=senha_criptografada)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Cadastro realizado com sucesso! Por Favor, Faça o Login.', 'alert-success')
        return redirect(url_for('loginspfc'))
    return render_template('cadastrospfc.html', form_cadastrospfc=form_cadastrospfc)


@app.route('/loginspfc',  methods= ['GET', 'POST'])
def loginspfc():
    form_loginspfc = FormLogin()
    if form_loginspfc.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_loginspfc.email.data).first()
        if usuario and criptografia.check_password_hash(usuario.senha, form_loginspfc.senha.data):
            login_user(usuario, remember=form_loginspfc.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail {form_loginspfc.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash('E-mail ou senha Inválidos!', 'alert-danger')
    return render_template('loginspfc.html', form_loginspfc=form_loginspfc)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso', 'alert-success')
    return redirect(url_for('loginspfc'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_usuario}')
    return render_template('perfil.html', foto_perfil=foto_perfil)


def salvar_imagem(imagem):
    codigo = secrets.token_hex(10)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_atualizado = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_atualizado)
    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_atualizado


@app.route('/edicaoperfil', methods=['GET', 'POST'])
@login_required
def edicao_perfil():
    form_editar_perfil = FormEditarPerfil()
    foto_perfil = url_for('static', filename=f'fotos_perfil/{current_user.foto_usuario}')
    if form_editar_perfil.validate_on_submit():
        if form_editar_perfil.foto_usuario.data:
            flash('Foto de Perfil Atualizada com sucesso', 'alert-success')
            nome_imagem_atualizada = salvar_imagem(form_editar_perfil.foto_usuario.data)
            current_user.foto_usuario = nome_imagem_atualizada
            database.session.commit()
            return redirect(url_for('perfil'))
        else:
            flash(f'Adicione uma foto de perfil antes de atualizar', 'alert-danger')
    return render_template('edicaoperfil.html', foto_perfil=foto_perfil, form_editar_perfil=form_editar_perfil)


@app.route('/editaratleta-<id>', methods=['GET', 'POST'])
def edicao_atleta(id):
    form_edicao_atleta = FormEdicaoAtleta()
    atleta = Atleta.query.get(id)
    form_edicao_atleta.id.data = int(atleta.id)

    if request.method == 'GET':
        form_edicao_atleta.nome_completo.data = atleta.nome_completo
        form_edicao_atleta.data_nascimento.data = datetime.strptime(atleta.data_nascimento, "%Y-%m-%d")
        form_edicao_atleta.cpf.data = atleta.cpf
        form_edicao_atleta.rg.data = atleta.rg
        form_edicao_atleta.sexo.data = atleta.sexo
        form_edicao_atleta.nacionalidade.data = atleta.nacionalidade
        form_edicao_atleta.naturalidade.data = atleta.naturalidade
        form_edicao_atleta.endereco.data = atleta.endereco
        form_edicao_atleta.telefone.data = atleta.telefone
        form_edicao_atleta.ddd.data = atleta.ddd
        form_edicao_atleta.email.data = atleta.email
        form_edicao_atleta.nome_responsavel.data = atleta.nome_responsavel
        form_edicao_atleta.telefone_responsavel.data = atleta.telefone_responsavel
        form_edicao_atleta.ddd_responsavel.data = atleta.ddd_responsavel

    if form_edicao_atleta.validate_on_submit():
        atleta.nome_completo = form_edicao_atleta.nome_completo.data
        atleta.data_nascimento = form_edicao_atleta.data_nascimento.data
        atleta.cpf = form_edicao_atleta.cpf.data
        atleta.rg = form_edicao_atleta.rg.data
        atleta.sexo = form_edicao_atleta.sexo.data
        atleta.nacionalidade = form_edicao_atleta.nacionalidade.data
        atleta.naturalidade = form_edicao_atleta.naturalidade.data
        atleta.endereco = form_edicao_atleta.endereco.data
        atleta.telefone = form_edicao_atleta.telefone.data
        atleta.ddd = form_edicao_atleta.ddd.data
        atleta.email = form_edicao_atleta.email.data
        atleta.nome_responsavel = form_edicao_atleta.nome_responsavel.data
        atleta.telefone_responsavel = form_edicao_atleta.telefone_responsavel.data
        atleta.ddd_responsavel = form_edicao_atleta.ddd_responsavel.data
        database.session.commit()

        flash('Dados atualizados com sucesso', 'alert-success')

    return render_template('atleta.html', atleta=atleta, form_edicao_atleta=form_edicao_atleta )


@app.route('/atleta/<id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_atleta(id):
    atleta = Atleta.query.get(id)
    database.session.delete(atleta)
    current_user.atletas_cadastrados -= 1
    database.session.commit()
    flash('Atleta deletado com sucesso', 'alert-danger')
    return redirect(url_for('exibir_atletas'))


