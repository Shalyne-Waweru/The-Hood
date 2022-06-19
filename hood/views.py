from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import NeighbourHood,Profile,Business,Post
from django.contrib.auth.models import User
from .forms import UpdateProfileForm, NeighbourHoodForm,SignupForm,BusinessForm,PostForm

# Create your views here.

def index (request):    
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


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
def join_hood(request):
    # neighbourhood =get_object_or_404(neighbourhood,id=id)
    # request.user.profile.neighbourhood =neighbourhood
    # request.user.profile.save()
    # return redirect('hood')
    return render(request, 'single_hood.html')

# @login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')

@login_required(login_url='login')
def edit_profile(request,username):
    use = User.objects.get(username=username)
    if request.method == 'POST':
        return redirect('profile',request.user.username)
    return render(request, 'editprofile.html')

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
    if request.method == 'GET':
        name = request.GET.get("title")
        results = Business.objects.filter(name__icontains=name).all()
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'results.html', params)
    else:
        message = "You haven't searched for any image category"
    return render(request, "results.html")

@login_required(login_url='login')
def leave_hood(request, id):
    hood = get_object_or_404(NeighbourHood, id=id)
    request.user.profile.neighbourhood = None
    request.user.profile.save()
    return redirect('hood')
        
    

    
    
