from django.urls import path, re_path
from django.conf.urls import url, include
from rest_framework import routers
from .views import KYCViewSet
from rest_framework.urlpatterns import format_suffix_patterns



'''urlpatterns = format_suffix_patterns([
    path('kyc/', kyc_list, name="kyc-list"),
    path('kyc/<int:pk>/', kyc_detail, name="kyc-detail"),
    path('kyc/<path:email>/', kyc_detail_email, name="kyc-detail-from-email"),
])'''


'''arr = np.array(space)
    neL = np.amax([np.amin(arr[i:i+x]) for i in range(0,arr.size) if arr[i:i+x].size == x ])
    
    for i in range(0,len(space)):
        slc = space[i:i+x]
        if (len(slc) == x):
            neL.append(min(slc))
   
    return neL


    import numpy as np
def carParkingRoof(cars, k):
    # Write your code here
    sorted = np.sort(cars)
    min = 10000000000000000
    for i in range(0,len(cars)):
        slc = sorted[i:i+k]
        if (len(slc) >= k):
            if ((slc[len(slc) - 1] - slc[0])+1 < min ):
                min = (slc[len(slc) - 1] - slc[0])+1
    return min


 sorted = np.sort(scores)
    print(sorted)
    ranks = rd(sorted, method='dense')
    print(ranks)
    result = reduce(lambda sum, j: sum  + (1 if j <= k else 0), ranks, 0)
    return result'''