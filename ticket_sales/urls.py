from os import name
from django.urls import path
from . import views
from .views import *

urlpatterns=[
  
	path('',views.index, name = 'home_page'),
	path('matches/',views.matches, name = 'matchespage'),
	path('matches/search/',views.search_match, name = 'matchsearchpage'),
	path('sales/',views.sales, name = 'salespage'),
	path('staduims/<int:id>',views.staduim_detail,name='staduim_matches'),
	# path('tickets/<int:match_id>', views.buy_ticket, name='buy'),

	path('buy/<match_id>/', buy_ticket, name="buy"),

	path('staduim/',staduims, name = 'staduimspage'),
	path('payment/',payment_page, name = 'payment'),
	# path('generate_pdf'),
	path('tickets/export_pdf/', views.export_pdf,name = 'export_pdf'),
	path('test',views.gen_qrcode,name = 'test'),
	# path('render-pdf', views.render_pdf, name = 'render'),
]