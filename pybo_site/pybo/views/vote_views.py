from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import Question, Answer

@login_required(login_url='common:login')
def vote_question(request, question_id):
	question = get_object_or_404(Question, pk=question_id)

	if(request.user == question.author):
		messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
	
	else:
		if(question.voter.filter(pk=request.user.pk).exists()):			# voter 테이블에 추천한 기록이 존재할 경우
			question.voter.remove(request.user)							# voter 추천 기록을 지운다.	(중복 추천 방지)
		
		else:
			question.voter.add(request.user)							# 추천 기록이 없을 경우 테이블에 레코드를 삽입한다.
			
	
	return redirect('pybo:detail', question_id=question_id)

@login_required(login_url='common:login')
def vote_answer(request, answer_id):
	answer = get_object_or_404(Answer, pk=answer_id)
	
	if(request.user == answer.author):
		messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
	
	else:
		if(answer.voter.filter(pk=request.user.pk).exists()):		# voter 테이블에 추천한 기록이 존재할 경우
			answer.voter.remove(request.user)                		# voter 추천 기록을 지운다.	(중복 추천 방지)
		else:                                                
			answer.voter.add(request.user)							# 추천 기록이 없을 경우 테이블에 레코드를 삽입한다.	
	
	return redirect('pybo:detail', question_id=answer.question.id)