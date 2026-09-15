import uuid

from django.db.models import Count
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product

from .models import Favorite
from .serializers import FavoriteSerializer


class FavoriteListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        guest_id = request.headers.get("X-Guest-ID")

        if request.user.is_authenticated:
            favorites = Favorite.objects.filter(
                user=request.user
            ).select_related("product")
        elif guest_id:
            try:
                guest_id = uuid.UUID(guest_id)
            except ValueError:
                return Response([])
            
            favorites = Favorite.objects.filter(
                guest_id=guest_id
            ).select_related("product")
        else:
            return Response([])

        serializer = FavoriteSerializer(
            favorites,
            many=True
        )

        return Response(serializer.data)


class FavoriteAddView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        product_id = request.data.get("product")

        if not product_id:
            return Response(
                {
                    "detail": "Le produit est obligatoire."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            product = Product.objects.get(
                id=product_id,
                is_active=True
            )
        except Product.DoesNotExist:
            return Response(
                {
                    "detail": "Produit introuvable."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if request.user.is_authenticated:
            favorite, created = Favorite.objects.get_or_create(
                user=request.user,
                product=product
            )
        else:
            guest_id = request.headers.get("X-Guest-ID")

            if not guest_id:
                return Response(
                    {
                        "detail": "Identifiant visiteur manquant."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                guest_id = uuid.UUID(guest_id)
            except ValueError:
                return Response(
                    {
                        "detail": "Identifiant visiteur invalide."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            favorite, created = Favorite.objects.get_or_create(
                guest_id=guest_id,
                product=product
            )

        total_favorites = Favorite.objects.filter(
            product=product
        ).count()

        serializer = FavoriteSerializer(favorite)

        return Response(
            {
                "detail": (
                    "Produit ajouté aux favoris."
                    if created
                    else "Ce produit est déjà dans vos favoris."
                ),
                "favorite": serializer.data,
                "favorites_count": total_favorites,
                "is_favorite": True
            },
            status=(
                status.HTTP_201_CREATED
                if created
                else status.HTTP_200_OK
            )
        )


class FavoriteRemoveView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, product_id):
        if request.user.is_authenticated:
            favorite = Favorite.objects.filter(
                user=request.user,
                product_id=product_id
            ).first()
        else:
            guest_id = request.headers.get("X-Guest-ID")

            if not guest_id:
                return Response(
                    {
                        "detail": "Identifiant visiteur manquant."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                guest_id = uuid.UUID(guest_id)
            except ValueError:
                return Response(
                    {
                        "detail": "Identifiant visiteur invalide."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            favorite = Favorite.objects.filter(
                guest_id=guest_id,
                product_id=product_id
            ).first()

        if not favorite:
            return Response(
                {
                    "detail": "Ce produit n'est pas dans vos favoris."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        product = favorite.product

        favorite.delete()

        total_favorites = Favorite.objects.filter(
            product=product
        ).count()

        return Response(
            {
                "detail": "Produit retiré des favoris.",
                "favorites_count": total_favorites,
                "is_favorite": False
            },
            status=status.HTTP_200_OK
        )


class FavoriteCountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, product_id):
        try:
            product = Product.objects.get(
                id=product_id,
                is_active=True
            )
        except Product.DoesNotExist:
            return Response(
                {
                    "detail": "Produit introuvable."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        favorites_count = Favorite.objects.filter(
            product=product
        ).count()

        return Response(
            {
                "product": product.id,
                "favorites_count": favorites_count
            }
        )


class FavoriteCountsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        counts = Favorite.objects.values(
            "product_id"
        ).annotate(
            favorites_count=Count("id")
        )

        result = {
            str(item["product_id"]): item["favorites_count"]
            for item in counts
        }

        return Response(result)