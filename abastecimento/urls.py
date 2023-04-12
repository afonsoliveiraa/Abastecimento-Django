from django.urls import path

from abastecimento.views import index, register, unidade_list, unidade_createPage, unidade_create, veiculo_list, \
    veiculo_createPage, veiculo_create, contrato_list, contrato_createPage, contrato_create, abastecimento_list, \
    abastecimento_createPage, abastecimento_create, abastecimento_edit, item_create, item_delete, abastecimento_delete, \
    abastecimento_update, unidade_delete, veiculo_delete, usuario_list, usuario_createPage, update_createPage, \
    update_create

urlpatterns = [
    path('', index, name='index'),
    path('usuario_list/', usuario_list, name='usuario_list'),
    path('usuario_createPage/', usuario_createPage, name='usuario_createPage'),
    path('register/', register, name='register'),

    path('unidade_list/', unidade_list, name='unidade_list'),
    path('unidade_createPage/', unidade_createPage, name='unidade_createPage'),
    path('unidade_create/', unidade_create, name='unidade_create'),
    path('unidade_delete/<int:id>', unidade_delete, name='unidade_delete'),

    path('veiculo_list/', veiculo_list, name='veiculo_list'),
    path('veiculo_createPage/', veiculo_createPage, name='veiculo_createPage'),
    path('veiculo_create/', veiculo_create, name='veiculo_create'),
    path('veiculo_delete/<int:id>/', veiculo_delete, name='veiculo_delete'),

    path('contrato_list/', contrato_list, name='contrato_list'),
    path('contrato_createPage/', contrato_createPage, name='contrato_createPage'),
    path('contrato_create/', contrato_create, name='contrato_create'),

    path('abastecimento_list/', abastecimento_list, name='abastecimento_list'),
    path('abastecimento_createPage/', abastecimento_createPage, name='abastecimento_createPage'),
    path('abastecimento_create/', abastecimento_create, name='abastecimento_create'),
    path('abastecimento_edit/<int:abastecimento_id>/', abastecimento_edit, name='abastecimento_edit'),
    path('abastecimento_update/<int:id>/', abastecimento_update, name='abastecimento_update'),
    path('abastecimento_delete/<int:id>/', abastecimento_delete, name='abastecimento_delete'),

    path('item_create/<int:abastecimento_id>/', item_create, name='item_create'),
    path('item_delete/<int:id>/', item_delete, name='item_delete'),

    path('update_createPage/', update_createPage, name='update_createPage'),
    path('update_create/', update_create, name='update_create'),
]
