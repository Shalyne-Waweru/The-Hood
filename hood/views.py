from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import NeighbourHood,Profile,Business,Post
from django.contrib.auth.models import User
from .forms import *
from django.http import HttpResponseRedirect

# Create your views here.

def index (request):    
    hoods = NeighbourHood.objects.all()
    
    if request.method == "POST":
        
        name = request.POST.get('hoodName')
        location = request.POST.get('location')
        description = request.POST.get('description')
        emergency = request.POST.get('emergency')
        police_number = request.POST.get('police_number')
        image = request.FILES['image']
        
        new_hood = NeighbourHood(name=name, location=location, description=description, image=image, emergency=emergency,police_number=police_number)
        new_hood.save()
        
        print(name)
        print(image)
        
        return redirect("index")
    
    return render(request, 'index.html', locals())

def login_user(request):
  '''
  View function that renders the login page and its data
  '''
  if request.method == "POST":
    username = request.POST['username']
    password = request.POST['password']
    
    print(username)
    print(password)
    
    user = authenticate(request, username=username, password=password)
    print(user)
    
    if user is not None:
      login(request, user)
    #   messages.success(request, username + " Logged In Successfully!")
      return redirect("index")
  
    else:
    #   messages.error(request, "Username or Password is Incorrect. Please Try Again!")
      return redirect("login")
  return render(request,"auth/login.html", locals())

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        
        if form.is_valid():
            form.save()
        
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            print(username)
            
            # user = authenticate(username=username, password=password1)
            # login(request, user)
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'auth/signup.html', locals())


@login_required(login_url='login')
def hoodsView (request):
    all_hoods =  NeighbourHood.objects.all()
    all_hoods = all_hoods[::-1]
    context = {
        'all_hoods': all_hoods
    }
    
    return render(request, 'all_hoods.html',context)

@login_required(login_url='login')
def newHood (request):
    if request.method == 'POST':
        form = NeighbourHoodForm(request.POST, request.FILES)
        if form.is_valid():
            hood = form.save(commit=False)
            hood.admin = request.user.profile
            hood.save()
            return redirect('hood')
    else:
        form = NeighbourHoodForm()
    return render(request, 'newhood.html', {'form': form})

   

@login_required(login_url='login')
def hoodMembership (request,hood_id):   
    hood = NeighbourHood.objects.get(id=hood_id)
    members =Profile.objects.filter(neighbourhood=hood).all()
    return render(request, 'members.html',{'members':members})


# @login_required(login_url='login')
def join_hood(request,id):
    neighbourhood =get_object_or_404(NeighbourHood,id=id)
    request.user.profile.neighbourhood =neighbourhood
    request.user.profile.save()
    
    members =Profile.objects.filter(neighbourhood=neighbourhood).all()
    
    businesses = Business.objects.filter(neighbourhood=neighbourhood).all()
    
    user = NeighbourHood.objects.filter(occupants=request.user.id)
    print(user)
    
    if request.method == "POST":
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        description = request.POST.get('description')
        image = request.FILES['image']
        
        new_business = Business(name=name, email=email, description=description, neighbourhood=neighbourhood, user=request.user, image=image)
        new_business.save()
        
        print(name)
        print(image)
    
    
    return render(request, 'single_hood.html', locals())

# @login_required(login_url='login')
def profile(request,id):
  '''
  View function that renders the profile page and its data
  '''

  user_info_form = UpdateUserInfoForm()
  update_profile_form = UpdateProfileForm()
  
  if request.method == 'POST':
    user_info_form = UpdateUserInfoForm(request.POST,instance=request.user)
    update_profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
    
    if user_info_form.is_valid and update_profile_form.is_valid():
            user_info_form.save()
            update_profile_form.save()
            return HttpResponseRedirect(request.path_info)
  else:
        user_info_form = UpdateUserInfoForm(instance=request.user)
        update_profile_form = UpdateProfileForm(instance=request.user.profile)
  return render(request, 'profile.html', locals())

@login_required(login_url='login')
def edit_profile(request,username):
    use = User.objects.get(username=username)
    if request.method == 'POST':
        return redirect('profile',request.user.username)
    return render(request, 'profile.html')

@login_required(login_url='login')
def add_amenity(request,hood_id):
    hood = NeighbourHood.objects.get(id=hood_id)
    business = Business.objects.filter(neighbourhood=hood)
    posts = Post.objects.filter(hood=hood)
    posts = posts[::-1]
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            b_form = form.save(commit=False)
            b_form.neighbourhood = hood
            b_form.user = request.user.profile
            b_form.save()
            return redirect('add_amenity', hood.id)
    else:
        form = BusinessForm()
    params = {
        'hood': hood,
        'business': business,
        'form': form,
        'posts': posts
    }
    return render(request, 'add_amenity.html', params)


@login_required(login_url='login')
def create_post(request,hood_id):
    hood = NeighbourHood.objects.get(id=hood_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.hood = hood
            post.user = request.user.profile
            post.save()
            return redirect('add_amenity', hood.id)
    else:
        form = PostForm()
    return render(request, 'post.html', {'form': form})


@login_required(login_url='login')
def search_business(request):
    if 'name' in request.GET and request.GET["name"]:
        search_term = request.GET.get("name")
        searched_businesses = Business.search_business(search_term)
        message = f"{search_term}"
        return render(request, 'search.html',{"message":message,"searched_businesses": searched_businesses})
    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})


@login_required(login_url='login')
def leave_hood(request, id):
    hood = get_object_or_404(NeighbourHood, id=id)
    request.user.profile.neighbourhood = None
    request.user.profile.save()
    return redirect('hood')
        
    

    
    
