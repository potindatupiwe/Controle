from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from .models import *
from django.views.generic.edit import FormView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView
from django.views import View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import Group
from controle.CRUD import *
from controle.forms import *
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
#Funcionarios
class ViewBens(ListView):
    model = Bens
    template_name = 'func/show_bens.html'
    context_object_name = 'list_bens'

class AddBensViews(FormView):
    form_class = AddItemForm
    template_name='func/add_bens.html'
    success_url = reverse_lazy('index_func')

    def form_valid(self, form:AddItemForm):
        form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,f'{form.errors}')
        return super().form_invalid(form)
class DeleteBensView(DeleteView):
    model = Bens
    template_name = 'func/delete_bens.html'
    success_url = reverse_lazy('list_bens')

class UpdateBensView(UpdateView):
    form_class = UpdateItemForm
    model = Bens
    template_name='func/update_bens.html'
    success_url = reverse_lazy('list_bens')

class AddMoveView(FormView):
    form_class = AddMoveForm
    template_name='func/add_move.html'
    success_url = reverse_lazy('list_bens')

    def form_valid(self, form:AddItemForm):
        ativo = form.cleaned_data.get('ativo')
        departamento_destino = form.cleaned_data.get('departamento_destino')
        Bens.objects.filter(nome = ativo).update(departamento = departamento_destino)
        form.save()
        return super().form_valid(form)
    
class AddRelatorioView(TemplateView):
    template_name='func/add_relatorio.html'
    
class AddRelatorioPerdaView(FormView):
    form_class = AddRelatorioPerdaForm
    template_name = 'func/add_relatorio_perda.html'
    success_url = reverse_lazy('list_bens')

    def form_valid(self, form:AddRelatorioPerdaForm):
        object = form.save()
        Relatorios.objects.filter(pk = object.pk).update(types = 'PERDA')
        obj = Relatorios.objects.get(id = object.pk)
        context = {"relatorio": obj}
        html_content = render_to_string("gerencia/show_detail_relatorio.html", context)
        text_content = f"O relatório do tipo {obj.types}"
        list_to = []
        gerencia_group = Group.objects.get(name="Gerencia")
        usuarios_gerencia = User.objects.filter(groups=gerencia_group)
        for i in usuarios_gerencia:
            list_to.append(i.email)
        email = EmailMultiAlternatives(
            subject="Relatorio",
            body=text_content,
            from_email="appdjango298@gmail.com",
            to=list_to,
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        return super().form_valid(form)
    
class AddRelatorioDanoView(FormView):
    form_class = AddRelatorioDanoForm
    template_name = 'func/add_relatorio_dano.html'
    success_url = reverse_lazy('list_bens')

    def form_valid(self, form:AddRelatorioPerdaForm):
        object = form.save()
        Relatorios.objects.filter(pk = object.pk).update(types = 'DANO')
        obj = Relatorios.objects.get(id = object.pk)
        context = {"relatorio": obj}
        html_content = render_to_string("gerencia/show_detail_relatorio.html", context)
        text_content = f"O relatório do tipo {obj.types}"
        list_to = []
        gerencia_group = Group.objects.get(name="Gerencia")
        usuarios_gerencia = User.objects.filter(groups=gerencia_group)
        for i in usuarios_gerencia:
            list_to.append(i.email)
        email = EmailMultiAlternatives(
            subject="Relatorio",
            body=text_content,
            from_email="appdjango298@gmail.com",
            to=list_to,
        )
        email.attach_file(f"media/{obj.img}")
        email.attach_alternative(html_content, "text/html")
        email.send()
        return super().form_valid(form)

#Gerencia
class ViewRelatorio(ListView):
    model = Relatorios
    template_name = 'gerencia/show_relatorio.html'
    context_object_name = 'relatorio'
   

class ViewRelatorioDetail(DetailView):
    model = Relatorios
    template_name = 'gerencia/show_detail_relatorio.html'
    context_object_name = 'relatorio'
    
class DeleteRelatorioView(DeleteView):
    model = Relatorios
    template_name = 'gerencia/delete_relatorio.html'
    success_url = reverse_lazy('show_relatorio')

class UpdateRelatorioPerdaView(UpdateView):
    fields = ['titulo', 'conteudo', 'criado_por']
    model = Relatorios
    template_name='gerencia/update_relatorio_perda.html'
    success_url = reverse_lazy('show_relatorio')
    
    def form_valid(self, form):
        Relatorios.objects.filter(pk=self.kwargs['pk']).update(modificado_por = self.request.user)
        form.save()
        return super().form_valid(form)
class UpdateRelatorioDanosView(UpdateView):
    fields = ['img','titulo', 'conteudo', 'criado_por']
    model = Relatorios
    template_name='gerencia/update_relatorio_dano.html'
    success_url = reverse_lazy('show_relatorio')
    
    def form_valid(self, form):
        Relatorios.objects.filter(pk=self.kwargs['pk']).update(modificado_por = self.request.user)
        form.save()
        
        return super().form_valid(form)





class ViewMovimentacao(ListView):
    model = Movimentacoes
    template_name = 'gerencia/show_move.html'
    context_object_name = 'movimentacoes'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = self.request.user.groups.all()
        return context
class DeleteMoveView(DeleteView):
    model = Movimentacoes
    template_name = 'gerencia/delete_move.html'
    success_url = reverse_lazy('index_gerencia')



class AddUserView(FormView):
    form_class = AddUserForm
    template_name = 'gerencia/add_user.html'
    success_url = reverse_lazy('index_gerencia')

    def form_valid(self, form:AddUserForm):
        form.save()
        user = User.objects.get(username = form.cleaned_data.get('username'))
        group = Group.objects.get(name=self.request.POST.get('group'))
        group.user_set.add(user)
        user.set_password(form.cleaned_data.get('password'))
        user.save()
        return super().form_valid(form)
    
class ViewUser(ListView):
    model = User
    template_name = 'gerencia/show_user.html'
    context_object_name = 'users'

class ViewDetailUser(DetailView):
    model = User
    template_name = 'gerencia/show_detail_user.html'
    context_object_name='user'

class DeleteUserView(DeleteView):
    model = User
    template_name = 'gerencia/delete_user.html'
    success_url = reverse_lazy('show_user')

class UpdateUserView(UpdateView):
    fields = ['username','email']
    template_name = 'gerencia/update_user.html'
    success_url = reverse_lazy('index_gerencia')
    model = User
    def form_valid(self, form:AddUserForm):
        form.save()
        user = User.objects.get(username = form.cleaned_data.get('username'))
        group = Group.objects.get(name=self.request.POST.get('group'))
        user.groups.clear()
        group.user_set.add(user)
        return super().form_valid(form)





#Administração
class CrudCategoria(metaclass = MetaCrud):
    model = Categorias
    success_url = reverse_lazy('show_categorias')
    form_class = AddCategoriasForm
    fields = ['nome', 'descricao']
    context_object_name = 'categorias'
    def form_valid(self, form:AddCategoriasForm):
        form.save()
        return super().form_valid(form)

class CrudDepartamento(metaclass = MetaCrud):
    model = Departamentos
    success_url = reverse_lazy('show_departamentos')
    form_class = AddDepartamentosForm
    fields = ['nome', 'localizacao']
    context_object_name = 'departamentos'
    def form_valid(self, form:AddDepartamentosForm):
        form.save()
        return super().form_valid(form)
    
class CrudFornecedores(metaclass = MetaCrud):
    model = Fornecedores
    success_url = reverse_lazy('show_fornecedores')
    form_class = AddFornecedoresForm
    fields = ['nome_empresa', 'dados_contato','categoria']
    context_object_name = 'fornecedores'
    def form_valid(self, form:AddFornecedoresForm):
        form.save()
        return super().form_valid(form)

class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html' 
    form_class = LoginForm
    
  

class IndexView(TemplateView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["group"] = self.request.user.groups.all()
        return context
    

class RedirectView(View):
    def get(self, *args, **kwargs):
        if self.request.user.groups.filter(name='Administradores').exists():
            return redirect('index_adm')
        elif self.request.user.groups.filter(name='Funcionários').exists():
            return redirect('index_func')
        else:
            return redirect('index_gerencia')
        



class DashboardView(TemplateView):
    template_name='dashboard_base.html'

class CustomLogout(LogoutView):
    pass



