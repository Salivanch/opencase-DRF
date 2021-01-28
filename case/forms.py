from django.forms import ModelForm
from django.forms.widgets import TextInput
from .models import Quality

class QualityForm(ModelForm):
    class Meta:
        model = Quality
        fields = '__all__'
        widgets = {
            'hexcolor': TextInput(attrs={'type': 'color'}),
        }