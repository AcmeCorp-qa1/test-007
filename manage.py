print("this is test-09 folder")


print("this is test-09 folder")
print("this is test-09 folder")
print("this is test-09 folder")





# views.py
from rest_framework.views import APIView
from rest_framework.response import Response

class VulnerableView(APIView):
    def get(self, request):
        # Unsafely retrieves user input directly for display in response headers
        user_input = request.GET.get('username', '')
        response = Response("Vulnerable")
        
        # The header is injected without sanitization, allowing script injection
        response['Location'] = f'https://example.com/{user_input}'
        return response

# urls.py
from django.urls import path
from .views import VulnerableView

urlpatterns = [
    path('vulnerable/', VulnerableView.as_view()),
]



# views.py
from rest_framework.views import APIView
from rest_framework.response import Response

class VulnerableView(APIView):
    def get(self, request):
        # Unsafely retrieves user input directly for display in response headers
        user_input = request.GET.get('username', '')
        response = Response("Vulnerable")
        
        # The header is injected without sanitization, allowing script injection
        response['Location'] = f'https://example.com/{user_input}'
        return response

# urls.py
from django.urls import path
from .views import VulnerableView

urlpatterns = [
    path('vulnerable/', VulnerableView.as_view()),
]
