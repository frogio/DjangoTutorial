from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.views import generic

from ..models import Question

def index(request):
	page = request.GET.get('page', '1')
	
	# GET메시지를 받아옴
	kw = request.GET.get("kw", "")
	so = request.GET.get("so", "recent")
	
	if(so == "recommend"):
		question_list = Question.objects.annotate(
			num_voter=Count('voter')).order_by('-num_voter','-create_date')
		
	elif(so == "popular"):
		question_list = Question.objects.annotate(
			num_answer=Count('answer')).order_by('-num_answer','-create_date')
		
	else: question_list = Question.objects.order_by('-create_date')
	# 모든 Question 레코드를 가져온다.
	
	# 검색 키워드값에 값이 존재할 경우, 필터를 통해 조건에 맞는 내용을 가져온다.
	if(kw):
		question_list = question_list.filter(
			Q(subject__icontains=kw) |
			Q(content__icontains=kw) |
			Q(author__username__icontains=kw)|
			Q(answer__author__username__icontains=kw)
		).distinct()
	
	
	paginator = Paginator(question_list, 10)
	# 가져온 Question_list 목록에서 10개씩 나눠 페이지를 만든다.
	
	page_obj = paginator.get_page(page)
	# page 번째의 레코드를 가져온다.
		#for answer in :
	#	print(answer,end =' ')
	
	context = {'page_obj' : page_obj,
				'page' : page,
				'kw' : kw,
				'so' : so}
	
	return render(request, 'pybo/question_list.html', context)
	# context 딕셔너리는 템플릿으로 넘어가 키 값으로 데이터를 참조할 수 있다.
	
def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	# 요청한 question 객체를 가져온다
	
	recommend_list = []
	
	idx = 0
	# 유저가 추천을 체크한 답변의 인덱스를 확인한다.
	for answer in question.answer_set.all():							# 로그인된 유저의 답변 추천 체크 목록을 만들어낸다.
		if(answer.voter.filter(pk=request.user.id).exists()):			
			recommend_list.append(idx)									# 답변의 순서는 0부터 시작하고, 체크가 되어있을 경우 해당 답변의 인덱스를 추가한다.
		idx += 1

	answer_idx_str = '//'.join([str(i) for i in recommend_list])		# 리스트를 자바스크립트에서 받을 수 있게 // 토큰으로 리스트 값들을 연결해
																		# 하나의 문자열로 만든다. 후에 자바스크립트에서 //토큰을 기준으로 split하여
																		# 추천 체크 배열을 만든다.
		
	context = {'question' : question,
				'answer_is_liked' : answer_idx_str}						# template에 context 객체를 보낸다. answer_is_liked은 리스트를 문자열로 변환한 변수이다.

	if(request.user.is_authenticated == True and question.voter.filter(pk=request.user.id).exists()):			# 질문에 요청한 유저의 추천이 체크되어 있을 경우
			context['question_is_liked'] = True
	
	else: context['question_is_liked'] = False
	

	return render(request, 'pybo/question_detail.html', context)
	# render함수는 request객체에 context객체를 추가하여 리턴한다. (요청 정보(요청자) + 데이터)