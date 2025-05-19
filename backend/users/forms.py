from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class CreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'first_name',)
