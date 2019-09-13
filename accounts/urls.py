from django.urls import path,include
from accounts.views import (SignUp,
                            LogIn,
                            LogOut,
                           )

urlpatterns = [

    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', LogIn.as_view(), name='login'),
    path('logout/', LogOut.as_view(), name='logout'),

]