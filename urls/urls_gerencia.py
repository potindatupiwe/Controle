from django.urls import path

from .. import views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    #Index
    path('index_gerencia', login_required(views.IndexView.as_view()), name='index_gerencia'),
    #Usuários
    path('add_user',login_required(views.AddUserView.as_view()),name='add_user'),
    path('show_user', login_required(views.ViewUser.as_view()),name='show_user'),
    path('show_detail_user/<int:pk>', login_required(views.ViewDetailUser.as_view()), name='show_detail_user'),
    path('delete_user/<int:pk>', login_required(views.DeleteUserView.as_view()), name='delete_user'),
    path('update_user/<int:pk>', login_required(views.UpdateUserView.as_view()), name='update_user'),
    #Movimentacoes
    path('delete_move/<int:pk>', login_required(views.DeleteMoveView.as_view()), name='dalete_movimentacao'),
    path('show_movimentacoes', login_required(views.ViewMovimentacao.as_view()),name='show_movimentacoes'),
    #Relatorios
    path('show_relatorio', login_required(views.ViewRelatorio.as_view()),name='show_relatorio'),
    path('show_detail_relatorio/<int:pk>', login_required(views.ViewRelatorioDetail.as_view()), name='show_detail_relatorio'),
    path('delete_relatorio/<int:pk>',login_required(views.DeleteRelatorioView.as_view()),name='delete_relatorio'),
    path('update_relatorio_perda/<int:pk>',login_required(views.UpdateRelatorioPerdaView.as_view()),name='update_relatorio_perda'),
    path('update_relatorio_dano/<int:pk>',login_required(views.UpdateRelatorioDanosView.as_view()),name='update_relatorio_danos'),
    ]