from django.forms import ModelForm

from .models import TODO


class CreateTaskForm(ModelForm):
    class Meta:
        model = TODO
        fields = ['header', 'description']