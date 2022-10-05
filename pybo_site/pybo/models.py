from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Question : Answer = 1 : N

# 클래스 이름이 테이블 명
class Question(models.Model):
	# 자동으로 Primary Key와 Auto Increment 가 자동으로 추가됨	
	author = models.ForeignKey(User, on_delete = models.CASCADE, related_name='author_question')
	subject = models.CharField('제목' ,max_length = 200)			# CharField : VARCHAR
	content = models.TextField('내용')							# TextField : Text
	create_date = models.DateTimeField('생성일')					# DateTimeField : Date
	modify_date = models.DateTimeField(null=True, blank=True)
	voter = models.ManyToManyField(User, related_name='voter_question')
	# 속성 명이 컬럼 명이 됨

	def __str__(self):
		return f'({self.id}) {self.subject}'


	
class Answer(models.Model):
	author = models.ForeignKey(User, on_delete = models.CASCADE, related_name="author_answer")
	question = models.ForeignKey(Question, verbose_name='질문', on_delete=models.CASCADE) # Question 테이블 명의 id를 참조하는 Foreign Key
	content = models.TextField('답변 내용')
	create_date = models.DateTimeField('생성일')
	modify_date = models.DateTimeField(null=True, blank=True)
	voter = models.ManyToManyField(User, related_name='voter_answer')
	
	def __str__(self):
		return f'({self.id}) {self.content}'

class Comment(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	create_date = models.DateTimeField()
	modify_date = models.DateTimeField(null=True, blank=True)
	question = models.ForeignKey(Question, null=True, blank=True, on_delete = models.CASCADE)
	answer = models.ForeignKey(Answer, null=True, blank=True, on_delete = models.CASCADE)
	
	def __str__(self):
		return f'({self.id}) {self.content}'
	
	