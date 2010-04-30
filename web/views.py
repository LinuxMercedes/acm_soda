from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout
from django.contrib.auth.models import User

from acm_soda.api.models import *

def external(request):
    inventories = Inventory.getEntireInventory()
    return render_to_response('external.html', {'request': request,
                                'inventories': inventories})
        
@login_required
def profile(request, username=''):
    # If no username was present in URL, load current user's profile
    if username == '':
        username = request.user.username
        real_user = request.user
    # Otherwise, load the profile of whichever user was listed
    else:
        real_user = User.objects.get(username=username)
        
    # If the currently logged in user is viewing his own page, show personal data
    if real_user == request.user:
        current_user = True
    else:
        current_user = False
    
    soda_user = MachineUser.objects.get(user=real_user)
    printable_balance = soda_user.balance/100.0
    
    # Grab all admin transactions
    try:
        transactions = SodaTransaction.objects.filter(user=real_user)
    except:
        transactions = None
        
    # Grab all soda transactions
    
    return render_to_response('profile.html', {'user': soda_user, 
        'current_user': current_user, 'printable_balance': printable_balance,
        'transactions': transactions})

def profile_logout(request):
    return logout(request, '/web')