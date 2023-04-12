import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from rolepermissions.decorators import has_permission_decorator

from abastecimento.admin import CustomUserCreationForm
from abastecimento.forms import UnidadeForm, VeiculoForm, ContratoForm, AbastecimentoForm, Item_AbastecimentoForm, \
    UpdateForm
from abastecimento.models import Unidade_Orcamentaria, Veiculo, Contrato, Abastecimento, Item_Abastecimento, Update


@login_required
def usuario_list(request):
    usuarios = User.objects.all()

    # Paginação para as tabelas de Usuários
    paginator = Paginator(usuarios, 5)
    page = request.GET.get('page')
    usuarios_page = paginator.get_page(page)

    context = {'usuarios_page': usuarios_page}
    return render(request, 'usuarios/usuario_list.html', context)


@login_required
def usuario_createPage(request):
    form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)


@login_required
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_valid = False
            user.save()
            messages.success(request, 'Registrado. Agora faça o login para começar!')
            return redirect(usuario_list)

        else:
            print('invalid registration details')

    form = CustomUserCreationForm()
    return render(request, "usuarios/usuario_list.html", {"form": form})


# HomePage

@login_required
def index(request):
    # Todos os updates
    updates = Update.objects.all()

    context = {'updates': updates}
    return render(request, 'home/index.html', context)


# Unidades Orçamentárias

@login_required
def unidade_list(request):
    # Todas as Unidades
    unidades = Unidade_Orcamentaria.objects.all()

    # Paginação para as tabelas de Unidades Orçamentárias
    paginator = Paginator(unidades, 5)
    page = request.GET.get('page')
    unidades_page = paginator.get_page(page)

    context = {'unidades_page': unidades_page}
    return render(request, 'unidade/unidade_list.html', context)


@login_required
def unidade_createPage(request):
    # Formulário para criação das unidades
    form = UnidadeForm()

    context = {'form': form}
    return render(request, 'unidade/unidade_createPage.html', context)


@login_required
def unidade_create(request):
    if request.method == 'POST':
        form = UnidadeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(unidade_list)
    else:
        form = UnidadeForm()
        context = {'form': form}
        return render(request, 'unidade/unidade_createPage.html', context)


@login_required
def unidade_delete(request, id):
    unidade = Unidade_Orcamentaria.objects.get(id=id)

    if unidade.unidade_veiculo.exists() or unidade.unidade_contrato.exists():
        return HttpResponseNotFound(
            '<p>Unidade sendo usada em algum veiculo ou contrato</p>')
    else:
        unidade.delete()
        return redirect(unidade_list)


# Veiculos

@login_required
def veiculo_list(request):
    # Todos os Veículos
    veiculos = Veiculo.objects.all()

    # Paginação para as tabelas de Veículos
    paginator = Paginator(veiculos, 5)
    page = request.GET.get('page')
    veiculos_page = paginator.get_page(page)

    context = {'veiculos_page': veiculos_page}
    return render(request, 'veiculo/veiculo_list.html', context)


@login_required
def veiculo_createPage(request):
    # Formulário para criação dos veículos
    form = VeiculoForm()

    context = {'form': form}
    return render(request, 'veiculo/veiculo_createPage.html', context)


@login_required
def veiculo_create(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(veiculo_list)
    else:
        form = VeiculoForm()
        context = {'form': form}
        return render(request, 'veiculo/veiculo_createPage.html', context)


@login_required
def veiculo_delete(request, id):
    veiculo = Veiculo.objects.get(id=id)

    if veiculo.veiculo_item.exists():
        return HttpResponseNotFound(
            '<p>Veículo sendo utilizado em algum abastecimento utilizado em </p>')
    else:
        veiculo.delete()
        return redirect(veiculo_list)


# Contratos

@login_required
def contrato_list(request):
    # Todos os Contratos
    contratos = Contrato.objects.all()

    # Paginação para as tabelas de Contratos
    paginator = Paginator(contratos, 5)
    page = request.GET.get('page')
    contratos_page = paginator.get_page(page)

    context = {'contratos_page': contratos_page}
    return render(request, 'contrato/contrato_list.html', context)


@login_required
def contrato_createPage(request):
    # Formulário para criação dos contratos
    form = ContratoForm()

    context = {'form': form}
    return render(request, 'contrato/contrato_createPage.html', context)


@login_required
def contrato_create(request):
    if request.method == 'POST':
        form = ContratoForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(contrato_list)
    else:
        form = ContratoForm()

        context = {'form': form}
        return render(request, 'contrato/contrato_createPage.html', context)


# Abastecimentos

@login_required
def abastecimento_list(request):
    # Todos os Abastecimentos
    abastecimentos = Abastecimento.objects.all()

    # Paginação para as tabelas de Abastecimentos
    paginator = Paginator(abastecimentos, 5)
    page = request.GET.get('page')
    abastecimentos_page = paginator.get_page(page)

    # Dashbord
    dia = datetime.date.today()
    mes = datetime.date.today().month
    ano = datetime.date.today().year

    # Dia
    total_dia = 0
    for abastecimento in Abastecimento.objects.filter(data=dia):
        for item in Item_Abastecimento.objects.filter(abastecimento=abastecimento):
            total_dia += item.quantidade_combustivel * item.valor_unitario

    # Mês
    total_mes = 0
    for abastecimento in Abastecimento.objects.filter(data__month=mes):
        for item in Item_Abastecimento.objects.filter(abastecimento=abastecimento):
            total_mes += item.quantidade_combustivel * item.valor_unitario

    # Ano
    total_ano = 0
    for abastecimento in Abastecimento.objects.filter(data__year=ano):
        for item in Item_Abastecimento.objects.filter(abastecimento=abastecimento):
            total_ano += item.quantidade_combustivel * item.valor_unitario

    context = {'abastecimentos_page': abastecimentos_page, 'dia': dia, 'total_dia': total_dia, 'mes': mes,
               'total_mes': total_mes, 'ano': ano, 'total_ano': total_ano}
    return render(request, 'abastecimento/abastecimento_list.html', context)


@login_required
def abastecimento_createPage(request):
    # Formulário para criação dos abastecimentos
    form = AbastecimentoForm()

    context = {'form': form}
    return render(request, 'abastecimento/abastecimento_createPage.html', context)


@login_required
def abastecimento_create(request):
    if request.method == 'POST':
        form = AbastecimentoForm(request.POST)

        if form.is_valid():
            abastecimento = form.save(commit=False)

            if abastecimento.valor <= abastecimento.contrato.valor_atual:
                abastecimento.save()
                return redirect('abastecimento_edit', abastecimento_id=abastecimento.id)
            else:
                return HttpResponseNotFound(
                    '<p>Valor do abastecimento Superior ao saldo do contrato</p>')
    else:
        form = AbastecimentoForm()

        context = {'form': form}
        return render(request, 'abastecimento/abastecimento_createPage.html', context)


@login_required
def abastecimento_edit(request, abastecimento_id):
    abastecimento = Abastecimento.objects.get(id=abastecimento_id)

    # Formulário Abastecimento
    form = AbastecimentoForm(instance=abastecimento)

    # Formulário ‘Item’ Abastecimento
    item_form = Item_AbastecimentoForm()
    # Itens
    itens_abastecimento = Item_Abastecimento.objects.filter(abastecimento=abastecimento)

    # Paginação para as tabelas de Itens
    paginator = Paginator(itens_abastecimento, 5)
    page = request.GET.get('page')
    itens_page = paginator.get_page(page)

    # Valor total dos itens
    y = 0
    for item in itens_abastecimento:
        x = item.quantidade_combustivel * item.valor_unitario
        y += x

    context = {'abastecimento': abastecimento, 'form': form, 'item_form': item_form, 'itens_page': itens_page, 'y': y}
    return render(request, 'abastecimento/abastecimento_edit.html', context)


# Faltou a verificação do saldo do contrato
@login_required
def abastecimento_update(request, id):
    abastecimento = Abastecimento.objects.get(id=id)
    valor_anterior = abastecimento.valor

    if request.method == 'POST':
        form = AbastecimentoForm(request.POST, instance=abastecimento)

        if form.is_valid():
            abastecimento_upd = form.save(commit=False)
            if abastecimento.item.exists():
                if valor_anterior <= abastecimento_upd.valor <= abastecimento.contrato.valor_atual:
                    abastecimento.save()
                    return redirect('abastecimento_edit', abastecimento_id=abastecimento.id)
                else:
                    return HttpResponseNotFound(
                        '<p>Valor menor que o total dos itens ou superior ao saldo do contrato</p>')
            else:
                if abastecimento.contrato.valor_atual >= abastecimento_upd.valor:
                    abastecimento_upd.save()
                    return redirect('abastecimento_edit', abastecimento_id=abastecimento.id)
                else:
                    return HttpResponseNotFound(
                        '<p>Valor do abastecimento maior que o total do contrato</p>')
    else:
        form = AbastecimentoForm()
        item_form = Item_AbastecimentoForm()
        context = {'form': form, 'item_form': item_form}
        return render(request, 'abastecimento/abastecimento_edit.html', context)


@login_required
def abastecimento_delete(request, id):
    abastecimento = Abastecimento.objects.get(id=id)

    if abastecimento.item.exists():
        return HttpResponseNotFound(
            '<p>Abasteciemnto com Itens</p>')
    else:
        abastecimento.delete()
        return redirect(abastecimento_list)


# Itens Abastecimento

@login_required
def item_create(request, abastecimento_id):
    abastecimento = Abastecimento.objects.get(id=abastecimento_id)

    if request.method == 'POST':
        form_item = Item_AbastecimentoForm(request.POST)

        if form_item.is_valid():
            item_abastecimento = form_item.save(commit=False)

            print(item_abastecimento.veiculo.unidade, abastecimento.contrato.unidade)

            if item_abastecimento.veiculo.unidade == abastecimento.contrato.unidade:
                # Itens do abastecimento
                itens_abastecimento = Item_Abastecimento.objects.filter(abastecimento=abastecimento)

                y = 0
                for item in itens_abastecimento:
                    y += item.quantidade_combustivel * item.valor_unitario

                w = item_abastecimento.quantidade_combustivel * item_abastecimento.valor_unitario

                if y + w <= abastecimento.valor and w <= abastecimento.valor:
                    # Salva o item vinculando o mesmo ao abastecimento
                    item_abastecimento.abastecimento = abastecimento
                    item_abastecimento.save()

                    # Abater do saldo contrato
                    contrato = abastecimento.contrato
                    contrato.valor_atual -= w
                    contrato.save()

                    return redirect('abastecimento_edit', abastecimento_id=abastecimento_id)
                else:
                    return HttpResponseNotFound(
                        '<p>Valor dos itens do abastecimento superior ao total do Abastecimento</p>')
            else:
                return HttpResponseNotFound(
                    '<p>Unidade Orçamentária do veículo diferente do Contrato</p>')
    else:
        form = AbastecimentoForm()
        item_form = Item_AbastecimentoForm()

        context = {'form': form, 'item_form': item_form}
        return render(request, 'abastecimento/abastecimento_edit.html', context)


@login_required
def item_delete(request, id):
    item_abastecimento = Item_Abastecimento.objects.get(id=id)

    # Atualiza o saldo do contrato
    contrato = item_abastecimento.abastecimento.contrato
    contrato.valor_atual += item_abastecimento.valor_unitario * item_abastecimento.quantidade_combustivel
    contrato.save()

    # Deleta
    item_abastecimento.delete()

    return redirect('abastecimento_edit', abastecimento_id=item_abastecimento.abastecimento.id)


@has_permission_decorator('update')
def update_createPage(request):
    form = UpdateForm()

    context = {'form': form}
    return render(request, 'update/update_createPage.html', context)


@has_permission_decorator('update')
def update_create(request):

    if request.method == 'POST':
        form = UpdateForm(request.POST)

        if form.is_valid():
            update = form.save(commit=False)
            update.autor = request.user
            update.save()
            return redirect(update_createPage)
    else:
        form = UpdateForm()

        context = {'form': form}
        return render(request, 'update/update_createPage.html', context)