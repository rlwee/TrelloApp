from django.urls import path,include
from django.contrib.auth import views as auth_views
from accounts.views import (SignUp,
                            LogIn,
                            LogOut,
                            MembersViewList,
                           )

urlpatterns = [

    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', LogIn.as_view(), name='login'),
    path('logout/', LogOut.as_view(), name='logout'),
    path('members/', MembersViewList.as_view(), name='invite'),

    path('', include('django.contrib.auth.urls')),
]