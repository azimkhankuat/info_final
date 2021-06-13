"""info_final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('otp-encrypt/', views.otp_encrypt, name="otp_encrypt"),
    path('huffman-encode/', views.huffmanEncode, name="huffman_encode"),
    path('huffman-decode/', views.huffmanDecode, name="huffman_decode"),
    path('hamming-encode/', views.hammingEncode, name="hamming_encode"),
    path('add-error/', views.addError, name="add_error"),
    path('hamming-decode/', views.hammingDecode, name="hamming_decode"),
    path('otp-decrypt/', views.otp_decrypt, name="otp_decrypt")
]
