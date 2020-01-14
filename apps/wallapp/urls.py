from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^delete_post/(?P<num>\d+)$', views.delete_post),
	url(r'^submit_comment/(?P<num>\d+)$', views.submit_comment),
	url(r'^submit_post$', views.submit_post),
	url(r'^wall$', views.success),
	url(r'^logout$', views.logout),
	url(r'^validuser$', views.login_check),
	url(r'^validate$', views.registration),
	url(r'^$', views.login),
]