from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from products.models import Product,ProductRange
from .models import Cart,CartItem
from .serializers import CartSerializer,CartItemSerializer,SyncCartItemSerializer

class CartView(generics.RetrieveAPIView):
    serializer_class=CartSerializer
    permission_classes=[IsAuthenticated]
    def get_object(self):
        cart,_=Cart.objects.get_or_create(user=self.request.user)
        return cart

class AddToCartView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]
    @transaction.atomic
    def post(self,request):
        product_id=request.data.get("product")
        quantity=request.data.get("quantity",1)
        if not product_id:
            return Response(
                {"message":"Le produit est obligatoire."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            quantity=int(quantity)
        except (TypeError,ValueError):
            return Response(
                {"message":"La quantité doit être un nombre entier."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if quantity<=0:
            return Response(
                {"message":"La quantité doit être supérieure à zéro."},
                status=status.HTTP_400_BAD_REQUEST
            )
        product=get_object_or_404(
            Product,
            id=product_id,
            is_active=True
        )
        if product.stock<=0:
            return Response(
                {"message":"Ce produit est actuellement en rupture de stock."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if quantity>product.stock:
            return Response(
                {"message":f"Stock disponible : {product.stock}."},
                status=status.HTTP_400_BAD_REQUEST
            )
        cart,_=Cart.objects.get_or_create(user=request.user)
        cart_item=CartItem.objects.filter(
            cart=cart,
            product=product,
            product_range__isnull=True
        ).first()
        if cart_item:
            new_quantity=cart_item.quantity+quantity
            if new_quantity>product.stock:
                return Response(
                    {"message":f"Stock disponible : {product.stock}."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity=new_quantity
            cart_item.save(update_fields=["quantity"])
        else:
            cart_item=CartItem.objects.create(
                cart=cart,
                product=product,
                product_range=None,
                quantity=quantity
            )
        return Response(
            {
                "message":"Produit ajouté au panier.",
                "item":CartItemSerializer(cart_item).data,
                "cart":CartSerializer(cart).data
            },
            status=status.HTTP_201_CREATED
        )

class SyncCartView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]
    @transaction.atomic
    def post(self,request):
        items=request.data.get("items",[])
        if not isinstance(items,list):
            return Response(
                {"message":"Le panier doit être une liste."},
                status=status.HTTP_400_BAD_REQUEST
            )
        cart,_=Cart.objects.get_or_create(user=request.user)
        local_products={}
        local_ranges={}
        for item in items:
            serializer=SyncCartItemSerializer(data=item)
            if not serializer.is_valid():
                return Response(
                    {
                        "message":"Données du panier invalides.",
                        "errors":serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            item_type=serializer.validated_data["type"]
            quantity=serializer.validated_data["quantity"]
            if item_type=="product":
                product_id=serializer.validated_data.get("product")
                if product_id:
                    local_products[product_id]=quantity
            elif item_type=="range":
                range_id=serializer.validated_data.get("product_range")
                if range_id:
                    local_ranges[range_id]=quantity
        for cart_item in cart.items.all():
            if cart_item.product_id is not None:
                if cart_item.product_id not in local_products:
                    cart_item.delete()
            elif cart_item.product_range_id is not None:
                if cart_item.product_range_id not in local_ranges:
                    cart_item.delete()
            else:
                cart_item.delete()
        for product_id,quantity in local_products.items():
            product=Product.objects.filter(
                id=product_id,
                is_active=True
            ).first()
            if not product:
                continue
            if product.stock<=0:
                CartItem.objects.filter(
                    cart=cart,
                    product=product,
                    product_range__isnull=True
                ).delete()
                continue
            quantity=min(
                quantity,
                product.stock
            )
            if quantity<=0:
                continue
            cart_item=CartItem.objects.filter(
                cart=cart,
                product=product,
                product_range__isnull=True
            ).first()
            if cart_item:
                cart_item.quantity=quantity
                cart_item.save(update_fields=["quantity"])
            else:
                CartItem.objects.create(
                    cart=cart,
                    product=product,
                    product_range=None,
                    quantity=quantity
                )
        for range_id,quantity in local_ranges.items():
            product_range=ProductRange.objects.filter(
                id=range_id,
                is_active=True
            ).first()
            if not product_range:
                continue
            if quantity<=0:
                continue
            cart_item=CartItem.objects.filter(
                cart=cart,
                product__isnull=True,
                product_range=product_range
            ).first()
            if cart_item:
                cart_item.quantity=quantity
                cart_item.save(update_fields=["quantity"])
            else:
                CartItem.objects.create(
                    cart=cart,
                    product=None,
                    product_range=product_range,
                    quantity=quantity
                )
        for cart_item in cart.items.select_related(
            "product",
            "product_range"
        ).all():
            if cart_item.product is not None:
                if (
                    not cart_item.product.is_active or
                    cart_item.product.stock<=0
                ):
                    cart_item.delete()
            elif cart_item.product_range is not None:
                if not cart_item.product_range.is_active:
                    cart_item.delete()
            else:
                cart_item.delete()
        cart.refresh_from_db()
        return Response(
            {
                "message":"Panier synchronisé avec succès.",
                "cart":CartSerializer(cart).data
            },
            status=status.HTTP_200_OK
        )

class UpdateCartItemView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]
    @transaction.atomic
    def patch(self,request,pk):
        item=CartItem.objects.filter(
            id=pk,
            cart__user=request.user
        ).select_related(
            "product",
            "product_range"
        ).first()
        if not item:
            return Response(
                {"message":"Article introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )
        quantity=request.data.get("quantity")
        try:
            quantity=int(quantity)
        except (TypeError,ValueError):
            return Response(
                {"message":"La quantité doit être un nombre entier."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if quantity<=0:
            return Response(
                {"message":"La quantité doit être supérieure à zéro."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if item.product is not None:
            if not item.product.is_active:
                item.delete()
                return Response(
                    {"message":"Ce produit n'est plus disponible."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if item.product.stock<=0:
                item.delete()
                return Response(
                    {"message":"Ce produit est en rupture de stock."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if quantity>item.product.stock:
                return Response(
                    {"message":f"Stock disponible : {item.product.stock}."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif item.product_range is not None:
            if not item.product_range.is_active:
                item.delete()
                return Response(
                    {"message":"Cette gamme n'est plus disponible."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            item.delete()
            return Response(
                {"message":"Article invalide."},
                status=status.HTTP_400_BAD_REQUEST
            )
        item.quantity=quantity
        item.save(update_fields=["quantity"])
        return Response(
            {
                "message":"Quantité mise à jour.",
                "item":CartItemSerializer(item).data,
                "cart":CartSerializer(item.cart).data
            },
            status=status.HTTP_200_OK
        )

class RemoveCartItemView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]
    @transaction.atomic
    def delete(self,request,pk):
        item=CartItem.objects.filter(
            id=pk,
            cart__user=request.user
        ).first()
        if not item:
            return Response(
                {"message":"Article introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )
        cart=item.cart
        item.delete()
        return Response(
            {
                "message":"Article supprimé du panier.",
                "cart":CartSerializer(cart).data
            },
            status=status.HTTP_200_OK
        )

class ClearCartView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]
    @transaction.atomic
    def post(self,request):
        cart,_=Cart.objects.get_or_create(
            user=request.user
        )
        cart.items.all().delete()
        return Response(
            {
                "message":"Panier vidé avec succès.",
                "cart":CartSerializer(cart).data
            },
            status=status.HTTP_200_OK
        )