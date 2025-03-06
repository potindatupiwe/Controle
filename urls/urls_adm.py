from django.urls import path
from django.contrib.auth.decorators import login_required
from .. import views

urlpatterns = [
    #Index
    path('index_adm', login_required(views.IndexView.as_view()), name='index_adm'),
    #Categorias
    path('add_categorias', login_required(views.CrudCategoria.AddViews.as_view()), name='add_categorias'),
    path('show_categorias', login_required(views.CrudCategoria.ShowViews.as_view()), name='show_categorias'),
    path('delete_categorias/<int:pk>', login_required(views.CrudCategoria.DeleteViews.as_view()), name='delete_categorias'),
    path('update_categorias/<int:pk>', login_required(views.CrudCategoria.UpdateViews.as_view()), name='update_categorias'),
    #Departamentos
    path('add_departamentos', login_required(views.CrudDepartamento.AddViews.as_view()), name='add_departamentos'),
    path('update_departamentos/<int:pk>', login_required(views.CrudDepartamento.UpdateViews.as_view()), name='update_departamentos'),
    path('delete_departamentos/<int:pk>', login_required(views.CrudDepartamento.DeleteViews.as_view()), name='delete_departamentos'),
    path('show_departamentos', login_required(views.CrudDepartamento.ShowViews.as_view()), name='show_departamentos'),
    #Fornecedores
    path('add_fornecedores', login_required(views.CrudFornecedores.AddViews.as_view()), name='add_fornecedores'),
    path('update_fornecedores/<int:pk>', login_required(views.CrudFornecedores.UpdateViews.as_view()), name='update_fornecedores'),
    path('delete_fornecedores/<int:pk>', login_required(views.CrudFornecedores.DeleteViews.as_view()), name='delete_fornecedores'),
    path('show_fornecedores', login_required(views.CrudFornecedores.ShowViews.as_view()), name='show_fornecedores'),
]

