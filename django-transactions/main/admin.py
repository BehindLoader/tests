from django.contrib.admin import AdminSite
from django.contrib.auth.models import User

from profiles.models import Profile
from cashes.models import Cash
from transactions.models import Transaction


class TestAdmin(AdminSite):
    site_header = 'TradingView'


my_admin = TestAdmin()

my_admin.register(User)

my_admin.register(Profile)
my_admin.register(Cash)
my_admin.register(Transaction)
