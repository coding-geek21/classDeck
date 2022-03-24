from django.urls import include, path
from django import urls
from django.contrib import admin
from .views import classroom, students, teachers
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('acc/', include('allauth.urls')),
    path('', classroom.home, name='home'),


    path('students/', include(([
        path('', students.HomeView.as_view(), name='student_home'),
        path('viewquiz', students.QuizListView.as_view(), name='quiz_list'),
        path('interests/', students.StudentInterestsView.as_view(), name='student_interests'),
        path('taken/', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
        path('quiz/<int:pk>/', students.take_quiz, name='take_quiz'),
        path('assignment/', students.AssignmentListView.as_view(), name='assignment_list'),
        path('activate/<uidb64>/<token>/',students.VerificationView.as_view(),name="activate")

       
    ], 'classroom'), namespace='students')),

    path('teachers/', include(([
        path('', teachers.HomeView.as_view(), name='teacher_home'),

        path('assignment/', teachers.AssignmentListView.as_view(),name='assignment_list'),
        path('assignment/add/<int:pk>', teachers.CreateAssignmentView.as_view(),name='assignment_add'),
        path('assignment/<int:pk>/', teachers.AssignmentView.as_view(),name='assignment'),
        path('response/<int:pk>/', teachers.ResponseView.as_view(),name='response'),

        path('quiz/', teachers.QuizListView.as_view(), name='quiz_change_list'),
        path('quiz/add/', teachers.QuizCreateView.as_view(), name='quiz_add'),
        path('quiz/<int:pk>/', teachers.QuizUpdateView.as_view(), name='quiz_change'),
        path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(), name='quiz_results'),
        path('quiz/<int:pk>/question/add/', teachers.question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
        
        path('/activate/<uidb64>/<token>/',teachers.VerificationView.as_view(),name="activate")
    ], 'classroom'), namespace='teachers')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)