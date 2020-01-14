from __future__ import unicode_literals
from django.db import models
import re, bcrypt

class UserManager(models.Manager):
	def registration_validator(self, postData):
		errors = {}
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
		if len(postData['fname']) < 2:
			errors["fname"] = "First name ought to be more than 2 characters!"
		if not NAME_REGEX.match(postData['fname']):
			errors["non-fname"] = "Names can only contain letters! Are you a robot?"
		if len(postData['lname']) < 2:
			errors["lname"] = "Come on.. dude. Your last name ought to be more than 2 characters!"
		if not NAME_REGEX.match(postData['lname']):
			errors["non-lname"] = "Last names can also only contain letters!"
		if not EMAIL_REGEX.match(postData['email']):
			errors["email"] = "Invalid email address!"
		if User.objects.filter(email=postData['email']):
			errors["non-unique-user"] = "This email already has an account!"
		if not (postData['password']):
			errors["password"] = "You must have a password!"
		if not postData['password'] == (postData['password_conf']):
			errors["password_match"] = "You password and password confirmation do not match!"
		return errors
		
	def login_validator(self, postData):
		errors = {}
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		if not EMAIL_REGEX.match(postData['email']):
			errors["email"] = "Invalid email address!"
		else:
			if not User.objects.filter(email=postData['email']):
				errors["non-user"] = "This user does not exist!"
			else:
				user = User.objects.get(email=postData['email'])
				if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
					errors['wrongPW'] = "That password does not match that User"
		return errors

class PostManager(models.Manager):
	def post_validator(self, postData):
		errors = {}
		if len(postData['posttitle']) < 1:
			errors["titlelength"] = "Your title cannot be empty!"
		if len(postData['postcontent']) < 1:
			errors["postlength"] = "You don't have anything in your post!"
		return errors
		
class CommentManager(models.Manager):
	def comment_validator(self, postData):
		errors = {}
		if len(postData['commentcontent']) < 1:
			errors["postlength"] = "You don't have anything in your comment!"
		return errors

class User(models.Model):
	firstname = models.CharField(max_length=25)
	lastname = models.CharField(max_length=25)
	email = models.CharField(max_length=25)
	password = models.CharField(max_length=60)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Post(models.Model):
	title = models.CharField(max_length=45)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	poster = models.ForeignKey(User, related_name="posts")
	objects = PostManager()

class Comment(models.Model):
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	commenter = models.ForeignKey(User, related_name="comments")
	parent = models.ForeignKey(Post, related_name="post_comments", null=True)
	objects = CommentManager()