from django import forms

from abastecimento.models import Unidade_Orcamentaria, Veiculo, Contrato, Abastecimento, Item_Abastecimento, Update


class UnidadeForm(forms.ModelForm):
    class Meta:
        model = Unidade_Orcamentaria
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            widget.attrs.update({'class': 'form-control'})


class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            widget.attrs.update({'class': 'form-control'})


class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        exclude = ['valor_atual']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            widget.attrs.update({'class': 'form-control'})


class AbastecimentoForm(forms.ModelForm):
    class Meta:
        model = Abastecimento
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            widget.attrs.update({'class': 'form-control'})


class Item_AbastecimentoForm(forms.ModelForm):
    class Meta:
        model = Item_Abastecimento
        exclude = ['abastecimento']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            widget.attrs.update({'class': 'form-control'})


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Update
        exclude = ['autor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            widget.attrs.update({'class': 'form-control'})
