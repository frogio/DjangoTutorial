from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import Question, Answer, Comment
from ..forms import CommentForm


@login_required(login_url = "common:login")
def comment_create_question(request, question_id):
	question = get_object_or_404(Question, pk = question_id)
	if(request.method == "POST"):
		form = CommentForm(request.POST)
		if(form.is_valid()):
			comment = form.save(commit=False)
			comment.author = request.user
			comment.create_date = timezone.now()
			comment.question = question
			comment.save()
			return redirect('{}#comment_{}'.format(resolve_url('pybo:detail', question_id=comment.question.id), comment.id))
	else:
		form = CommentForm()
	context = {'form' : form}
	
	return render(request, 'pybo/comment_form.html', context)
	
	
@login_required(login_url = "common:login")	
def comment_modify_question(request, comment_id):
	comment = get_object_or_404(Comment, pk=comment_id)
	# DB에 있는 내용을 불러온 뒤

	if(request.user != comment.author):
		messages.error(request, "댓글 수정 권한이 없습니다.")
		return redirect('pybo:detail', question_id=comment.question.id)
	
	if(request.method == "POST"):
		# request.POST => 사용자 폼에서 입력받은 content 내용만 db에서 불러온 내용에 덮어씌운다.(instance 객체는 테이블의 한 레코드값들을 가지고 있다.)
		form = CommentForm(request.POST, instance=comment)
		
		if(form.is_valid()):
			comment = form.save(commit=False)
			# 변경된 content 값을 save한다, 단 commit이 False이므로 db에는 기록되지 않는다.
			comment.author = request.user
			comment.modify_date = timezone.now()
			# 직접 변경해야하는 나머지 값들을 변경하고
			comment.save()
			# db에 기록한다
			return redirect('{}#comment_{}'.format(resolve_url('pybo:detail', question_id=comment.question.id), comment.id))			
			
	else:		# 처음 링크를 타고 들어올 떄 GET으로 입력받음
		form = CommentForm(instance=comment)
				# DB로 불러왔던 내용을 초기값으로 설정한다.
	context = {'form' : form}
	return render(request, 'pybo/comment_form.html', context)
	
	
@login_required(login_url = "common:login")	
def comment_delete_question(request, comment_id):
	comment = get_object_or_404(Comment, pk=comment_id)
	
	if(request.user != comment.author):
		message.error(request,"댓글 삭제 권한이 없습니다.")
		return redirect('pybo:detail', qusetion_id=comment.question.id)
	else:
		comment.delete()
		# db에서 삭제한다(db에서만)
		
	return redirect('pybo:detail', question_id = comment.question.id)
		# db에서 지워졌지만, 메모리엔 계속 남은 상태.
	
	# pybo:detail/pybo/question_id로 리다이렉트 한다.
	
	# comment.question.id는 라우트 변수명
	# 따라서 redirect 위치는 pybo:detail/3/
	# 템플릿에서는 {% url 'pybo_detail' id %}
	
	
@login_required(login_url = "common:login")
def comment_create_answer(request, answer_id):
	answer = get_object_or_404(Answer, pk= answer_id)
	
	if(request.method == "POST"):
		form = CommentForm(request.POST)
		if(form.is_valid()):
			comment = form.save(commit=False)
			comment.author = request.user
			comment.create_date = timezone.now()
			comment.answer = answer
			comment.save()
			return redirect('{}#comment_{}'.format(resolve_url('pybo:detail', question_id=comment.answer.question.id), comment.id))
				# pybo:detail/pybo/question_id로 리다이렉트 한다.
	else:
		form = CommentForm()
		
	context = {'form' : form}
	return render(request, 'pybo/comment_form.html', context)
	
	
@login_required(login_url = "common:login")
def comment_modify_answer(request, comment_id):
	comment = get_object_or_404(Comment, pk= comment_id)
	
	if(request.method == "POST"):
		form = CommentForm(request.POST, instance=comment)
		if(form.is_valid()):
			comment = form.save(commit=False)
			comment.author = request.user
			comment.modify_date = timezone.now()
			comment.save()
			return redirect('{}#comment_{}'.format(resolve_url('pybo:detail', question_id=comment.answer.question.id), comment.id))
			
	else:
		form = CommentForm(instance=comment)
		
	context = {'form' : form}
	return render(request, 'pybo/comment_form.html', context)

	
@login_required(login_url = "common:login")
def comment_delete_answer(request, comment_id):
	comment = get_object_or_404(Comment, pk=comment_id)
	
	if(request.user != comment.author):
		message.error(request,"댓글 삭제 권한이 없습니다.")
		return redirect('pybo:detail', qusetion_id=comment.question.id)
	else:
		comment.delete()
		
	return redirect('pybo:detail', question_id = comment.answer.question.id)