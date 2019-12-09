"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url

from cashes.views import send_money
from main.admin import my_admin
from profiles.views import login
from transactions.views import TransactionsList, TransactionUserList

urlpatterns = [
    url(r'^admin/', my_admin.urls),
    url(r"^account/login/", login),
    url(r"^cash/send/", send_money),
    url(r"^transactions/$", TransactionsList.as_view()),
    url(r"^transactions/users/$", TransactionUserList.as_view()),
]
