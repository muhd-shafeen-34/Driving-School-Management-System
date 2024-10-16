from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


@never_cache
@login_required(login_url='login')
def admin_dashboard(req):
    if req.user.role == 'admin':
        return render(req, 'App/Admin/admin_dashboard.html')
#     elif req.user.role=='instructor':
#         return rednder(req, 'App/Staff/staff_dashboard.html')
    else:
        return HttpResponseForbidden("you do not have permission to this page")