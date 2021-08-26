from django.core.mail import message
from django.http.response import HttpResponse
from kbl.models.certificate import generate_motor_certificate
from kbl.models import policy, vehicles
from django.core.exceptions import ObjectDoesNotExist
from functools import reduce
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response

from .models import (
    User, MotorComprehensivePolicy, Product, Claim, HomeXtra,
    MotorThirdPartyPolicy, PaymentHistory, Policy, MotorClaim,
    Branch, History, PushNotificationToken, PushNotification, VehicleModel
)
from .serializers import (BranchSerializers, ProductSerializers, MotorCliamSerializers,
    UserSerializer, MTPPSerializers, MCPSerializers, PolicySerializers, ClaimSerializers,
    HomeExtraSerializers, HistorySerializers, NotificationSerializers, VehicleSerializer
)

from core.settings import BASE_DIR
from rest_framework import viewsets, status
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import  AllowAny
from .permissions import IsOwnerProfileOrReadOnly, IsLoggedInUserOrAdmin, IsOwnerProfileOrReadOnly, IsAdminUser
from .flutterwave import FlutterWave
from .validators import validatePaymentDetails



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def update(self, request, *args, **kwargs):
        partial = True # Here I change partial to True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


@api_view(['POST'])
@permission_classes((IsLoggedInUserOrAdmin,))
def set_push_token(request):
    try:
        other = PushNotificationToken.objects.filter(token=request.data.get('token')).first()
        if other:
            other.token = None
            other.save()
            
        user = User.objects.get(pk=request.data.get('user'))
        pushToken = PushNotificationToken.objects.filter(user=user.pk).first()
        if pushToken:
            pushToken.token = request.data.get('token')
            pushToken.save()
        else:
            pushToken = PushNotificationToken(user=user,token=request.data.get('token'))
            pushToken.save()

        
        return Response('ok', status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        print(e)
        return Response('Not Ok', status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response('Not Ok', status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ProductViewSet(viewsets.ModelViewSet):
    queryset =Product.objects.all()
    serializer_class = ProductSerializers
   
    def get_permissions(self):
        permission_classes = []
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        elif self.action == 'create' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class BranchViewSet(viewsets.ModelViewSet):
    queryset =Branch.objects.all()
    serializer_class = BranchSerializers
   
    def get_permissions(self):
        permission_classes = []
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [AllowAny]
        elif self.action == 'create' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class NotificationViewSet(viewsets.ModelViewSet):
    queryset =PushNotification.objects.all()
    serializer_class = NotificationSerializers

    def list(self, request):
        user = request.user
        
        nots = PushNotification.objects.filter(user=user.pk).all()
        if nots:
            return Response(NotificationSerializers(nots, many=True).data, status=status.HTTP_200_OK)

        return Response([], status=status.HTTP_200_OK)
   
    def get_permissions(self):
        permission_classes = []
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'create' or self.action == 'destroy' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsOwnerProfileOrReadOnly]
        
        return [permission() for permission in permission_classes]


class MotorThirdPartyViewSet(viewsets.ModelViewSet):
    queryset = MotorThirdPartyPolicy.objects.all()
    serializer_class = MTPPSerializers

    def create(self, request):
        regNo = request.data.get('registration_number')
        try:
            policy = MotorThirdPartyPolicy.objects.get(registration_number=regNo)

            if policy:
                return Response(dict(message="You already have an active policy for this vehicle"), status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
   
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class MotorComprehensiveViewSet(viewsets.ModelViewSet):
    queryset = MotorComprehensivePolicy.objects.all()
    serializer_class = MCPSerializers

    def create(self, request):
        regNo = request.data.get('registration_number')
        try:
            policy = MotorThirdPartyPolicy.objects.get(registration_number=regNo)

            if policy:
                return Response(dict(message="You already have an active policy for this vehicle"), status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
   
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]



class HomeExtraViewSet(viewsets.ModelViewSet):
    queryset = HomeXtra.objects.all()
    serializer_class = HomeExtraSerializers

    '''def create(self, request):
        user = request.data.get('user')
        try:
            policy = HomeXtra.objects.get(user=user)

            if policy:
                return Response(dict(message="You already have an active policy"), status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)'''
   
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]



class MotorClaimsViewSet(viewsets.ModelViewSet):
    queryset = MotorClaim.objects.all()
    serializer_class = MotorCliamSerializers

   
    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


@api_view(['GET'])
@permission_classes((IsLoggedInUserOrAdmin,))
def all_policy_by_user_id(request, pk):
    try:
        queryset = Policy.objects.filter(user=pk).all()
        return Response(PolicySerializers(queryset, many=True).data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        print(e)
        return Response(dict(message="Policy Doesn't Exist"), status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print()
        return Response(dict(message="Something Happened"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes((IsLoggedInUserOrAdmin,))
def all_claim_by_user_id(request, pk):
    try:
        queryset = Claim.objects.filter(user=pk).all()
        return Response(ClaimSerializers(queryset, many=True).data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        print(e)
        return Response(dict(message="Policy Doesn't Exist"), status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response(dict(message="Something Happened"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes((IsLoggedInUserOrAdmin,))
def policy_from_policy_number(request, pn):
    try:
        policy = Policy.objects.get(policy_number=pn)
        serializer = None
        if policy.product.name == "Motor Comprehensive":
            policy = policy.motorcomprehensivepolicy
            serializer = MCPSerializers
        elif policy.product.name == "Motor Third-Party":
            policy = policy.motorthirdpartypolicy
            serializer = MTPPSerializers
        elif policy.product.name == "Home Xtra":
            policy = policy.homextra
            serializer = HomeExtraSerializers

        return Response(serializer(policy).data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        print(e)
        
        return Response(dict(message="Policy Doesn't Exist"), status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response(dict(message="Something Happened"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes((IsLoggedInUserOrAdmin,))
def claim_from_policy_number(request, pn):
    try:
        policy = MotorClaim.objects.get(claim_number=pn)
        serializer = None
        if policy.product.name == "Motor Comprehensive":
            policy = policy.motorcomprehensivepolicy
            serializer = MCPSerializers(policy.motor)
        elif policy.product.name == "Motor Third-Party":
            policy = policy.motorthirdpartypolicy
            serializer = MTPPSerializers

        return Response(serializer(policy).data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        print(e)
        return Response(dict(detail="Policy Doesn't Exist"), status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response(dict(detail="Something Happened"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes((IsLoggedInUserOrAdmin,))
def recent_activities(request, pk):
    if not pk:
        return Response(dict(message="Invalid request format"), status=status.HTTP_400_BAD_REQUEST)
    try:
        history = History.objects.filter(user=pk).all()
        
        return Response(HistorySerializers(history,many=True).data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        print(e)
        return Response(dict(detail="Nothing was found"), status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response(dict(detail="Something Happened"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['GET'])
@permission_classes((AllowAny,))
def all_vehicle_model(request):
    
    try:
        vehicle = VehicleModel.objects.order_by('make','model').all()
        
        return Response(VehicleSerializer(vehicle, many=True).data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        print(e)
        return Response(dict(detail="Nothing was found"), status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response(dict(detail="Something Happened"), status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@permission_classes((AllowAny,))
def pay_with_rave(request):

    error = validatePaymentDetails(request.data)
    
    if error.get('status') != 'ok':
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    try:
        user_id = request.data['user_id']
        user = User.objects.get(pk=user_id)
        rave = FlutterWave(cardno=request.data['cardno'], cvv=request.data['cvv'], 
                            expirymonth=request.data['expirymonth'], expiryyear=request.data['expiryyear'],
                            pin=request.data['pin'], amount=request.data['amount'], user=user)

        res = rave.pay_via_card()

        if res['status'] != 'success':
            return Response({'msg': res['data']['message'], 
                            'code': res['data']['code'], 'status': res['status']}, status=status.HTTP_400_BAD_REQUEST)
                            
        if res['status'] == 'success' and res['data']['chargeResponseCode'] == "00":
            PaymentHistory(request.data['policy_number'],res['data']['flwRef'],'Flutterwave')
            PaymentHistory.save()
            return Response({'msg': res['data']['chargeResponseMessage'], 
                            'code': res['data']['chargeResponseCode'], 
                            'status': res['status'], 'ref': res['data']['flwRef']}, 
                            status=status.HTTP_201_CREATED)

        elif res['status'] == 'success' and res['data']['chargeResponseCode'] == "02":
            return Response({'msg': res['data']['chargeResponseMessage'], 
                            'code': res['data']['chargeResponseCode'], 
                            'status': res['status'],
                            'ref': res['data']['flwRef']},
                            status=status.HTTP_200_OK)

    except Exception as e:
        print(e)
        return Response({"status": "failed", "msg": "something happened server cannot handle this request at the moment try again later"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes((AllowAny,))
def validate_with_OTP_rave(request):

    otp = request.data['otp']
    policy = request.data['policy_number']
    amount = request.data['amount']
    ref = request.data['ref']
    
    if not otp or not ref or not policy or not amount:
        return Response({"status": "failed", "msg": "Bad request some fields are missing from request body"}, 
                        status=status.HTTP_400_BAD_REQUEST)
    try:
       
        rave = FlutterWave()

        res = rave.validatePayment(ref=ref, otp=otp)

        if res['status'] != 'success':
            return Response({'msg': res['message'], 'status': res['status']}, status=status.HTTP_400_BAD_REQUEST)

                       
        if res['status'] == 'success' and res['data']['data']['responsecode'] == "00":

            verify = rave.verifyPayment(res['data']['tx']['txRef'],amount)
            
            if verify == False:
                return Response({"status": "failed", "msg": "Provide amount doesn't match charged amount"}, status=status.HTTP_400_BAD_REQUEST)

            payment = PaymentHistory(policy=policy, ref_num=ref, platform='Flutterwave')
            payment.save()

            return Response({'msg': res['data']['data']['responsemessage'], 
                            'code': res['data']['data']['responsecode'], 'status': res['status']}, 
                            status=status.HTTP_201_CREATED)

    except Exception as e:
        print(e)
        return Response({"status": "failed", "msg": "something happened server cannot handle this request at the moment try again later"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def certificate(request):
    policy = Policy.objects.get(policy_number='MMC-000077KBL')
    product = Product.objects.get(id=policy.product.id)
    pol = None
    if product.category == "Motor":
        pol = policy.motorcomprehensivepolicy if product.name == 'Motor Comprehensive' else policy.motorthirdpartypolicy
    else:
        pol = policy.homextra

    context = {"user": policy.user, 'policy': pol, 'product': product}
    res = generate_motor_certificate(pol,product)
    return render(request, 'motor_certificate.html',context=context)

def testing(request):
    '''policy = Policy.objects.get(policy_number='MMT-000002KBL')
    product = Product.objects.get(id=policy.product.id)
    generate_motor_certificate(policy,product)
    
    return HttpResponse('We had some errors <pre>' + '</pre>')'''
    '''import csv
    with open(f'{BASE_DIR}/kbl/car.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            car = VehicleModel(make=row['MOD_MAK_CODE'], model=row['MOD_DESC'])
            car.save()'''

    return HttpResponse('OK')