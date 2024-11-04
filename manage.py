print("this is test-09 folder")


print("this is test-09 folder")
print("this is test-09 folder")
print("this is test-09 folder")



# from django.forms import ImageField as i
from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Choose an image')

    def clean_image(self):
        image = self.cleaned_data['image']
        image.save('a') 
        return image


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




from django.utils.encoding import uri_to_iri

# A URI containing non-ASCII characters
uri = "https://example.com/path/%C3%A9cole"

# Convert the URI to an IRI
iri = uri_to_iri(uri)

print(iri)  # Output: https://example.com/path/école
