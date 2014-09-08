from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from portal.models import *

class NewUserForm(UserCreationForm):
	username = forms.CharField(label="Email", widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'signup-field'}))

	class Meta:
 		model = User
		fields = ("username", )

class NewRusheeForm(forms.Form):
	# keep these in the tope of the code
	q1 = forms.CharField(required=False, widget=forms.Textarea, label="Why do you want to be a member of Alpha Kappa Psi?")
	q2 = forms.CharField(required=False, widget=forms.Textarea, label="Describe something meaningful you took away from a recruitment event or an interaction with a brother that makes you want to be a part of Alpha Kappa Psi.")
	q3 = forms.CharField(required=False, widget=forms.Textarea, label="What is your business interest and what have you done so far to further that interest?")
	q4 = forms.CharField(required=False, widget=forms.Textarea, label="(Optional) If there is additional information that you would like to share with us, please include it here- interesting facts, miscellaneous thoughts, experiences, or talents are welcome.")
	picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'id': 'imgInp'}))
	first_name = forms.CharField(required=False, label="First Name", widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'question-primary'}))
	last_name = forms.CharField(required=False, label="Last Name", widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'question-primary'}))
	phone_num = forms.CharField(required=False, label="Phone", widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'question-primary'}))
	dorm = forms.CharField(required=False)
	grad_class = forms.CharField(required=False, label="Graduation Year", widget=forms.TextInput(attrs={'placeholder': 'Graduation Year', 'class': 'question-primary'}))
	major = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Major', 'class': 'question-primary'}))
	gpa = forms.CharField(required=False, label="Cumulative GPA", widget=forms.TextInput(attrs={'placeholder': 'Cumulative GPA', 'class': 'question-primary'}))
	
	
	resume = forms.FileField(required=False, widget=forms.FileInput(attrs={'class': 'hidden', 'id' : 'image'}))

class LoginForm(forms.Form):
    username = forms.CharField(label="Email", widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'signup-field'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'signup-field'}))
