
from django.utils import timezone
from django.contrib.auth import logout
from django.shortcuts import redirect

class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            
            if (timezone.now() - request.user.last_login).total_seconds() > 3600:
                logout(request)
            
        return response


class GroupRestrictedMiddleware:
     def __init__(self, get_response):
        self.get_response = get_response

     def __call__(self,request):
        response = self.get_response(request)
        dict={
            '/adm/':'Administradores',
            '/func/':'Funcionários',
            '/gerencia/':'Gerencia'
            
        }
        cont = 0
        for ind, value in enumerate(request.path):
            if value == '/' and cont<2:
                cont+=1
                path_dict = request.path[0:ind+1]
        try:
            dict[path_dict]
        except:
            return response
        else:
            if request.user.is_authenticated:
                for group in request.user.groups.all():
                    if dict[path_dict] == group.name:
                        return response
                return redirect('redirect')
            else:
                return response