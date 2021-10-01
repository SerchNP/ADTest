from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
	# url(r'^carrito/$', 						views.showShoppingCart, 		name='show-cart'),
	# url(r'^carrito/limpiar/$', 				views.emptyShoppingCart, 		name='clean-cart'),
	# url(r'^carrito/concretar-compra/$', 	views.checkout, 				name='checkout'),
	# url(r'^carrito/procesar/$', 			apiviews.process_cart, 			name='process-purchase'),
	# url(r'^carrito/comprar-ahora/$', 		apiviews.add_secundary_cart, 	name='add-secundario-cart-api'),
	# url(r'^carrito/agregar/$', 				apiviews.add_cart, 				name='add-cart-api'),
	# url(r'^carrito/aumentar/$', 			apiviews.increase_cart, 		name='increase-cart-api'),
	# url(r'^carrito/disminuir/$', 			apiviews.decrease_cart, 		name='decrease-cart-api'),
	# url(r'^carrito/cantidad/$', 			apiviews.quantity_cart, 		name='quantity-cart-api'),
	# url(r'^carrito/quitar/$', 				apiviews.remove_cart, 			name='remove-cart-api'),

	# URL para leer los datos del metrobus
	path('pipeline/metrobus/consultar', 	views.getMetrobusInfo, 					name='metrobus-info'),
	# URL empleada al momento de procesar la compra para envíos foráneos
	# path('carrito/cotizar-envio/', 			apiviews.cotizar_envio, 		name='quote-shipping'),
	# # path('carrito/rastrear-envio/', 		apiviews.rastrear_envio, 		name='track-shipping'),

	# path('carrito/olvidado/', 				apiviews.forgetCart, 			name='forget-cart'),	
]
