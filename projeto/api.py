
from rest_framework import routers

from projeto.apps.polare import api as polare_api

router = routers.DefaultRouter()
router.register('plano-individual', polare_api.PlanoIndividualViewSet)
router.register('plano-individual-progep', polare_api.PlanoIndividualPROGEPViewSet)

urls = router.urls, 'projeto', 'v1'
