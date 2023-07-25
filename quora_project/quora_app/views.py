from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.conf import settings
from .forms import QuestionForm,AnswerForm,SignUpForm
from .models import Question, Answer,Like, QuestionCategory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User

from django.contrib.auth import authenticate
from django.contrib import auth


media_url = settings.MEDIA_URL
static = settings.STATIC_URL
LOGIN_URL = settings.LOGIN_URL

def SignupPage(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request,'quora_app/signup.html',{'form':form})


def LoginPage(request):
    passing_dictionary = {
        'media_url': media_url,
    } 
    if request.user.id :
        # send user to dashboard if already logged in 
        return HttpResponseRedirect ('/dashboard')
    if 'successLogout' in request.session:
        # display message of successful logout if exists.
        passing_dictionary ['successLogout'] = 'You are logged out successfully!'
        del request.session['successLogout']
        request.session.modified = True
    if request.method == 'POST':
        # if form is submitted
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username is not "" and password is not "":
            # check credentials
            if '@' in username:
                # user is logging with email
                try:
                    user = User.objects.get(email = username)
                    if user.check_password(password):
                        # Password is correct and user is authenticated
                        print('Password is OK')
                    else:
                        user = None
                        # Password is wrong
                except User.DoesNotExist :
                    #User does not exist with the corresponding email
                    user = None
            else:
                # User is logging with username
                user = authenticate(username= username, password= password)
            if user is not None:
                # Login is success
                auth.login(request, user)
                passing_dictionary ['success'] = 'Woohoo! You are logged in to awesomeness.'
                return HttpResponseRedirect('/dashboard') 
                # return render( request, 'core/template-dashboard.html', passing_dictionary )
            else:
                # There is some error while logging in 
                passing_dictionary ['errors'] = 'Invalid Credentials buddy! Try again.' 
                return render( request, 'accounts/template-login.html', passing_dictionary )
        else:
            # Throw error of empty password
            passing_dictionary ['errors'] = 'Enter valid values.' 
            return render( request, 'accounts/template-login.html', passing_dictionary )
    else:
        return render( request, 'accounts/template-login.html', passing_dictionary )

def Logout(request):
    auth.logout(request) #logout the current user
    request.session['successLogout'] = 'You are now logged out successfully!' #logout message
    return HttpResponseRedirect( LOGIN_URL )


def home(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request,'quora_app/home.html',{'questions':questions})

@login_required
def profile(request):
    username = request.user.username
    email = request.user.email
    return render(request, 'quora_app/profile.html', {'username': username, 'email': email})

@login_required

def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            messages.success(request, 'Your question has been posted successfully')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors')
    else:
        form = QuestionForm()
    return render(request, 'quora_app/post_question.html', {'form': form})

from django.views.generic.edit import FormMixin
from django.views.generic import DetailView, FormView
class QuestionDetailView(DetailView,FormMixin):
    model = Question
    template_name = 'quora_app/view_question.html'
    context_object_name = 'question'
    form_class = AnswerForm

    def get_success_url(self):
        return self.request.path 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        context['answers'] = Answer.objects.filter(question=question).order_by('-created_at')
        context['form'] = self.get_form()
        return context

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = self.get_form()
    #     if form.is_valid():
    #         answer = form.save(commit=False)
    #         answer.user = self.request.user
    #         answer.question = self.object
    #         answer.save()
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View

class AnswerCreateView(View):
    # template_name = 'quora_app/view_question.html'
    # form_class = AnswerForm
    # success_url = reverse_lazy('view_question')

    # def form_valid(self, form):
    #     question = Question.objects.get(pk=self.kwargs['pk'])
    #     answer = form.save(commit=False)
    #     answer.question = question
    #     if self.request.user.is_authenticated:
    #         answer.user = self.request.user
    #         answer.save()
    #         return redirect('view_question', pk=question.pk)
    #     else:
    #         return redirect('login')


    def post(self, request, pk):
        question = Question.objects.get(pk=pk)
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            if request.user.is_authenticated:
                answer.user = request.user
                answer.save()
        return redirect('view_question', pk=pk)

class LikeAnswerView(View):
    def get(self, request, question_id, answer_id):
        try:
            answer = Answer.objects.get(pk=answer_id)
        except Answer.DoesNotExist:
            return redirect('view_question', pk=question_id)
        
        if request.user.is_authenticated:
            if request.user in answer.likes.all():
                answer.likes.remove(request.user)
            else:
                answer.likes.add(request.user)
        return redirect('view_question', pk=question_id)

from django.views.generic import ListView

class UserListView(ListView):
    model = User
    template_name = 'user_list.html'
    context_object_name = 'users'

class DislikeAnswerView(View):
    def get(self, request, question_id, answer_id):
        try:
            answer = Answer.objects.get(pk=answer_id)
        except Answer.DoesNotExist:
            return redirect('view_question', pk=question_id)
        
        if request.user.is_authenticated:
            if request.user in answer.dislikes.all():
                answer.dislikes.remove(request.user)
            else:
                answer.dislikes.add(request.user)
        return redirect('view_question', pk=question_id)