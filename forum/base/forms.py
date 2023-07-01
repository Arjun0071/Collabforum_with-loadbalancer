from django.forms import ModelForm
from base.models import Room, Feedback, User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email','password1', 'password2' ]

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
         model = User
         fields = [ 'avatar', 'name', 'username', 'email', 'bio']

class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['project_name', 'mail', 'feedback']
        labels = {
            'project_name': 'Enter The Project Name',
            'mail': 'Enter Your Email',
            'feedback': 'Enter Your Feedback',
        }
     