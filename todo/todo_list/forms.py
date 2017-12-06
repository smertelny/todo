from django.forms import ModelForm, TextInput, Textarea

from .models import TODO


class CreateTaskForm(ModelForm):
    class Meta:
        model = TODO
        fields = ['header', 'description']
        widgets = {
            'header': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control',
                                             'rows': 5}),        }
