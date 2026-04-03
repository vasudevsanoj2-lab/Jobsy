"""
URL configuration for Jobsy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from myapp import views

urlpatterns = [
    path('',views.login,name='login'),
    path('login_post',views.login_post,name='login_post'),
    path('admin_page',views.admin_page,name='admin_page'),
    path('verify_worker',views.verify_worker,name='verify_worker'),
    path('view_worker_rating',views.view_worker_rating,name='view_worker_rating'),
    path('view_complaint',views.view_complaint,name='view_complaint'),
    path('send_reply/<id>',views.send_reply,name='send_reply'),
    path('send_reply_post',views.send_reply_post,name='send_reply_post'),
    path('worker_registration',views.worker_registration,name='worker_registration'),
    path('view_rating',views.view_rating,name='view_rating'),
    path('manage_skill_worker',views.manage_skill_worker,name='manage_skill_worker'),
    path('view_skill_request',views.view_skill_request,name='view_skill_request'),
    path('view_feedback',views.view_feedback,name='view_feedback'),
    path('update_status/<id>',views.update_status,name='update_status'),
    path('view_payment',views.view_payment,name='view_payment'),
    path('send_complaint/<id>',views.send_complaint,name='send_complaint'),
    path('view_complaint_worker',views.view_complaint_worker,name='view_complaint_worker'),
    path('worker_registration_post',views.worker_registration_post,name='worker_registration_post'),
    path('accept_worker/<id>',views.accept_worker,name='accept_worker'),
    path('reject_worker/<id>',views.reject_worker,name='reject_worker'),
    path('worker_page',views.worker_page,name='worker_page'),
    path('add_new',views.add_new,name='add_new'),
    path('add_post',views.add_post,name='add_post'),
    path('edit_skill_post',views.edit_skill_post,name='edit_skill_post'),
    path('delete_skill/<id>',views.delete_skill,name='delete_skill'),
    path('edit_skill/<id>', views.edit_skill, name='edit_skill'),
    path('accept_skill_request/<id>',views.accept_skill_request,name='accept_skill_request'),
    path('reject_skill_request/<id>',views.reject_skill_request,name='reject_skill_request'),
    path('update_status_post',views.update_status_post,name='update_status_post'),
    path('send_complaint_post',views.send_complaint_post,name='send_complaint_post'),
    path('send_feedback_worker',views.send_feedback_worker,name='send_feedback_worker'),
    path('send_feedback_worker_post',views.send_feedback_worker_post,name='send_feedback_worker_post'),
    path('view_workdetails',views.view_workdetails,name='view_workdetails'),
    path('send_work_request/<id>',views.send_work_request,name='send_work_request'),
    path('view_workrequest_status',views.view_workrequest_status,name='view_workrequest_status'),
    path('reply_worker/<id>',views.reply_worker,name='reply_worker'),
    path('reply_worker_post',views.reply_worker_post,name='reply_worker_post'),
    path('incomingcomplaintworker',views.incomingcomplaintworker,name='incomingcomplaintworker'),
    path('incomingreplyworker/<id>',views.incomingreplyworker,name='incomingreplyworker'),
    path('incomingreplyworker_post',views.incomingreplyworker_post,name='incomingreplyworker_post'),





    path('user_registration',views.user_registration,name='user_registration'),
    path('user_registration_post',views.user_registration_post,name='user_registration_post'),
    path('user_page',views.user_page,name='user_page'),
    path('send_rating/<id>',views.send_rating,name='send_rating'),
    path('send_complaint_user/<id>',views.send_complaint_user,name='send_complaint_user'),
    path('send_complaint_user_post',views.send_complaint_user_post,name='send_complaint_user_post'),
    path('view_reply_user',views.view_reply_user,name='view_reply_user'),
    path('view_skill',views.view_skill,name='view_skill'),
    path('send_rating_post',views.send_rating_post,name='send_rating_post'),
    path('user_send_request_post',views.user_send_request_post,name='user_send_request_post'),    path('user_send_request/<id>',views.user_send_request,name='user_send_request'),
    path('view_request_status_user',views.view_request_status_user,name='view_request_status_user'),
    path('send_feedback',views.send_feedback,name='send_feedback'),
    path('send_feedback_post',views.send_feedback_post,name='send_feedback_post'),
    path('work_details',views.work_details,name='work_details'),
    path('Add_newwork',views.Add_newwork,name='Add_newwork'),
    path('add_newwork_post',views.add_newwork_post,name='add_newwork_post'),
    path('delete/<id>',views.delete,name='delete'),
    path('edit/<id>',views.edit,name='edit'),
    path('edit_post',views.edit_post,name='edit_post'),
    path('view_workrequest',views.view_workrequest,name='view_workrequest'),
    path('Accept/<id>',views.Accept,name='Accept'),
    path('Reject/<id>',views.Reject,name='Reject'),
    path('view_worker_details/<id>',views.view_worker_details,name='view_worker_details'),
    path('admin_block_worker/<id>',views.admin_block_worker,name='admin_block_worker'),
    path('admin_unblock_worker/<id>',views.admin_unblock_worker,name='admin_unblock_worker'),
    path('view_feedback',views.view_feedback,name='view_feedback'),
    path('worker_view_feedback',views.worker_view_feedback,name='worker_view_feedback'),
    path('incoming_complaints',views.incoming_complaints,name='incoming_complaints'),
    path('incomingcomplaintreply/<id>',views. incomingcomplaintreply,name='incomingcomplaintreply'),
    path('incomingcomplaintreply_post',views.incomingcomplaintreply_post,name='incomingcomplaintreply_post'),









    path('logout',views.logout,name='logout'),
path('make_request_payment/<id>/', views.make_request_payment, name='make_request_payment'),
path('request_payment_success/', views.request_payment_success, name='request_payment_success'),



path('worker_chat_withuser', views.worker_chat_withuser),
path('chatview', views.chatview),
path('coun_msg/<int:id>', views.coun_msg, name='coun_msg'),
path('coun_insert_chat/<str:msg>/<int:id>', views.coun_insert_chat, name='coun_insert_chat'),



path('user_chat_withworker', views.user_chat_withworker),
path('u_chatview', views.u_chatview),
path('u_coun_msg/<int:id>', views.u_coun_msg, name='u_coun_msg'),
path('u_coun_insert_chat/<str:msg>/<int:id>', views.u_coun_insert_chat, name='u_coun_insert_chat'),

    path('chatbot/', views.chatbot, name='chatbot'),
    path('chatbot-reply/', views.chatbot_reply, name='chatbot_reply'),

    path('user_chatbot/', views.user_chatbot, name='user_chatbot'),
    path('user_chatbot_reply/', views.user_chatbot_reply, name='user_chatbot_reply'),




]



























































