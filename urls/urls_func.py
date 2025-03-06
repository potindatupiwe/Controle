from django.urls import path

from .. import views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    #Index
    path('index_func', login_required(views.IndexView.as_view()), name='index_func'),
    #Bens
    path('list_bens', login_required(views.ViewBens.as_view()), name='list_bens'),
    path('add_bens', login_required(views.AddBensViews.as_view()), name='add_bens'),
    path('delete_bens/<str:pk>', login_required(views.DeleteBensView.as_view()), name='delete_bens'),
    path('update_bens/<str:pk>', login_required(views.UpdateBensView.as_view()), name='update_bens'),
    #Movimentações
    path('add_movimentacao',login_required(views.AddMoveView.as_view()), name='add_movimentacao'),
    path('show_movimentacoes', login_required(views.ViewMovimentacao.as_view()),name='show_movimentacoes'),
    #Relatórios
    path('add_relatorio',login_required(views.AddRelatorioView.as_view()),name='add_relatorio'),
    path('add_relatorio_perda',login_required(views.AddRelatorioPerdaView.as_view()),name='add_relatorio_perda'),
    path('add_relatorio_dano',login_required(views.AddRelatorioDanoView.as_view()),name='add_relatorio_dano'),
    ]