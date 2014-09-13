from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from portal.models import *
import re
from django.core.exceptions import ValidationError

class ExtFileField(forms.FileField):
    """
    Same as forms.FileField, but you can specify a file extension whitelist.

    >>> from django.core.files.uploadedfile import SimpleUploadedFile
    >>>
    >>> t = ExtFileField(ext_whitelist=(".pdf", ".txt"))
    >>>
    >>> t.clean(SimpleUploadedFile('filename.pdf', 'Some File Content'))
    >>> t.clean(SimpleUploadedFile('filename.txt', 'Some File Content'))
    >>>
    >>> t.clean(SimpleUploadedFile('filename.exe', 'Some File Content'))
    Traceback (most recent call last):
    ...
    ValidationError: [u'Not allowed filetype!']
    """
    def __init__(self, *args, **kwargs):
        ext_whitelist = kwargs.pop("ext_whitelist")
        self.ext_whitelist = [i.lower() for i in ext_whitelist]

        super(ExtFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ExtFileField, self).clean(*args, **kwargs)
        filename = data.name
        ext = os.path.splitext(filename)[1]
        ext = ext.lower()
        if ext not in self.ext_whitelist:
            raise forms.ValidationError("Resume must be a PDF file")

def is_andrew_email(value):
	a = re.compile("^[a-zA-Z0-9._%+-]+@andrew.cmu.edu$")
	a2 = re.compile("^[a-zA-Z0-9._%+-]+@cmu.edu$")
	if not (a.match(value) or a2.match(value)):
		raise ValidationError("Your email must be an Andrew email.")

def is_valid_phone_num(value):
	a = re.compile("^[0-9]")
	if len(value) != 10 or not a.match(value):
		raise ValidationError("Your phone number must be 10 digits long.")

def is_valid_grad_class(value):
	a = re.compile("^[0-9]")
	if len(value) != 4 or not a.match(value):
		raise ValidationError("Your graduating class must be 4 digits long.")

def is_valid_question(value):
	if len(value) > 1500:
		raise ValidationError("Please limit your responses to 250 words or less. ")

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
	q1 = forms.CharField(required=False, widget=forms.Textarea, label="Why do you want to be a member of Alpha Kappa Psi?", validators=[is_valid_question])
	q2 = forms.CharField(required=False, widget=forms.Textarea, label="Describe something meaningful you took away from a recruitment event or an interaction with a brother that makes you want to be a part of Alpha Kappa Psi.", validators=[is_valid_question])
	q3 = forms.CharField(required=False, widget=forms.Textarea, label="What is your business interest and what have you done so far to further that interest?", validators=[is_valid_question])
	q4 = forms.CharField(required=False, widget=forms.Textarea, label="(Optional) If there is additional information that you would like to share with us, please include it here- interesting facts, miscellaneous thoughts, experiences, or talents are welcome.", validators=[is_valid_question])
	picture = forms.ImageField(required=True, widget=forms.FileInput(attrs={'id': 'imgInp'}))
	first_name = forms.CharField(required=True, label="First Name", widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'question-primary'}))
	last_name = forms.CharField(required=True, label="Last Name", widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'question-primary'}))
	phone_num = forms.CharField(required=True, label="Phone", widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'question-primary'}), validators=[is_valid_phone_num])
	grad_class = forms.CharField(required=True, label="Graduation Year", widget=forms.TextInput(attrs={'placeholder': 'Graduation Year', 'class': 'question-primary'}), validators=[is_valid_grad_class])
	major = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Major', 'class': 'question-primary'}))
	gpa = forms.CharField(required=True, label="Cumulative GPA", widget=forms.TextInput(attrs={'placeholder': 'GPA', 'class': 'question-primary'}))	
	resume = ExtFileField(required=True, widget=forms.FileInput, ext_whitelist=[".pdf", ])

class LoginForm(forms.Form):
    username = forms.CharField(label="Email", widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'signup-field'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'signup-field'}))
