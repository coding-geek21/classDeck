from tkinter.tix import Tree
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView,TemplateView)
from django.views import View
from ..decorators import teacher_required
from ..forms import BaseAnswerInlineFormSet, QuestionForm, TeacherSignUpForm
from ..models import Answer, Question, Quiz, User, Assignment, Subject, AssignmentSubmission
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from ..utils import token_generator
from django.shortcuts import render
from django import forms
from django.contrib.sites.models import Site
from django.views.decorators.clickjacking import xframe_options_sameorigin
from .notification import send_notification


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        userEmail=user.email
        print(user.email)
        user.is_active=False
        user.save()
      
        email_subject="Activate your account"
       
        # path to view
        # - getting domain we are on
        # -relative url to verification
        # -encode uid
        # -token
        
        uidb64=urlsafe_base64_encode(force_bytes(user.pk))
        current_site = Site.objects.get_current()
        # domain=current_site.domain
        domain='localhost:8000'
        # domain = Site.objects.get_current()
        # domain=get_current_site(self.request).domain
        print(domain)
        link=reverse('activate',kwargs ={'uidb64':uidb64,'token':token_generator.make_token(user)})
        print(link)
        activate_url='http://'+domain+link
        email_body='Hi '+user.username+ ' Please use this link to verify your account\n' + activate_url 

        email = EmailMessage(
    email_subject,
    email_body,
    'noreply@classDeck.com',
    [userEmail],
   
)       
        
        email.send(fail_silently=False)
        messages.success(self.request,"Check your mail to activate your account")
        return render(self.request,'registration/login.html')
        # login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        # return redirect('students:quiz_list')
 


@method_decorator([login_required], name='dispatch')
class HomeView(TemplateView):
    template_name = 'classroom/teachers/teacher_home.html'

@method_decorator([login_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'classroom/teachers/quiz_change_list.html'

    def get_queryset(self):
        queryset = self.request.user.quizzes \
            .select_related('subject') \
            .annotate(questions_count=Count('questions', distinct=True)) \
            .annotate(taken_count=Count('taken_quizzes', distinct=True))
        return queryset


@method_decorator([login_required], name='dispatch')
class QuizCreateView(CreateView):
    model = Quiz
    fields = ('name', 'subject', )
    template_name = 'classroom/teachers/quiz_add_form.html'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.owner = self.request.user
        quiz.save()
        messages.success(self.request, 'The quiz was created with success! Go ahead and add some questions now.')
        return redirect('teachers:quiz_change', quiz.pk)


@method_decorator([login_required], name='dispatch')
class QuizUpdateView(UpdateView):
    model = Quiz
    fields = ('name', 'subject', )
    context_object_name = 'quiz'
    template_name = 'classroom/teachers/quiz_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.quizzes.all()

    def get_success_url(self):
        return reverse('teachers:quiz_change', kwargs={'pk': self.object.pk})


@method_decorator([login_required ], name='dispatch')
class QuizDeleteView(DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'classroom/teachers/quiz_delete_confirm.html'
    success_url = reverse_lazy('teachers:quiz_change_list')

    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, 'The quiz %s was deleted with success!' % quiz.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()


@method_decorator([login_required, teacher_required], name='dispatch')
class AssignmentListView(View):
    def get(self, request):
        context = {'assignments':Assignment.objects.filter(owner=self.request.user)}
        return render(request, 'classroom/teachers/assignment_list.html',context)


@method_decorator([login_required, teacher_required], name='dispatch')
class CreateAssignmentView(View):
    def get(self,request,pk):
        assignment = None
        if pk!=0:
            assignment = Assignment.objects.get(id=pk)
        query = Subject.objects.all()
        return render(request, 'classroom/teachers/assignment_add_form.html',{'subjects':query,'assignment':assignment})
    
    def post(self,request,pk):
        print(pk==0)
        name = request.POST['name']
        subject = Subject.objects.get(id=request.POST['subject'])
        try :
            file = request.FILES['file']
        except:
            file = None
        last_date = request.POST['last_date']
        note = 'No note'
        if request.POST['note']:
            note = request.POST['note']
        print(pk==0)
        if name and subject and last_date:
            print(pk==0)
            if pk==0:
                assignment = Assignment(name=name,subject=subject,file=file,
                                        last_date=last_date,owner=self.request.user,
                                        note=note)
                assignment.save()
                print("here")
                send_notification(assignment)
                
                messages.success(request, 'The assignment was created successfuly !')
                return redirect('teachers:assignment_list') 
            assignment = Assignment.objects.get(id=pk)
            assignment.name = name
            assignment.subject = subject
            assignment.last_date = last_date
            assignment.note = note
            if file:
                assignment.file = file
                assignment.save(update_fields=['name','subject','file','last_date','note'])
            else:
                assignment.save(update_fields=['name','subject','last_date','note'])
            messages.success(request, 'The assignment was updated successfuly !')
            return redirect('teachers:assignment_list')
        messages.error(request, 'Few fields were empty ! Try Again !')
        return redirect('teachers:assignment_list')

@method_decorator([login_required, teacher_required], name='dispatch')
class DeleteAssignmentView(View):
    def get(self,request,pk):
        assignment = Assignment.objects.filter(id=pk)
        if len(assignment)>0:
            assignment[0].delete()
            messages.success(request, 'The assignment was deleted successfuly !')
            return redirect('teachers:assignment_list')
        messages.success(request, 'Oops ! Looks like the assignment was already deleted ')
        return redirect('teachers:assignment_list')

@method_decorator([login_required, teacher_required], name='dispatch')
class AssignmentView(View):
    def get(self,request,pk):
        assignment = Assignment.objects.get(id=pk)
        responses = AssignmentSubmission.objects.filter(assignment=assignment)
        total = len(responses)
        context = {'assignment':assignment, 'responses':responses, 'total':total}
        return render(request, 'classroom/teachers/assignment.html',context)


@method_decorator([login_required, teacher_required], name='dispatch')
class ResponseView(View):
    def get(self,request,pk):
        submission = AssignmentSubmission.objects.get(id=pk)
        return render(request, 'classroom/teachers/assignment_submission.html/',{'response':submission})
    
    def post(self,request,pk):
        assignment = AssignmentSubmission.objects.get(id=pk)
        assignment.score = request.POST['score']
        assignment.remarks = request.POST['remarks']
        assignment.save(update_fields=['score','remarks'])
        messages.success(request, 'The response was scored successfuly !')
        return redirect('teachers:assignment_list') 

@method_decorator([login_required ], name='dispatch')
class QuizResultsView(DetailView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'classroom/teachers/quiz_results.html'

    def get_context_data(self, **kwargs):
        quiz = self.get_object()
        taken_quizzes = quiz.taken_quizzes.select_related('student__user').order_by('-date')
        total_taken_quizzes = taken_quizzes.count()
        quiz_score = quiz.taken_quizzes.aggregate(average_score=Avg('score'))
        extra_context = {
            'taken_quizzes': taken_quizzes,
            'total_taken_quizzes': total_taken_quizzes,
            'quiz_score': quiz_score
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()


@login_required
@teacher_required
def question_add(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, 'You may now add answers/options to the question.')
            return redirect('teachers:question_change', quiz.pk, question.pk)
    else:
        form = QuestionForm()

    return render(request, 'classroom/teachers/question_add_form.html', {'quiz': quiz, 'form': form})

@login_required
@teacher_required
def question_change(request, quiz_pk, question_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk, owner=request.user)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

    AnswerFormSet = inlineformset_factory(
        Question, 
        Answer, 
        formset=BaseAnswerInlineFormSet,
        fields=('text', 'is_correct'),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, 'Question and answers saved with success!')
            return redirect('teachers:quiz_change', quiz.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)

    return render(request, 'classroom/teachers/question_change_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'formset': formset
    })


@method_decorator([login_required   ], name='dispatch')
class QuestionDeleteView(DeleteView):
    model = Question
    context_object_name = 'question'
    template_name = 'classroom/teachers/question_delete_confirm.html'
    pk_url_kwarg = 'question_pk'

    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs['quiz'] = question.quiz
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        question = self.get_object()
        messages.success(request, 'The question %s was deleted with success!' % question.text)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Question.objects.filter(quiz__owner=self.request.user)

    def get_success_url(self):
        question = self.get_object()
        return reverse('teachers:quiz_change', kwargs={'pk': question.quiz_id})




class VerificationView(TemplateView):
    def get(self,request,uidb64,token):
        print('IN')
       
        id=force_text(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=id)

        user.is_active=True
        user.save()
        messages.success(request,"Account activated successfully")
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
         
       

        return render(self.request,'classroom/teachers/teacher_home.html')
  