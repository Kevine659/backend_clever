from decimal import Decimal
from django.db import transaction
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from products.models import ProductRange, Product
from .models import Order,OrderItem,Commercial,CommercialRotation
from .permissions import IsAdminUser
from .serializers import OrderSerializer


# ROTATION DES COMMERCIAUX

def get_next_commercial():
    commercials=list(
        Commercial.objects.filter(
            is_active=True
        ).order_by("id")
    )
    if not commercials:
        return None
    rotation=(
        CommercialRotation.objects
        .select_for_update()
        .first()
    )
    if rotation is None:
        rotation=CommercialRotation.objects.create(
            current_index=0
        )
    current_index=rotation.current_index%len(commercials)
    commercial=commercials[current_index]
    rotation.current_index=(current_index+1)%len(commercials)
    rotation.save(
        update_fields=[
            "current_index",
            "updated_at"
        ]
    )
    return commercial


# PRIX D'UNE GAMME


def get_range_price(product_range):
    if product_range is None:
        return Decimal("0.00")
    for field_name in [
        "current_price",
        "promotional_price",
        "price"
    ]:
        if hasattr(product_range,field_name):
            value=getattr(product_range,field_name)
            if value is not None:
                try:
                    return Decimal(str(value))
                except (TypeError,ValueError):
                    pass
    return Decimal("0.00")


# COMMANDES CLIENT


class OrderListCreateView(APIView):

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        orders = (
            Order.objects
            .filter(user=request.user)
            .select_related("commercial")
            .prefetch_related(
                "items__product",
                "items__product_range"
            )
        )

        serializer = OrderSerializer(
            orders,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @transaction.atomic
    def post(self, request):

        # ==========================================================
        # 1. INFORMATIONS CLIENT
        # ==========================================================

        first_name = str(
            request.data.get("first_name", "")
        ).strip()

        last_name = str(
            request.data.get("last_name", "")
        ).strip()

        phone = str(
            request.data.get("phone", "")
        ).strip()

        email = str(
            request.data.get("email", "")
        ).strip()

        city = str(
            request.data.get("city", "")
        ).strip()

        address = str(
            request.data.get("address", "")
        ).strip()

        if not all([
            first_name,
            last_name,
            phone,
            email,
            city,
            address
        ]):
            return Response(
                {
                    "detail": "Tous les champs de livraison sont obligatoires."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # ==========================================================
        # 2. DETERMINER SI LE CLIENT EST CONNECTE
        # ==========================================================

        is_authenticated = (
            request.user
            and request.user.is_authenticated
        )

        user = request.user if is_authenticated else None

        # ==========================================================
        # 3. RECUPERER LES ARTICLES
        # ==========================================================

        cart_items = []

        # ----------------------------------------------------------
        # CLIENT CONNECTE
        # ----------------------------------------------------------

        if is_authenticated:

            try:
                cart = (
                    Cart.objects
                    .select_for_update()
                    .get(user=request.user)
                )

            except Cart.DoesNotExist:

                return Response(
                    {
                        "detail": "Votre panier est vide."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart_items = list(
                cart.items
                .select_related(
                    "product",
                    "product_range"
                )
                .all()
            )

            if not cart_items:
                return Response(
                    {
                        "detail": "Votre panier est vide."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        # ----------------------------------------------------------
        # CLIENT NON CONNECTE
        # ----------------------------------------------------------

        else:

            items = request.data.get("items", [])

            if not isinstance(items, list) or not items:

                return Response(
                    {
                        "detail": "Votre panier est vide."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ======================================================
            # CONSTRUIRE UNE LISTE D'ARTICLES DEPUIS LE PAYLOAD
            # ======================================================

            for item in items:

                if not isinstance(item, dict):
                    return Response(
                        {
                            "detail": "Un article du panier est invalide."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                item_type = item.get("type")

                quantity = item.get("quantity", 0)

                try:
                    quantity = int(quantity)
                except (TypeError, ValueError):
                    quantity = 0

                if quantity <= 0:
                    return Response(
                        {
                            "detail": "La quantité d'un article est invalide."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # --------------------------------------------------
                # PRODUIT
                # --------------------------------------------------

                if item_type == "product":

                    product_id = item.get("product")

                    if not product_id:
                        return Response(
                            {
                                "detail": "Identifiant produit manquant."
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    try:
                        product = Product.objects.get(
                            id=product_id
                        )
                    except Product.DoesNotExist:

                        return Response(
                            {
                                "detail": "Produit introuvable."
                            },
                            status=status.HTTP_404_NOT_FOUND
                        )

                    cart_items.append({
                        "type": "product",
                        "product": product,
                        "product_range": None,
                        "quantity": quantity
                    })

                # --------------------------------------------------
                # GAMME
                # --------------------------------------------------

                elif item_type == "range":

                    product_range_id = item.get(
                        "product_range"
                    )

                    if not product_range_id:
                        return Response(
                            {
                                "detail": "Identifiant de gamme manquant."
                            },
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    try:
                        product_range = ProductRange.objects.get(
                            id=product_range_id
                        )
                    except ProductRange.DoesNotExist:

                        return Response(
                            {
                                "detail": "Gamme introuvable."
                            },
                            status=status.HTTP_404_NOT_FOUND
                        )

                    cart_items.append({
                        "type": "range",
                        "product": None,
                        "product_range": product_range,
                        "quantity": quantity
                    })

                else:

                    return Response(
                        {
                            "detail": "Type d'article invalide."
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

        # ==========================================================
        # 4. VERIFIER LES COMMERCIAUX
        # ==========================================================

        if not Commercial.objects.filter(
            is_active=True
        ).exists():

            return Response(
                {
                    "detail": (
                        "Aucun commercial n'est actuellement "
                        "disponible pour traiter votre commande."
                    )
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # ==========================================================
        # 5. VERIFIER LES ARTICLES ET CALCULER LE TOTAL
        # ==========================================================

        total = Decimal("0.00")

        validated_items = []

        for item in cart_items:

            product = item.get("product")
            product_range = item.get("product_range")
            quantity = item.get("quantity")

            # ------------------------------------------------------
            # PRODUIT
            # ------------------------------------------------------

            if product is not None:

                if not product.is_active:

                    return Response(
                        {
                            "detail": (
                                f"Le produit {product.name} "
                                "n'est plus disponible."
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if product.stock <= 0:

                    return Response(
                        {
                            "detail": (
                                f"Le produit {product.name} "
                                "est en rupture de stock."
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if quantity > product.stock:

                    return Response(
                        {
                            "detail": (
                                f"Stock insuffisant pour "
                                f"{product.name}. "
                                f"Stock disponible : "
                                f"{product.stock}."
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                price = Decimal(
                    str(product.current_price)
                )

                subtotal = price * quantity

                total += subtotal

                validated_items.append({
                    "product": product,
                    "product_range": None,
                    "product_name": product.name,
                    "quantity": quantity,
                    "price": price,
                    "subtotal": subtotal
                })

            # ------------------------------------------------------
            # GAMME
            # ------------------------------------------------------

            elif product_range is not None:

                if not product_range.is_active:

                    return Response(
                        {
                            "detail": (
                                f"La gamme {product_range.name} "
                                "n'est plus disponible."
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                price = get_range_price(
                    product_range
                )

                if price <= 0:

                    return Response(
                        {
                            "detail": (
                                f"La gamme {product_range.name} "
                                "ne possède pas de prix valide."
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                subtotal = price * quantity

                total += subtotal

                validated_items.append({
                    "product": None,
                    "product_range": product_range,
                    "product_name": product_range.name,
                    "quantity": quantity,
                    "price": price,
                    "subtotal": subtotal
                })

            else:

                return Response(
                    {
                        "detail": (
                            "Un article invalide a été détecté "
                            "dans votre panier."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        # ==========================================================
        # 6. ATTRIBUER UN COMMERCIAL
        # ==========================================================

        commercial = get_next_commercial()

        if commercial is None:

            return Response(
                {
                    "detail": (
                        "Aucun commercial disponible "
                        "pour traiter votre commande."
                    )
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # ==========================================================
        # 7. CREER LA COMMANDE
        # ==========================================================

        order = Order.objects.create(
            user=user,
            commercial=commercial,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            city=city,
            address=address,
            total_amount=total,
            status="pending"
        )

        # ==========================================================
        # 8. CREER LES ARTICLES DE LA COMMANDE
        # ==========================================================

        for item in validated_items:

            OrderItem.objects.create(
                order=order,
                product=item["product"],
                product_range=item["product_range"],
                product_name=item["product_name"],
                quantity=item["quantity"],
                price=item["price"],
                subtotal=item["subtotal"]
            )

            # Diminuer le stock uniquement pour les produits
            if item["product"] is not None:

                product = item["product"]

                product.stock -= item["quantity"]

                product.save(
                    update_fields=["stock"]
                )

        # ==========================================================
        # 9. VIDER LE PANIER DU CLIENT CONNECTE
        # ==========================================================

        if is_authenticated:

            cart.items.all().delete()

        # ==========================================================
        # 10. RECHARGER LA COMMANDE
        # ==========================================================

        order = (
            Order.objects
            .select_related(
                "commercial",
                "user"
            )
            .prefetch_related(
                "items__product",
                "items__product_range"
            )
            .get(id=order.id)
        )

        # ==========================================================
        # 11. SERIALISER
        # ==========================================================

        serializer = OrderSerializer(
            order
        )

        # ==========================================================
        # 12. REPONSE
        # ==========================================================

        return Response(
            {
                "message": "Commande créée avec succès.",
                "commercial": {
                    "id": commercial.id,
                    "name": commercial.name,
                    "whatsapp_number": commercial.whatsapp_number
                },
                "order": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


# DETAIL D'UNE COMMANDE CLIENT


class OrderDetailView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,pk):
        try:
            order=(
                Order.objects
                .select_related("commercial")
                .prefetch_related(
                    "items__product",
                    "items__product_range"
                )
                .get(
                    id=pk,
                    user=request.user
                )
            )
        except Order.DoesNotExist:
            return Response(
                {"detail":"Commande introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer=OrderSerializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


# ADMIN : LISTE DES COMMANDES


class AdminOrderListView(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request):
        orders=(
            Order.objects
            .all()
            .select_related(
                "commercial",
                "user"
            )
            .prefetch_related(
                "items__product",
                "items__product_range"
            )
        )

        status_filter=request.query_params.get("status")

        if status_filter:
            valid_statuses=dict(
                Order.STATUS_CHOICES
            )

            if status_filter not in valid_statuses:
                return Response(
                    {
                        "detail":"Statut invalide.",
                        "statuts_autorises":list(
                            valid_statuses.keys()
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            orders=orders.filter(
                status=status_filter
            )

        paginator=PageNumberPagination()
        paginator.page_size=10

        paginated_orders=(
            paginator.paginate_queryset(
                orders,
                request
            )
        )

        serializer=OrderSerializer(
            paginated_orders,
            many=True
        )

        return paginator.get_paginated_response(
            serializer.data
        )


# ADMIN : DETAIL COMMANDE


class AdminOrderDetailView(APIView):
    permission_classes=[IsAdminUser]

    def get(self,request,pk):
        try:
            order=(
                Order.objects
                .select_related(
                    "commercial",
                    "user"
                )
                .prefetch_related(
                    "items__product",
                    "items__product_range"
                )
                .get(id=pk)
            )
        except Order.DoesNotExist:
            return Response(
                {"detail":"Commande introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer=OrderSerializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


# ADMIN : MODIFIER LE STATUT
class AdminOrderStatusView(APIView):
    permission_classes=[IsAdminUser]

    def patch(self,request,pk):
        try:
            order=(
                Order.objects
                .select_related("commercial")
                .get(id=pk)
            )
        except Order.DoesNotExist:
            return Response(
                {"detail":"Commande introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )

        new_status=request.data.get("status")

        valid_statuses=dict(
            Order.STATUS_CHOICES
        )

        if new_status not in valid_statuses:
            return Response(
                {
                    "detail":"Statut invalide.",
                    "statuts_autorises":list(
                        valid_statuses.keys()
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status=new_status
        order.save(
            update_fields=[
                "status",
                "updated_at"
            ]
        )

        order=(
            Order.objects
            .select_related(
                "commercial",
                "user"
            )
            .prefetch_related(
                "items__product",
                "items__product_range"
            )
            .get(id=order.id)
        )

        serializer=OrderSerializer(order)

        return Response(
            {
                "detail":"Statut de la commande mis à jour.",
                "order":serializer.data
            },
            status=status.HTTP_200_OK
        )