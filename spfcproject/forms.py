from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, Optional, ValidationError
from spfcproject.models import Usuario, Atleta
from datetime import datetime


class FormCriarConta(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(),Length(4, 20)])
    confirmacao_senha = PasswordField('Confirmação de Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criar_conta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado!')
        if not '@saopaulofc.net' in email.data:
            raise ValidationError('Somente emails @saopaulofc.net serão permitidos')


class FormEditarPerfil(FlaskForm):
    foto_usuario = FileField('Escolher Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    botao_adicionar_foto_usuario = SubmitField('Atualizar')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=4, max=20)])
    lembrar_dados = BooleanField('Lembrar dados de Acesso')
    botao_submit_login = SubmitField('Login')


def validar_idade(form, field):
    """Valida se o atleta tem menos de 18 anos e exige os dados do responsável."""
    hoje = datetime.today().date()
    idade = hoje.year - field.data.year - ((hoje.month, hoje.day) < (field.data.month, field.data.day))

    if idade < 18:
        if not form.nome_responsavel.data or not form.ddd_responsavel.data or not form.telefone_responsavel.data:
            raise ValidationError("Os campos do responsável são obrigatórios para menores de 18 anos.")


class FormCadastroAtleta(FlaskForm):
    nome_completo = StringField('Nome do Atleta', validators=[DataRequired()])
    data_nascimento = DateField('Data de Nascimento', format='%Y-%m-%d', validators=[DataRequired(), validar_idade])
    cpf = StringField('CPF',validators=[DataRequired(), Regexp(r'^\d{11}$', message="CPF inválido"), Length(min=11, max=11)])
    rg = StringField('RG', validators=[DataRequired(), Regexp(r'^\d{9}$', message="RG inválido"), Length(min=9, max=9)])
    sexo = SelectField('Sexo', choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')], validators=[DataRequired()])
    nacionalidade = StringField('Nacionalidade', validators=[DataRequired()])
    naturalidade = StringField('Naturalidade', validators=[DataRequired()])
    endereco = StringField('Endereço Completo', validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[DataRequired(), Regexp(r'^\d{9}$', message="Telefone inválido"), Length(min=9, max=9)])
    ddd = StringField('DDD', validators=[DataRequired(), Regexp(r'^\d{2}$', message="DDD inválido"), Length(min=2, max=2)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])

    # Campos do responsável (só obrigatórios se o atleta for menor de 18 anos)
    nome_responsavel = StringField('Nome Completo do Responsável', validators=[Optional()])
    telefone_responsavel = StringField('Telefone do Responsável', validators=[Optional(), Regexp(r'^\d{10,11}$', message="Telefone inválido"), Length(min=10, max=11)])
    ddd_responsavel = StringField('DDD do Responsável', validators=[Optional(), Length(min=2, max=2)])

    botao_cadastrar_atleta = SubmitField('Cadastrar Atleta')


    def validate_email(self, email):
        atleta = Atleta.query.filter_by(email=email.data).first()
        if atleta:
            raise ValidationError('E-mail já cadastrado!')


    def validate_cpf(self, cpf):
        atleta = Atleta.query.filter_by(cpf=cpf.data).first()
        if atleta:
            raise ValidationError('CPF já cadastrado!')


    def validate_rg(self, rg):
        atleta = Atleta.query.filter_by(rg=rg.data).first()
        if atleta:
            raise ValidationError('RG já cadastrado!')


    def validate_telefone(self, telefone):
        atleta = Atleta.query.filter_by(telefone=telefone.data).first()
        if atleta:
            raise ValidationError('Telefone já cadastrado!')


class FormEdicaoAtleta(FlaskForm):
    id = HiddenField()
    nome_completo = StringField('Nome do Atleta', validators=[DataRequired()])
    data_nascimento = DateField('Data de Nascimento', format='%Y-%m-%d', validators=[DataRequired(), validar_idade])
    cpf = StringField('CPF',validators=[DataRequired(), Regexp(r'^\d{11}$', message="CPF inválido"), Length(min=11, max=11)])
    rg = StringField('RG', validators=[DataRequired(), Regexp(r'^\d{9}$', message="RG inválido"), Length(min=9, max=9)])
    sexo = SelectField('Sexo', choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')], validators=[DataRequired()])
    nacionalidade = StringField('Nacionalidade', validators=[DataRequired()])
    naturalidade = StringField('Naturalidade', validators=[DataRequired()])
    endereco = StringField('Endereço Completo', validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[DataRequired(), Regexp(r'^\d{9}$', message="Telefone inválido"), Length(min=9, max=9)])
    ddd = StringField('DDD', validators=[DataRequired(), Regexp(r'^\d{2}$', message="DDD inválido"), Length(min=2, max=2)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])

    nome_responsavel = StringField('Nome Completo do Responsável', validators=[Optional()])
    telefone_responsavel = StringField('Telefone do Responsável', validators=[Optional(), Regexp(r'^\d{10,11}$', message="Telefone inválido"), Length(min=10, max=11)])
    ddd_responsavel = StringField('DDD do Responsável', validators=[Optional(), Length(min=2, max=2)])

    botao_editar_atleta = SubmitField('Salvar Edições')


    def validate_email(self, email):
        atleta_existente = Atleta.query.filter_by(email=email.data).first()
        if atleta_existente and atleta_existente.id != int(self.id.data):
            raise ValidationError('Este e-mail já está em uso por outro atleta.')


    def validate_cpf(self, cpf):
        atleta_existente = Atleta.query.filter_by(cpf=cpf.data).first()
        if atleta_existente and atleta_existente.id != int(self.id.data):
            raise ValidationError('Este cpf já está em uso por outro atleta.')


    def validate_rg(self, rg):
        atleta_existente = Atleta.query.filter_by(rg=rg.data).first()
        if atleta_existente and atleta_existente.id != int(self.id.data):
            raise ValidationError('Este rg já está em uso por outro atleta.')


    def validate_telefone(self, telefone):
        atleta_existente = Atleta.query.filter_by(telefone=telefone.data).first()
        if atleta_existente and atleta_existente.id != int(self.id.data):
            raise ValidationError('Este telefone já está em uso por outro atleta.')
