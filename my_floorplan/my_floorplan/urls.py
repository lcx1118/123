"""
URL configuration for my_floorplan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
from django.urls import path
from myapp.views import RegisterView, LoginView,ImageUploadView, BoundaryUploadView, HousingAndCoreSubmitView,ImageView,ImageUploadView2
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
def home(request):
    return HttpResponse("Welcome to My Floorplan API!")
urlpatterns = [
    path('', home, name='home'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/upload/', ImageUploadView.as_view(), name='image-upload'),
    path('api/upload2/', ImageUploadView2.as_view(), name='image-upload2'),
    path('api/upload-boundary/', BoundaryUploadView.as_view(), name='upload-boundary'),
    path('api/submit-housing-core/', HousingAndCoreSubmitView.as_view(), name='submit-housing-core'),
    path('api/images/', ImageView.as_view(), name='images'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


