from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from foodoffers.models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import F

from foober.forms import *

# if not request.user.is_authenticated():
#     return HttpResponseRedirect('/register/')

def populate_home_page(request):
    if request.user.is_authenticated():
        return render(request, 'index.html', {'authenticated': True})
    else:
        return render(request, 'index.html', {'authenticated': False})
        
@login_required
def populate_browse(request):
    return render(request, 'browse.html', {'offer_list': FoodOffer.objects.all()})

@login_required
def populate_long_offer(request, offer_id):
    offer_id = int(offer_id)
    try:
        offer = FoodOffer.objects.get(pk=offer_id)
    except:
        raise Http404("Offer " + str(offer_id) + " does not exist.")
        
    return render(request, 'long_offer.html', {'offer': offer})

def get_new_user(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewUser(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid() and request.POST.get('confirm') == request.POST.get('password'):
            u = User(username = request.POST.get('username'),
                    first_name = request.POST.get('first_name'),
                    last_name = request.POST.get('last_name'),
                    email = request.POST.get('email'),
                    password = make_password(request.POST.get('password')),
                    zip_code = request.POST.get('zip_code'),
                    prof_pic = request.FILES['prof_pic'])
            u.save()
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewUser()

    return render(request, 'new_user.html', {'form': form})

@login_required
def see_profile(request):
    offers = FoodOffer.objects.prefetch_related('foodrequest_set').filter(user=request.user)
    requests = FoodRequest.objects.filter(requester=request.user)
    return render(request, 'myaccount.html', {'offer_list': offers, 'request_list': requests})
            
def return_static_file(request, fname):
    try:
        f = open(os.path.join(os.getcwd(), fname))
        return HttpResponse(f.read())
    except:
         raise Http404("File " + os.path.join(os.getcwd(), fname) + " does not exist.")
                    
    
def populate_user_created(request):
    return render(request, 'user_created.html', {})

def get_new_offer(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Offer(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Offer()

    return render(request, 'name.html', {'form': form})

@login_required
def confirm_request(request, offer_id):
    offer_id = int(offer_id)
    try:
        offer = FoodOffer.objects.get(pk=offer_id)
    except:
        raise Http404("Offer " + str(offer_id) + " does not exist.")
    response =  render(request, "confirm_request.html", {"offer": offer})
    response.set_cookie('confirmed' + str(offer_id),"yes", max_age=120)
    return response

@login_required
def request_food(request, offer_id):
    offer_id = int(offer_id)
    try:
        offer = FoodOffer.objects.get(pk=offer_id)
    except:
        raise Http404("Offer " + str(offer_id) + " does not exist.")
    
    food_request = FoodRequest(offer = offer,
                                requester = User.objects.get(pk=request.user.id),
                                party_size = 1,
                                accepted = False)
    if ("confirmed" + str(offer_id)) not in request.COOKIES.keys():
        return HttpResponseRedirect('/confirm/' + str(offer_id))
    if len(FoodRequest.objects.filter(offer=offer, requester=request.user)) == 0:
        food_request.save()
        offer.available_people = F('available_people') - 1
        offer.save()
    
    return render(request, "successful_request.html", {"offer": offer})

@login_required
def accept_request(request, request_id):
    request_id = int(request_id)
    try:
        request_to_accept = FoodRequest.objects.get(pk=request_id)
    except:
        return Http404("Food request " + str(request_id) + " does not exist.")
    
    if request_to_accept.offer.user.id == request.user.id:
        request_to_accept.accepted = True
        request_to_accept.save()
    
    return HttpResponseRedirect('/accounts/profile/')

@login_required
def get_new_offer(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewOffer(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            o = FoodOffer(user = User.objects.get(pk=request.user.id),
                        address = request.POST.get('address'),
                        description = request.POST.get('description'),
                        picture = request.FILES['picture'],
                        price = request.POST.get('price'),
                        max_people = request.POST.get('max_people'),
                        available_people = request.POST.get('max_people'),
                        offer_datetime = request.POST.get('offer_datetime')
                    )
            o.save()
            return HttpResponseRedirect('/thanks/offer/' + str(o.id))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewOffer()

    return render(request, 'offer.html', {'form': form})

@login_required
def thank_offer(request, offer_id):
    offer_id = int(offer_id)
    
    try:
        offer = FoodOffer.objects.get(pk=offer_id)
    except:
        return Http404('FoodOffer ' + str(offer_id) + ' does not exist.')
    
    if offer.user.id == request.user.id:
        return render(request, "thank_offer.html", {"offer": offer})
    else:
        return Http404('User is not the person who offered this meal.')