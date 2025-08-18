from .models import Employee

def employee_data(request):
    if request.user.is_authenticated and hasattr(request.user, 'employee'):
        return {'employee': request.user.employee}
    return {}