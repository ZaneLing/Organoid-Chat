from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import FileModel, MessageModel, ConversationModel
from datetime import datetime
from rest_framework.authtoken.models import Token
import uuid

# 用户注册
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

# 用户登录
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

# 用户上传文件
@csrf_exempt
def upload_user_file(request):
    print(request.FILES)
    if request.method == 'POST':
        if 'files' not in request.FILES:
            return JsonResponse({'error': 'No files uploaded'}, status=400)

        username = request.POST.get('username')
        conversationTitle = request.POST.get('conversationTitle')
        files = request.FILES.getlist('files')

        conversation = ConversationModel.objects.get(conversation_title=conversationTitle)
        user = get_object_or_404(User, username=username)
        # Save file to the user's file space
        for file in files:   

            print(file.name)

            user_file = FileModel.objects.create(
                file=file,
                conversation = conversation,
                filename=file.name,
                file_size=file.size,
                file_format=file.content_type,
                user=user
            )
            user_file.save()

        return JsonResponse({'message': 'Files uploaded successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

# 获取用户信息
@csrf_exempt
@login_required
def user_info(request):
    user = request.user
    return JsonResponse({'username': user.username})

# 获取用户文件列表
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
                    'file_conversation':file.conversation.id,
                    'file_format': file.file_format,
                    'uploaded_at': str(file.uploaded_at),
            } for file in files]
            return JsonResponse({'files': file_data})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid Json'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# 删除文件
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

# 打开指定pdf文件
@csrf_exempt
def open_file(request, fileId):
    file = get_object_or_404(FileModel, id=fileId)
    if not file.file:
        return HttpResponse(status=404)

    response = HttpResponse(file.file, content_type='application/pdf')
    
    response['Content-Disposition'] = f'inline; filename="{file.filename}"'
    
    return response

# 删除用户
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

# 修改用户密码
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

# 更新用户信息
@csrf_exempt
def update_user_info(request):
    try:
        data = json.loads(request.body)
        username = data.get('user')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email_address = data.get('email_address')

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

# 生成新消息
@csrf_exempt
def create_message(request):
    if request.method == 'POST':
        try:
            # 解析请求数据
            data = json.loads(request.body)
            conversation_title = data.get('conversation_title')
            message_content = data.get('message_content')
            message_role = data.get('message_role')
            print(conversation_title)
            print(1111111)
            print(message_content)
            print(message_role)
            if not conversation_title or not message_content:
                return JsonResponse({'error': 'Conversation title and message content are required'}, status=400)
            
            conversation = ConversationModel.objects.get(conversation_title=conversation_title)

            # 创建 MessageModel 实例
            message = MessageModel.objects.create(
                conversation=conversation,
                message_id=uuid.uuid4(),
                message_role=message_role,
                message_content=message_content
            )
            return JsonResponse({
                'message_id': message.message_id,
                'message_content': message.message_content,
                'message_role': message.message_role,
                }, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# 生成新会话
@csrf_exempt
def create_conversation(request):
    if request.method == 'POST':
        try:
            # 解析请求数据
            data = json.loads(request.body)
            message = data.get('message')
            username = data.get('user')

            if not message or not username:
                return JsonResponse({'error': 'Message and username are required'}, status=400)

            # 获取用户
            user = User.objects.get(username=username)

            # 自动生成 conversation_id 和 conversation_title
            conversation_title = message[:20]
            
            # 创建 ConversationModel 实例
            conversation = ConversationModel.objects.create(
                user=user,
                conversation_id=uuid.uuid4(),
                conversation_title=conversation_title
            )
            
            message = MessageModel.objects.create(
                conversation=conversation,
                message_id=uuid.uuid4(),
                message_role='user',
                message_content=message
            )

            return JsonResponse({
                'message': 'Conversation created successfully',
                'conversation_id': conversation.conversation_id,
                'conversation_title': conversation.conversation_title
            }, status=201)

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

# 获取用户的初始问题和会话文件
@csrf_exempt
def save_conversation_file(request):
    if request.method == 'POST':
        try:
            print(request.POST)  # 打印表单数据以检查内容
            print(request.FILES)
            if 'files' not in request.FILES:
                return JsonResponse({'error': 'No files uploaded'}, status=400)

            files = request.FILES.getlist('files')
            conversation_title = request.POST.get('conversation_title')
            conversation = get_object_or_404(ConversationModel, conversation_title=conversation_title)
            user = conversation.user
             # 打印文件数据
            for file in files:   

                print(file.name)

                user_file = FileModel.objects.create(
                    user = user,
                    file=file,
                    filename=file.name,
                    file_size=file.size,
                    file_format=file.content_type,
                    conversation=conversation
                )
                user_file.save()
            
            return JsonResponse({'message': 'Files uploaded successfully'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

# 获取对话文件   
@csrf_exempt
def get_conversation_file(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            conversation_title = data.get('conversationTitle')
            
            conversation = ConversationModel.objects.get(conversation_title=conversation_title)
            user = User.objects.get(username=username)
            
            files = FileModel.objects.filter(conversation=conversation, user=user)
            print(files)
            file_data = [{
                    'id': file.id,
                    'filename': file.filename.rsplit('/', 1)[-1],
                    'file_size': file.file_size,
                    'file_conversation':file.conversation.id,
                    'file_format': file.file_format,
                    'uploaded_at': str(file.uploaded_at),
            } for file in files]
            return JsonResponse({'files': file_data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
@csrf_exempt
def get_user_conversations(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('user')
            user = User.objects.get(username=username)
            conversations = ConversationModel.objects.filter(user=user)
            conversation_data = [{
                    'id': conversation.conversation_id,
                    'title': conversation.conversation_title,
            } for conversation in conversations]
            return JsonResponse({'conversations': conversation_data})

        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
@csrf_exempt
def delete_conversation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            conversation_title = data.get('conversation_title')
            print(conversation_title)
            conversation = ConversationModel.objects.filter(conversation_title=conversation_title)
            conversation.delete()
            return JsonResponse({'message': 'Conversation deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
@csrf_exempt
def open_conversation(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            conversation_id = data.get('conversation_id')
            conversation = ConversationModel.objects.get(conversation_id=conversation_id)
            messages = MessageModel.objects.filter(conversation=conversation).values('message_content', 'created_at')
            return HttpResponse(messages, content_type='application/json')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def get_conversation_messages(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("get messages:")
            conversation_title = data.get('conversation_title')
            print("title:", conversation_title)
            # username = data.get('username')
            # user = User.objects.get(username=username)
            conversation = ConversationModel.objects.get(conversation_title=conversation_title)
            print("conversation:", conversation)
            messages = MessageModel.objects.filter(conversation=conversation).values('message_content', 'message_role')
            messages_list = list(messages)
            print(1111)
            print(messages_list)

            return JsonResponse(messages_list, safe=False)
        except:
            return JsonResponse({'error': 'Invalid request'}, status=401)
        
