from django.shortcuts import render
from django.http import HttpResponseRedirect
from portal.forms import *
from django.contrib.auth import authenticate, login, logout
from portal.models import *
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime

# Create your views here.

DUE_DATE = datetime(2014, 9, 14, 18, 0, 0)
DUE_DATE_STR = DUE_DATE.strftime("%A, <br> %B %d %I:%M%p").lstrip("0").replace(" 0", " ")

def index_view(request):
	data = {'DUE_DATE' : DUE_DATE_STR}
	
	if request.user.is_authenticated():
		return HttpResponseRedirect("/application")

	return render(request, 'index.html', data)

def application_view(request, splash=False):

	if datetime.now() > DUE_DATE:
		return HttpResponseRedirect("/closed")

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/login")

	if request.user.username == "webmaster":
		return HttpResponseRedirect("/gallery")
		
	data = {'DUE_DATE' : DUE_DATE_STR}
	rushee = Rushee.objects.get(user=request.user)
	if splash:
		data['splash'] = True
		data['rushee'] = rushee
		form = NewRusheeForm(initial={'first_name' : rushee.first_name, 
									  'last_name' : rushee.last_name,
									  'phone_num' : rushee.phone_num,
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

	if request.method == 'POST':
		form = NewRusheeForm(request.POST, request.FILES)
		if form.is_valid():
			cd = form.cleaned_data
			rushee = Rushee.objects.get(user=request.user)
			rushee.first_name = cd['first_name']
			rushee.last_name = cd['last_name']
			rushee.phone_num = cd['phone_num']
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
			return application_view(request, splash=True)
		else:
			rushee = Rushee.objects.get(user=request.user)
			data['rushee'] = rushee
			form = NewRusheeForm(request.POST, request.FILES, 
								 initial={'phone_num' : rushee.phone_num,
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
		data['rushee'] = rushee
		form = NewRusheeForm(initial={'first_name' : rushee.first_name, 
									  'last_name' : rushee.last_name,
									  'phone_num' : rushee.phone_num,
									  'dorm' : rushee.dorm,
									  'grad_class' : rushee.grad_class,
									  'major' : rushee.major,
									  'gpa' : rushee.gpa,
									  'q1' : rushee.q1, 
									  'q2' : rushee.q2,
									  'q3' : rushee.q3,
									  'q4' : rushee.q4})	
	data["form"] = form
	data['rushee'] = rushee
	return render(request, 'application.html', data, context_instance=RequestContext(request))

def login_view(request):
	data = {'DUE_DATE' : DUE_DATE_STR}
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
					data['form'] = form
			else: 
				data['error'] = "Your email and password don't match!"
				data['form'] = form
				return render(request,'login.html', data, context_instance=RequestContext(request))
	data['form'] = LoginForm()
	return render(request,'login.html', data, context_instance=RequestContext(request))

def signup_view(request):

	if datetime.now() > DUE_DATE:
		return HttpResponseRedirect("/closed")

	data = {'DUE_DATE' : DUE_DATE_STR}
	if request.method == 'POST':
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
	data = {'DUE_DATE' : DUE_DATE_STR}
	data['rushees'] = Rushee.objects.all()
	return render(request, 'gallery.html', data)

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

@user_passes_test(lambda u: u.is_superuser)
def rushee_view(request, rushee_id):
	data = {'DUE_DATE' : DUE_DATE_STR}
	data['rushee'] = Rushee.objects.get(id=rushee_id)
	return render(request, 'rushee.html', data)

def closed_view(request):
	data = {'DUE_DATE' : DUE_DATE_STR}
	return render(request, 'closed.html', data)