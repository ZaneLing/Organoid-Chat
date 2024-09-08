from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import FileModel
import json
from rest_framework.authtoken.models import Token

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return JsonResponse({"error": "Username and password are required"}, status=400)
        
        # 创建新用户
        user = User.objects.create_user(username=username, password=password)
        user.save()

        return JsonResponse({"message": "Registration successful"}, status=201)


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        # 验证用户
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({"message": "Login successful", "username": username, "token":token.key}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)
        
    return JsonResponse({"error": "Method not allowed...."}, status=405)
        
@csrf_exempt
def upload_user_file(request):
    print(request.FILES)
    if request.method == 'POST':
        if 'files' not in request.FILES:
            return JsonResponse({'error': 'No files uploaded'}, status=400)

        files = request.FILES.getlist('files')
        username = request.POST.get('username')

        user = get_object_or_404(User, username=username)
        # Save file to the user's file space
        for file in files:   

            print(file.name)

            user_file = FileModel.objects.create(
                file=file,
                filename=file.name,
                file_size=file.size,
                file_format=file.content_type,
                user=user
            )
            user_file.save()

        return JsonResponse({'message': 'Files uploaded successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
@login_required
def user_info(request):
    user = request.user
    return JsonResponse({'username': user.username})

@csrf_exempt

def get_user_files(requset):
    if requset.method == 'POST':
        try:
            data = json.loads(requset.body)
            username = data.get('user')
            user = User.objects.get(username=username)
            files = FileModel.objects.filter(user=user)
            file_data = [{
                    'id': file.id,
                    'filename': file.filename.rsplit('/', 1)[-1],
                    'file_size': file.file_size,
                    'file_format': file.file_format,
                    'uploaded_at': str(file.uploaded_at),
            } for file in files]
            return JsonResponse({'files': file_data})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid Json'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_file(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            file_id = data.get('id')
            file = FileModel.objects.get(pk=file_id)
            file.delete()
            return JsonResponse({'message': 'File deleted!'})
        except:
            return JsonResponse({'error': 'ID not found'}, status=404)

@csrf_exempt
def open_file(request, fileId):
    file = get_object_or_404(FileModel, id=fileId)
    if not file.file:
        return HttpResponse(status=404)

    response = HttpResponse(file.file, content_type='application/pdf')
    
    response['Content-Disposition'] = f'inline; filename="{file.filename}"'
    
    return response

@csrf_exempt
def delete_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('user')
            user = User.objects.get(username=username)
            user.delete()
            return JsonResponse({'message': 'User deleted!'})
        except:
            return JsonResponse({'error': 'Username not found'}, status=404);


@csrf_exempt

def change_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('user')
        user = User.objects.get(username=username)

        current_password = data.get('currentPassword')
        new_password = data.get('newPassword')
        confirm_password = data.get('confirmPassword')
        
        print(username)

        # 验证当前密码是否正确
        user = authenticate(username=username, password=current_password)
        if user is None:
            return JsonResponse({'error': 'current password wrong'}, status=400)

        # 检查新密码和确认密码是否一致
        if new_password != confirm_password:
            return JsonResponse({'error': 'two passwords not equal'}, status=400)

        # 修改用户密码
        user.set_password(new_password)
        user.save()

        return JsonResponse({'message': 'change successfully'}, status=200)

    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def update_user_info(request):
    try:
        data = json.loads(request.body)
        username = data.get('user')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email_address = data.get('email_address')

        print(username)
        print(first_name)
        print(last_name)
        print(email_address)
        # 获取当前用户
        user = User.objects.get(username=username)
        
        # 更新用户信息
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email_address:
            user.email = email_address

        user.save()

        return JsonResponse({'message': 'User information updated successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)