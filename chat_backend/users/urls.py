
from django.urls import path
from .views import register, get_conversation_file, get_conversation_messages, delete_conversation, get_user_conversations, create_message, create_conversation, save_conversation_file, update_user_info, change_password, delete_file, open_file, delete_user, login_view, upload_user_file, user_info, get_user_files

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('upload/', upload_user_file, name='upload'),
    path('filespace/',get_user_files,name='get_user_files'),
    path('userinfo/', user_info, name='user_info'),
    path('deletefile/',delete_file, name='delete_file'),
    path('openfile/<int:fileId>/', open_file, name='open_file'),
    path('deleteuser/', delete_user, name='delete_user'),
    path('changepassword/', change_password, name='change_password'),
    path('updateuserinfo/', update_user_info, name='update_user_info'),
    path('createconversation/', create_conversation, name='create_conversation'),
    path('saveconversationfile/', save_conversation_file, name='save_conversation_file'),
    path('createmessage/', create_message, name='create_message'),
    path('getuserconversations/', get_user_conversations, name='get_user_conversations'),
    path('deleteconversation/', delete_conversation, name='delete_conversation'),
    path('getconversationmessages/', get_conversation_messages, name='get_conversation_messages'),
    path('getconversationfile/', get_conversation_file, name='get_conversation_file')
    
]