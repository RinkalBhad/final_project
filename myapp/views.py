from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import*
from django.contrib.auth.decorators import login_required
from itertools import chain
import random

# Create your views here.
@login_required
def index(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)
    
    user_following_list=[]
    feed=[]
    user_following=FollowersCount.objects.filter(follower=request.user.username)

    for users in user_following:
        user_following_list.append(users.user)

    for usernames in user_following_list:
        feed_lists=Post.objects.filter(user=usernames)
        feed.append(feed_lists)

    feed_list=list(chain(*feed))

   # posts=Post.objects.all()
    #user suggestion

    all_users=User.objects.all()
    user_following_all=[]

    for user in user_following:
        user_list=User.objects.get(username=user.user)
        user_following_all.append(user_list)

    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if ( x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
        username_profile.append(users.id)

    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)

    suggestions_username_profile_list = list(chain(*username_profile_list))



    return render(request,'index.html',{'user_profile': user_profile, 'posts':feed_list, 'suggestions_username_profile_list': suggestions_username_profile_list[:4]})

def likepost(request):
    username=request.user.username
    post_id=request.GET.get('post_id')

    post=Post.objects.get(id=post_id)

    like_filter=LikePost.objects.filter(post_id=post_id,username=username).first()

    if like_filter==None:
        new_like=LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()

        post.no_of_likes=post.no_of_likes+1
        post.save()
        return redirect("/")
  
    else:
        like_filter.delete()
        post.no_of_likes=post.no_of_likes-1
        post.save()
        return redirect("/")

    

def upload(request):
    if request.method=="POST":
        user=request.user.username
        image=request.FILES.get('image_upload')
        caption=request.POST['caption']

        new_post=Post.objects.create(user=user,image=image,caption=caption)

        new_post.save()
        return redirect("/")
    else:
        return redirect("/")
    

def profile(request,pk):
    user_object=User.objects.get(username=pk)
    user_profile=Profile.objects.get(user=user_object)
    user_post=Post.objects.filter(user=pk)
    user_post_length=len(user_post)

    follower=request.user.username
    user=pk
    if FollowersCount.objects.filter(follower=follower,user=user).first():
        button_text='unfollow'

    else:
        button_text='Follow'

    user_followers=len(FollowersCount.objects.filter(user=pk))
    user_followeing=len(FollowersCount.objects.filter(follower=pk))
    return render(request,'profile.html',{'user_profile':user_profile,"user_object":user_object,'user_post':user_post,"user_post_length":user_post_length,
                                          'button_text':button_text,'user_followers':user_followers,'user_followeing':user_followeing})

@login_required
def setting(request):
    user_profile=Profile.objects.get(user=request.user)
    
    if request.method=="POST":
        if request.FILES.get('image')==None:
            image=user_profile.profileimg
            bio=request.POST['bio']
            location=request.POST['location']

            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()

        if request.FILES.get('image')!=None:
            image=request.FILES.get('image')
            bio=request.POST['bio']
            location=request.POST['location']

            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()

        return redirect('setting')

    return render(request,'setting.html',{'user_profile':user_profile})

def signin(request):
    if request.method=="POST":
        username=request.POST['username']
        pwd=request.POST['password']

        user=auth.authenticate(username=username,password=pwd)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        
        else:
            messages.info(request,'invalid username or password')
            return redirect("signin")
    return render(request,'signin.html')

def signup(request):

    if request.method=="POST":
        unm=request.POST['username']
        email=request.POST['email']
        pwd=request.POST['password']
        pwd2=request.POST['password2']

        if pwd==pwd2:
                """ if User.objects.filter(email=email).exists:
                messages.info(request,'email already exists')
                 return redirect('signup')
                if User.objects.filter(username=unm).exists:
                messages.info(request,'username already exists')"""
           
                user=User.objects.create_user(username=unm,email=email,password=pwd)
                user.save()
               
               # log user in and redirect setting page
                user_login=auth.authenticate(username=unm,password=pwd)
                auth.login(request,user_login)

                # creaate a profile object for the new user

                user_model=User.objects.get(username=unm)
                new_profile=Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('setting')
        else:
            messages.info(request,'password does not match')
            return redirect('signup')
       
    else:
        pass
    return render(request,'signup.html')


def userlogout(request):
    auth.logout(request)
    return redirect("signin")


def follow(request):
   
   if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
   else:
        return redirect('/')
   



def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})


def delete(request,id):
    uid=User.objects.get(id=id)
    User.delete(uid)
    return redirect("/")