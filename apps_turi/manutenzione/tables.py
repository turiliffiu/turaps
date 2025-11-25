import django_tables2 as tables
from .models import TmplTma
from django_tables2.utils import Accessor


class TmplTmaTable(tables.Table):
    cod = tables.LinkColumn("dettaglio_template", args=[Accessor("pk")])
    
    #cod = tables.Column(order_by=('cod', 'tmpl'))
    #tmpl = tables.Column(order_by=('tmpl', 'cod'))


    class Meta:
        model = TmplTma
        fields = ('cod', 'tmpl')