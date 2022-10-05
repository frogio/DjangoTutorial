from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import Question
from ..forms import QuestionForm

@login_required(login_url='common:login')
def question_create(request):
	
	if(request.method == 'POST'):		# POST 요청으로 호출됨 (DB 등록)
		form = QuestionForm(request.POST)
		if(form.is_valid()):
			question = form.save(commit=False)
			question.author = request.user
			question.create_date = timezone.now()
			question.save()
			
			return redirect('pybo:index')
		
	else:								# GET 요청으로 호출됨 (HTML 생성)
		form = QuestionForm()

	return render(request, 'pybo/question_form.html', {'form' : form})

@login_required(login_url='common:login')
def question_modify(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	
	if(request.user != question.author):
		message.error(request, "수정 권한이 없습니다.")
		return redirect('pybo:detail', question_id=question_id)
	
	if request.method == "POST":
# 질문 수정을 위해 값 덮어쓰기
		form = QuestionForm(request.POST, instance=question)
		if form.is_valid():
			question = form.save(commit=False)
			question.author = request.user
			question.modify_date = timezone.now() # 수정일시 저장
			question.save()
			return redirect('pybo:detail', question_id=question.id)
	else:
	# 질문 수정 화면에 기존 제목, 내용 반영
		form = QuestionForm(instance=question)
	context = {'form': form}
	return render(request, 'pybo/question_form.html', context)
	
@login_required(login_url='common:login')
def question_delete(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	
	if(request.user != question.author):
		message.error(request, "삭제권한이 없습니다.")
		return redirect('pybo:detail', question_id=question.id)
		
	question.delete()
	return redirect('pybo:index')	
	