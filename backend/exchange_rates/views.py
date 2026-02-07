from datetime import date

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ExchangeRate
from .serializers import ExchangeRateSerializer
from .services import ExchangeRateService


class ExchangeRateListView(generics.ListAPIView):
    """List exchange rates for a specific date."""
    serializer_class = ExchangeRateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        rate_date = self.request.query_params.get('date')
        if rate_date:
            return ExchangeRate.objects.filter(rate_date=rate_date)
        return ExchangeRate.objects.filter(rate_date=date.today())


class ExchangeRateSyncView(APIView):
    """Trigger exchange rate sync."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        rate_date = request.data.get('date')
        if rate_date:
            from datetime import datetime
            rate_date = datetime.strptime(rate_date, '%Y-%m-%d').date()
        else:
            rate_date = date.today()

        try:
            rates = ExchangeRateService.fetch_rates_for_date(rate_date)
            return Response({
                'message': f'Fetched {len(rates)} exchange rates',
                'date': rate_date.isoformat(),
                'rates_count': len(rates)
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
