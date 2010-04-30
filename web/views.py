from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout
from django.contrib.auth.models import User

from acm_soda.api.models import Inventory, MachineUser

def external(request):
    inventories = Inventory.getEntireInventory()
    return render_to_response('external.html', {'inventories': inventories})
        
@login_required
def profile(request, username):
    real_user = User.objects.get(username=username)
    soda_user = MachineUser.objects.get(user=real_user)
    return render_to_response('profile.html', {'user': soda_user, 'request': real_user})

def profile_logout(request):
    return logout(request, '/web')