from django.urls import path

from .views import ImportEPGStationFormView, TopView, VideoFileView

urlpatterns = [
    path('', TopView.as_view(), name='top'),
    # path('album/<str:pk>/', AlbumDetailView.as_view(), name='album_detail'),
    path('videos/file/<uuid:pk>/',
         VideoFileView.as_view(),
         name='videos-file'),
    path('import-epgstation/',
         ImportEPGStationFormView.as_view(),
         name='import_epgstation'),
]
