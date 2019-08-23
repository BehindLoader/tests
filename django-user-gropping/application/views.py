from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import user_passes_test


def user_in_group_one(user):
    return user.groups.filter(name='group1').exists()

def user_in_group_two(user):
    return user.groups.filter(name='group2').exists()

# # # # # # # # # # # # # # # # # # # # # # # # #

@user_passes_test(user_in_group_one)
def view1(request):
    return HttpResponse('This is view 1')

@user_passes_test(user_in_group_two)
def view2(request):
    return HttpResponse('This is view 2')
