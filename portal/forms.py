from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from portal.models import *
import re
from django.core.exceptions import ValidationError

def is_andrew_email(value):
	a = re.compile("^[a-zA-Z0-9._%+-]+@andrew.cmu.edu$")
	if not a.match(value):
		raise ValidationError("Your email must be an Andrew email.")

def is_valid_phone_num(value):
	a = re.compile("^[0-9]$")
	if len(value) != 10 or not a.match(value):
		raise ValidationError("Your phone number must be 10 digits long.")

def is_valid_grad_class(value):
	a = re.compile("^[0-9]$")
	if len(value) != 4 or not a.match(value):
		raise ValidationError("Your graduating class must be 4 digits long.")

class NewUserForm(UserCreationForm):
	username = forms.CharField(label="Email", widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'signup-field'}), 
								validators=[is_andrew_email])

	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'signup-field'}))
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'signup-field'}), label="Confirm Password")


	class Meta:
 		model = User
		fields = ("username", )

class NewRusheeForm(forms.Form):
	# keep these in the tope of the code
	q1 = forms.CharField(required=False, widget=forms.Textarea, label="Describe your business interests.")
	q2 = forms.CharField(required=False, widget=forms.Textarea, label="Describe something meaningful you took away from a recruitment event or an interaction with a brother that makes you want to be a part of Alpha Kappa Psi.")
	q3 = forms.CharField(required=False, widget=forms.Textarea, label="What specifically do you hope to gain from membership in Alpha Kappa Psi?")
	q4 = forms.CharField(required=False, widget=forms.Textarea, label="Anything else you'd like to add? This is to be used if there is anything else you would like to tell us that we have not asked you about on the application. If you believe that there is some fact, experience, talent, thought, or whatever which just did not seem to fit into our application but which you would like us to take into consideration, let us know about it here. (Optional)")
	picture = forms.ImageField(required=False)
	first_name = forms.CharField(required=True, label="First Name", widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'question-primary'}))
	last_name = forms.CharField(required=True, label="Last Name", widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'question-primary'}))
	phone_num = forms.CharField(required=True, label="Phone", widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'question-primary'}), validators=[is_valid_phone_num])
	dorm = forms.CharField(required=False)
	grad_class = forms.CharField(required=True, label="Graduation Year", widget=forms.TextInput(attrs={'placeholder': 'Graduation Year', 'class': 'question-primary'}), validators=[is_valid_grad_class])
	major = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Major', 'class': 'question-primary'}))
	gpa = forms.CharField(required=True, label="Cumulative GPA", widget=forms.TextInput(attrs={'placeholder': 'GPA', 'class': 'question-primary'}))	
	resume = forms.FileField(required=True, widget=forms.FileInput)

class LoginForm(forms.Form):
    username = forms.CharField(label="Email", widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'signup-field'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'signup-field'}))
