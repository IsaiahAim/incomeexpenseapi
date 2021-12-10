from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import IncomeSerializer
from .models import Income
from .permissions import IsOwner
from .paginations import ExpensePagination


class IncomeListAPIView(ListCreateAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = ExpensePagination

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)
        return instance

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class IncomeDetailAPIView(RetrieveUpdateAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
