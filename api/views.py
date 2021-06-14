from .models import Exchange, UserAccess
from .serializers import ExchangeSerializer
from .utils import  ExtractBanxico, ExtractDiario, ExtractFixer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, IsAuthenticated
from datetime import datetime, date, timedelta

class LimitReachedOnly(BasePermission):
    def has_permission(self, request, view):
        td = date.today()
        tm = td + timedelta(days=1)
        access = UserAccess.objects.filter(user=request.user.id, created__range=[td, tm]).count()
        return not access >= 30

class ExchangeListView(APIView):
    permission_classes = [IsAuthenticated, LimitReachedOnly]

    def get(self, request, format=None):
        ex_B = ExtractBanxico()
        ex_B.main()
        ex_F = ExtractFixer()
        ex_F.main()
        ex_D = ExtractDiario()
        ex_D.main()
        UserAccess.objects.create(user=request.user)
        td = date.today()
        tm = td + timedelta(days=1)
        exchange = Exchange.objects.filter(created__range=[td, tm])
        serializer = ExchangeSerializer(exchange, many=True)
        return Response(serializer.data)
