"""
Managers personalizzati per i modelli RET

I managers semplificano le query comuni e centralizzano la logica
di accesso al database.
"""

from django.db import models
from django.db.models import Q


class RETManager(models.Manager):
    """Manager personalizzato per il modello RET"""
    
    def for_user(self, user):
        """
        Filtra RET per utente specifico.
        
        Args:
            user: Oggetto User o user_id
            
        Returns:
            QuerySet filtrato per utente
        
        Uso:
            rets = RET.objects.for_user(request.user)
        """
        if hasattr(user, 'id'):
            user_id = user.id
        else:
            user_id = user
        return self.filter(utente_id=user_id)
    
    def by_baseband(self, bb):
        """
        Filtra RET per baseband.
        
        Args:
            bb: Codice baseband
            
        Returns:
            QuerySet filtrato per baseband
        """
        return self.filter(bb=bb)
    
    def by_port(self, port):
        """
        Filtra RET per porta.
        
        Args:
            port: Tipo di porta (A, B, R)
            
        Returns:
            QuerySet filtrato per porta
        """
        return self.filter(port=port)
    
    def by_cell(self, cell):
        """
        Filtra RET per cella.
        
        Args:
            cell: Nome cella
            
        Returns:
            QuerySet filtrato per cella
        """
        return self.filter(cell=cell)
    
    def with_cells(self):
        """
        Include informazioni sulle celle associate.
        Ottimizza le query con select_related.
        
        Returns:
            QuerySet ottimizzato
        """
        return self.select_related('utente')
    
    def ordered(self):
        """
        Restituisce RET ordinati per ordine e cella.
        
        Returns:
            QuerySet ordinato
        """
        return self.order_by('ordine', 'cell')
    
    def get_duplicates_by_serial(self):
        """
        Trova RET con serial number duplicati.
        
        Returns:
            QuerySet di RET duplicati
        """
        from django.db.models import Count
        
        duplicates = self.values('serial').annotate(
            count=Count('serial')
        ).filter(count__gt=1).values_list('serial', flat=True)
        
        return self.filter(serial__in=duplicates)
    
    def remove_duplicates_by_serial(self, port_priority=['R', 'A', 'B']):
        """
        Rimuove RET con serial number duplicati, mantenendo quello con priorità porta maggiore.
        
        Args:
            port_priority: Lista di porte in ordine di priorità (default: R > A > B)
            
        Returns:
            Numero di record eliminati
        """
        deleted_count = 0
        
        for port in port_priority:
            port_rets = self.filter(port=port)
            for ret in port_rets:
                # Trova duplicati con porte a priorità inferiore
                lower_priority_ports = port_priority[port_priority.index(port) + 1:]
                duplicates = self.filter(
                    serial=ret.serial,
                    port__in=lower_priority_ports
                )
                deleted_count += duplicates.count()
                duplicates.delete()
        
        return deleted_count


class CellRetManager(models.Manager):
    """Manager personalizzato per il modello CellRet"""
    
    def for_user(self, user):
        """Filtra CellRet per utente"""
        if hasattr(user, 'id'):
            user_id = user.id
        else:
            user_id = user
        return self.filter(utente_id=user_id)
    
    def masters_only(self):
        """Restituisce solo le celle master"""
        return self.filter(master=True)
    
    def by_baseband(self, bb):
        """Filtra per baseband"""
        return self.filter(bb=bb)
    
    def by_system(self, sistema):
        """Filtra per sistema"""
        return self.filter(sistema=sistema)
    
    def ordered(self):
        """Restituisce celle ordinate"""
        return self.order_by('ordine', 'cell')
    
    def get_choices(self):
        """
        Restituisce lista di tuple per choices in form.
        
        Returns:
            List di tuple (cell, cell)
        
        Uso:
            CHOICES = [('', '')] + CellRet.objects.for_user(user).get_choices()
        """
        return list(self.values_list('cell', 'cell'))


class SwapMatrixManager(models.Manager):
    """Manager personalizzato per il modello SwapMatrix"""
    
    def for_user(self, user):
        """Filtra SwapMatrix per utente"""
        if hasattr(user, 'id'):
            user_id = user.id
        else:
            user_id = user
        return self.filter(utente_id=user_id)
    
    def by_baseband(self, bb):
        """Filtra per baseband"""
        return self.filter(sito__contains=bb)
    
    def by_system(self, sistema):
        """Filtra per sistema"""
        return self.filter(sistema=sistema)
    
    def ordered(self):
        """Restituisce record ordinati"""
        return self.order_by('sito', 'sttr')


class ScriptRetManager(models.Manager):
    """Manager personalizzato per il modello ScriptRet"""
    
    def for_user(self, user):
        """Filtra ScriptRet per utente"""
        if hasattr(user, 'id'):
            user_id = user.id
        else:
            user_id = user
        return self.filter(utente_id=user_id)
    
    def get_or_none(self, user):
        """
        Restituisce script per utente o None se non esiste.
        
        Args:
            user: Oggetto User
            
        Returns:
            ScriptRet object o None
        """
        return self.for_user(user).first()
    
    def clear_for_user(self, user):
        """
        Elimina tutti gli script di un utente.
        
        Args:
            user: Oggetto User
            
        Returns:
            Numero di record eliminati
        """
        queryset = self.for_user(user)
        count = queryset.count()
        queryset.delete()
        return count


class ScriptRetLogManager(models.Manager):
    """Manager personalizzato per il modello ScriptRetLog"""
    
    def for_user(self, user):
        """Filtra log per utente"""
        if hasattr(user, 'id'):
            user_id = user.id
        else:
            user_id = user
        return self.filter(utente_id=user_id)
    
    def recent(self, limit=10):
        """
        Restituisce i log più recenti.
        
        Args:
            limit: Numero massimo di record
            
        Returns:
            QuerySet ordinato per data decrescente
        """
        return self.order_by('-time')[:limit]
    
    def by_site(self, sito):
        """Filtra log per sito"""
        return self.filter(sito=sito)
    
    def by_baseband(self, bb):
        """Filtra log per baseband"""
        return self.filter(bb=bb)
