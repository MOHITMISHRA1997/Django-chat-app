from django.shortcuts import render,redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Chat,Group,Onlineuser
from .forms import Create_users,Update_profile,Update_user
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = Create_users(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your data has been saved')
            return redirect('login')            
    form = Create_users()
    return render(request,'signup.html',{'form' : form})



@login_required
def index(request):
    all_users = User.objects.all()
    if request.method == 'POST':
        name = request.POST['names']
        all_users = User.objects.filter(Q(username__startswith=name))         
    return render(request,'frotpage.html',{'all_users':all_users})


@login_required
def chat(request,user_id):    
    all_users = User.objects.all()
    selected_user = get_object_or_404(User,id=user_id)
    recievers_id = selected_user.id 
    sender_id = request.user.id
    to_be_group = f'chat_{min(sender_id,recievers_id)}_{max(sender_id,recievers_id)}'
    group = Group.objects.filter(name = str(to_be_group)).first()
    chats = []
    if group:
        chats = Chat.objects.filter(group = group).order_by('timestamp')
    else:
        group = Group(name = to_be_group)
        group.save()
    
    return render(request,'chat.html',{'selected_user': selected_user,'all_users':all_users,'chats':chats})

# View Profile
def profile(request,username):
    user = User.objects.get(username=username)
    all_users = User.objects.all()
    return render(request,'profile.html',{'all_users':all_users,'user':user})


# Update Profile
@login_required
def profile_update(request):
    all_users = User.objects.all()   
    if request.method == 'POST':
        form1 = Update_user(request.POST,instance=request.user)
        form2 = Update_profile(request.POST,request.FILES,instance=request.user.userprofile)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            messages.success(request,'Your data has been updated...')
    form1 = Update_user()
    form2 = Update_profile()
    return render(request,'update_profile.html',{'all_users':all_users,'form1':form1,'form2':form2})


class ChangePasswordView(SuccessMessageMixin,PasswordChangeView):
    template_name = 'change_password.html'
    success_message = 'Your Password has been changed'
    success_url = reverse_lazy('index')


