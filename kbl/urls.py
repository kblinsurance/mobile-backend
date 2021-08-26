from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers

#from .views import UserProfileListCreateView, userProfileDetailView
from .views import (UserViewSet, 
    MotorThirdPartyViewSet, 
    MotorComprehensiveViewSet, 
    pay_with_rave, validate_with_OTP_rave, HomeExtraViewSet,
    all_policy_by_user_id, policy_from_policy_number,
    ProductViewSet, MotorClaimsViewSet, all_claim_by_user_id, all_vehicle_model,
    BranchViewSet, recent_activities, set_push_token, NotificationViewSet
)
from kyc.views import KYCViewSet

#router = routers.DefaultRouter()
#router.register(r'users', UserProfileListCreateView)
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'claims/motor', MotorClaimsViewSet)
router.register(r'kyc', KYCViewSet)
router.register(r'products', ProductViewSet)
router.register(r'branchs', BranchViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'policies/home-xtra', HomeExtraViewSet)
router.register(r'policies/motor-third-party', MotorThirdPartyViewSet)
router.register(r'policies/motor-comprehensive', MotorComprehensiveViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('dj_rest_auth.urls')),
    url(r'^', include('django.contrib.auth.urls')),
    path('push-token/save/', set_push_token, name='set_push_token'),
    path('claims/<int:pk>/', all_claim_by_user_id, name='claims by user id'),
    path('activities/<int:pk>/', recent_activities, name='Recent activities for user'),
    path('policies/<int:pk>/', all_policy_by_user_id, name='policies by user id'),
    path('policy/<path:pn>/', policy_from_policy_number, name='policies by policy number'),
    path('vehicles/models/', all_vehicle_model, name='Get all vehicles'),
    url(r'pay/rave/validate/', validate_with_OTP_rave),
    url(r'pay/rave/', pay_with_rave),
    
    #re_path(r'^.*$',views.allroutes, name="*")
]
