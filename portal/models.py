from django.db import models
from django.contrib.auth.models import User
from django.template import RequestContext


# Create your models here.

class ContentTypeRestrictedFileField(models.FileField):
	def __init__(self, *args, **kwargs):
	    self.content_types = kwargs.pop("content_types")
	    self.max_upload_size = kwargs.pop("max_upload_size")

	    super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

	def clean(self, *args, **kwargs):        
	    data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)

	    file = data.file
	    try:
	        content_type = file.content_type
	        if content_type in self.content_types:
	            if file._size > self.max_upload_size:
	                raise forms.ValidationError(_('Please keep filesize under %s. Current filesize %s') % (filesizeformat(self.max_upload_size), filesizeformat(file._size)))
	        else:
	            raise forms.ValidationError(_('Filetype not supported.'))
	    except AttributeError:
	        pass        

	    return data

class Rushee(models.Model):
	user = models.OneToOneField(User)
	first_name = models.CharField(max_length=40, blank=True, null=True)
	last_name = models.CharField(max_length=40, blank=True, null=True)
	phone_num = models.CharField(max_length=10, blank=True, null=True)
	dorm = models.CharField(max_length=40, blank=True, null=True)
	grad_class = models.CharField(max_length=4, blank=True, null=True)
	major = models.CharField(max_length=100, blank=True, null=True)
	gpa = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
	picture = models.ImageField(upload_to="rushpics", blank=True, null=True)
	resume = ContentTypeRestrictedFileField(upload_to="rushresumes", 
		  								    content_types=['application/pdf'],
											max_upload_size=26214400,
											blank=True,
											null=True)
	q1 = models.TextField(blank=True, null=True)
	q2 = models.TextField(blank=True, null=True)
	q3 = models.TextField(blank=True, null=True)
	q4 = models.TextField(blank=True, null=True)