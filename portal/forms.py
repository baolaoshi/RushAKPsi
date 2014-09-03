from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from portal.models import *

class NewUserForm(UserCreationForm):
	username = forms.CharField(label="Email")

	class Meta:
 		model = User
		fields = ("username", )

class NewRusheeForm(forms.Form):
	first_name = forms.CharField(required=False, label="First Name")
	last_name = forms.CharField(required=False, label="Last Name")
	phone_num = forms.CharField(required=False, label="Phone")
	dorm = forms.CharField(required=False)
	grad_class = forms.CharField(required=False, label="Graduation Year")
	major = forms.CharField(required=False)
	gpa = forms.CharField(required=False, label="Cumulative GPA")
	q1 = forms.CharField(required=False, widget=forms.Textarea, label="Describe your business interests.")
	q2 = forms.CharField(required=False, widget=forms.Textarea, label="Describe something meaningful you took away from a recruitment event or an interaction with a brother that makes you want to be a part of Alpha Kappa Psi.")
	q3 = forms.CharField(required=False, widget=forms.Textarea, label="What specifically do you hope to gain from membership in Alpha Kappa Psi?")
	q4 = forms.CharField(required=False, widget=forms.Textarea, label="Anything else you'd like to add? This is to be used if there is anything else you would like to tell us that we have not asked you about on the application. If you believe that there is some fact, experience, talent, thought, or whatever which just did not seem to fit into our application but which you would like us to take into consideration, let us know about it here. (Optional)")
	picture = forms.ImageField(required=False)
	resume = forms.FileField(required=False)

class LoginForm(forms.Form):
    username = forms.CharField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput())
