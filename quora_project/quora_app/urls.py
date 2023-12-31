from django.urls import path
from . import views

urlpatterns = [
    path('post-question/',views.post_question, name='post_question'),
    path('question/<int:pk>/',views.QuestionDetailView.as_view(), name='view_question'),
    path('question/<int:pk>/answer/', views.AnswerCreateView.as_view(), name='post_answer'),
    path('question/<int:question_id>/like/<int:answer_id>/',views.LikeAnswerView.as_view(), name='like_answer'),
    path('question/<int:question_id>/dislike/<int:answer_id>/', views.DislikeAnswerView.as_view(), name='dislike_answer'),
    path('',views.home, name='home'),
    path('accounts/profile/', views.profile, name='user_profile'),
    path('user/login/', views.LoginPage, name='login_page'),
    path('user/logout/', views.Logout, name='logout_page'),
    path('user/signup/', views.SignupPage, name='signup'),
    path('user_list/', views.UserListView.as_view(), name='user_list'),
    
    # path('user/forgot_password/', views.ForgotPassword, name='forgot_password_page'),
    # path('user/forgot_password/<action>', views.ForgotPassword, name='forgot_password_action'),
]