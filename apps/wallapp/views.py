from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Post, Comment
import bcrypt

def login(request):
	return render(request, "wallapp/index.html")

# Login Redirects:

def registration(request):
	errors = User.objects.registration_validator(request.POST)
	request.session.flush()
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	else:
		password = request.POST['password']
		pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
		User.objects.create(firstname = request.POST['fname'], lastname = request.POST['lname'], email = request.POST['email'], password = pw_hash)
		validuser = User.objects.get(email = request.POST['email'])
		request.session["validuser_email"] = validuser.email
		request.session["validuser_firstname"] = validuser.firstname
		request.session["validuser_lastname"] = validuser.lastname
		request.session["validuser_id"] = validuser.id
		return redirect('/wall')

def login_check(request):
	errors = User.objects.login_validator(request.POST)
	request.session.flush()
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	validuser = User.objects.get(email = request.POST['email'])
	request.session["validuser_email"] = validuser.email
	request.session["validuser_firstname"] = validuser.firstname
	request.session["validuser_lastname"] = validuser.lastname
	request.session["validuser_id"] = validuser.id
	return redirect ('/wall')

def logout(request):
	request.session.flush()
	return redirect("/")

# Wall renders:

def success(request):
	if "validuser_id" not in request.session:
		return redirect("/")
	context = {
			"all_posts": Post.objects.all().order_by('-created_at'),
			"comments": Comment.objects.all().order_by('-created_at')
		}
	return render(request, "wallapp/wall.html", context)

# Wall redirects:

def submit_post(request):
	errors = Post.objects.post_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/wall')
	Post.objects.create(title=request.POST['posttitle'], content=request.POST['postcontent'], poster=User.objects.get(id=request.session['validuser_id']))
	return redirect('/wall')

def submit_comment(request, num):
	errors = Comment.objects.comment_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/wall')
	Comment.objects.create(content=request.POST['commentcontent'], commenter=User.objects.get(id=request.session['validuser_id']), parent=Post.objects.get(id = num))
	return redirect('/wall')

def delete_post(request, num):
	post = Post.objects.get(id = num)
	if request.session["validuser_id"] == post.poster.id:
		post.delete()
		return redirect('/wall')
	return redirect('/wall')