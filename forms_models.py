from django import forms
from controle.models import *



class AddItemForm(forms.ModelForm):
    class Meta:
        model = Bens
        fields = ['RFID', 'nome', 'descricao', 'data_aquisicao',
                'valor', 'status','categoria',
                'departamento', 'fornecedor']
        widgets = {
            'RFID': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o código RFID'
            }),
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do item'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição detalhada...'
            }),
            'data_aquisicao': forms.DateInput(attrs={
                'class': 'form-control datepicker',
                'type': 'date'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0,00'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'departamento': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fornecedor': forms.Select(attrs={
                'class': 'form-select'
            })
        }

class AddMoveForm(forms.ModelForm):
    class Meta:
        model = Movimentacoes
        fields = ['ativo', 'departamento_origem', 'departamento_destino', 'responsavel']
        widgets = {
            'ativo':forms.Select(),
            'departamento_origem':forms.Select(),
            'departamento_destino':forms.Select(),
            'responsavel':forms.Select()
        }

class AddRelatorioDanoForm(forms.ModelForm):
    class Meta:
        model = Relatorios
        fields = ['img', 'titulo', 'conteudo', 'criado_por']
        widgets = {
            'img': forms.FileInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'criado_por': forms.Select(attrs={'class': 'form-select'})
        }
        
class AddRelatorioPerdaForm(forms.ModelForm):
    class Meta:
        model = Relatorios
        fields = ['titulo','conteudo',
                  'criado_por']

class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome de usuário'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Crie uma senha segura'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'exemplo@dominio.com'
            })
        }
class AddCategoriasForm(forms.ModelForm):
    class Meta:
        model = Categorias
        fields = ['nome', 'descricao']

class AddDepartamentosForm(forms.ModelForm):
    class Meta:
        model = Departamentos
        fields = ['nome', 'localizacao']

class AddFornecedoresForm(forms.ModelForm):
    class Meta:
        model = Fornecedores
        fields = ['nome_empresa', 'dados_contato','categoria']

class UpdateItemForm(forms.ModelForm):
    class Meta:
        model = Bens
        fields = ['RFID', 'nome', 'descricao', 'data_aquisicao',
                'valor', 'status','categoria', 'fornecedor']
        widgets = {
            'RFID': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o código RFID'
            }),
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do item'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição detalhada...'
            }),
            'data_aquisicao': forms.DateInput(attrs={
                'class': 'form-control datepicker',
                'type': 'date'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': '0,00'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fornecedor': forms.Select(attrs={
                'class': 'form-select'
            })
        }
