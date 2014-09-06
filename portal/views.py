from django.shortcuts import render
from django.http import HttpResponseRedirect
from portal.forms import *
from django.contrib.auth import authenticate, login, logout
from portal.models import *
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

def index_view(request):
	data = {}
	return render(request, 'index.html', data)

def application_view(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")

	if request.user.username == "webmaster":
		return HttpResponseRedirect("/gallery")
		
	data = {}

	if request.method == 'POST':
		form = NewRusheeForm(request.POST, request.FILES)
		if form.is_valid():
			cd = form.cleaned_data
			rushee = Rushee.objects.get(user=request.user)
			rushee.phone_num = cd['phone_num']
			rushee.dorm = cd['dorm']
			rushee.grad_class = cd['grad_class']
			rushee.major = cd['major']
			rushee.gpa = cd['gpa']
			rushee.q1 = cd['q1']
			rushee.q2 = cd['q2']
			rushee.q3 = cd['q3']
			rushee.q4 = cd['q4']
			rushee.picture = cd['picture']
			rushee.resume = cd['resume']
			rushee.save()
			return HttpResponseRedirect("/application")
		else:
			rushee = Rushee.objects.get(user=request.user)
			form = NewRusheeForm(initial={'phone_num' : rushee.phone_num,
										  'dorm' : rushee.dorm,
										  'grad_class' : rushee.grad_class,
										  'major' : rushee.major,
										  'gpa' : rushee.gpa,
										  'q1' : rushee.q1, 
										  'q2' : rushee.q2,
										  'q3' : rushee.q3,
										  'q4' : rushee.q4})
	else:
		rushee = Rushee.objects.get(user=request.user)
		form = NewRusheeForm(initial={'phone_num' : rushee.phone_num,
									  'dorm' : rushee.dorm,
									  'grad_class' : rushee.grad_class,
									  'major' : rushee.major,
									  'gpa' : rushee.gpa,
									  'q1' : rushee.q1, 
									  'q2' : rushee.q2,
									  'q3' : rushee.q3,
									  'q4' : rushee.q4})	
	data["form"] = form
	return render(request, 'application.html', data, context_instance=RequestContext(request))

def login_view(request):
	data = {}
	if request.user.is_authenticated():
		return HttpResponseRedirect("/application")
	else:
		if request.method == 'POST':
			form = LoginForm(request.POST)
			if form.is_valid():
				cd = form.cleaned_data
				username = cd['username']
				password = cd['password']
				user = authenticate(username=username, password=password)
				if user is not None:
					login(request, user)
					return HttpResponseRedirect("/application/")
				else: 
					data['error'] = "Your email and password don't match!"
					data['form'] = LoginForm()
		else:
			data['form'] = LoginForm()
	return render(request,'login.html', data, context_instance=RequestContext(request))

def signup_view(request):
	data = {}
	form = NewUserForm(request.POST)
	if form.is_valid():
		new_user = form.save()
		print form.cleaned_data['password1']
		new_rushee = Rushee(user=new_user)
		new_rushee.save()
		new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
		if new_user is not None:
			new_user.backend = 'django.contrib.auth.backends.ModelBackend'
			login(request, new_user)		
			return HttpResponseRedirect("/application")
	else:
		form = NewUserForm()
	data["form"] = form
	return render(request, 'signup.html', data, context_instance=RequestContext(request))

@user_passes_test(lambda u: u.is_superuser)
def gallery_view(request):
	data = {}
	data['rushees'] = Rushee.objects.all()
	return render(request, 'gallery.html', data)