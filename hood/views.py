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
        return redirect('index')
    return render(request, 'registration/signup.html')

def hoodsView (request):
    all_hoods =  Neighborhood.objects.all()
    all_hoods = all_hoods[::-1]
    context = {
        'all_hoods': all_hoods
    }
    
    return render(request, 'all_hoods.html',context)

def newHood (request):
    if request.method == 'POST':
        return redirect('hood')
    return render(request, 'newhood.html')

def hoodMembership (request,hood_id):   
    hood = Neighborhood.objects.get(id=hood_id)
    members =Profile.objects.filter(neighbourhood=hood).all()
    return render(request, 'members.html',{'members':members})

def join_hood(request,id):
    neighbourhood =get_object_or_404(neighbourhood,id=id)
    request.user.profile.neighbourhood =neighbourhood
    requst.user.profile.save()
    return redirect('hood')

def profile(request,username):
    return render(request, 'profile.html')

def edit_profile(request,username):
    use = User.objects.get(username=username)
    if request.method == 'POST':
        return redirect('profile',user.username)
    return render(request, 'editprofile.html')

def add_amenity(request,hood_id):
    hood = NeighbourHood.objects.get(id=hood_id)
    business = Business.objects.filter(neighbourhood=hood)
    posts = Post.objects.filter(hood=hood)
    posts = posts[::-1]
    if request.method == 'POST':
        return redirect('add_amenity', hood.id)
    return render(request, 'add_amenity.html')

def create_post(request,hood_id):
    hood = NeighbourHood.objects.get(id=hood_id)
    if request.method == 'POST':
        return redirect('add_amenity', hood.id)
    return render(request, 'post.html')
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

def leave_hood(request, id):
    hood = get_object_or_404(NeighbourHood, id=id)
    request.user.profile.neighbourhood = None
    request.user.profile.save()
    return redirect('hood')