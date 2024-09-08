
from django.urls import path
from .views import register, update_user_info, change_password, delete_file, open_file, delete_user, login_view, upload_user_file, user_info, get_user_files

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('upload/', upload_user_file, name='upload'),
    path('filespace/',get_user_files,name='get-user_files'),
    path('userinfo/', user_info, name='user_info'),
    path('deletefile/',delete_file, name='delete_file'),
    path('openfile/<int:fileId>/', open_file, name='open_file'),
    path('deleteuser/', delete_user, name='delete_user'),
    path('changepassword/', change_password, name='change_password'),
    path('updateuserinfo/', update_user_info, name='update_user_info'),
]