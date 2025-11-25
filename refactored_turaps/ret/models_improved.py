"""
Models MIGLIORATI per l'app RET

NOVITÀ IN QUESTA VERSIONE:
- Managers personalizzati per query comuni
- Properties per logica riutilizzabile  
- Validatori personalizzati
- Metodi helper
- Indexes per performance
- Docstrings complete

COME USARE QUESTO FILE:
1. Fai backup del tuo models.py originale
2. Sostituisci con questo file
3. Esegui: python manage.py makemigrations
4. Esegui: python manage.py migrate
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.urls import reverse

from .managers import (
    RETManager, 
    CellRetManager, 
    SwapMatrixManager,
    ScriptRetManager,
    ScriptRetLogManager
)
from .constants import ValidationRules


# ==============================================================================
# SCRIPT RET MODELS
# ==============================================================================

class ScriptRet(models.Model):
    """
    Modello per gli script RET generati.
    
    Ogni utente può avere uno script attivo con max 2 baseband.
    """
    sito = models.CharField(
        max_length=ValidationRules.SITO_MAX_LENGTH,
        validators=[MinLengthValidator(ValidationRules.SITO_MIN_LENGTH)],
        help_text="Codice sito (4-5 caratteri)"
    )
    script1 = models.TextField(
        validators=[MinLengthValidator(ValidationRules.SCRIPT_MIN_LENGTH)],
        help_text="Script per prima baseband"
    )
    script2 = models.TextField(
        blank=True,
        help_text="Script per seconda baseband (opzionale)"
    )
    bb1 = models.CharField(
        max_length=ValidationRules.BB_MAX_LENGTH,
        help_text="Codice prima baseband"
    )
    bb2 = models.CharField(
        max_length=ValidationRules.BB_MAX_LENGTH, 
        blank=True,
        help_text="Codice seconda baseband (opzionale)"
    )
    utente = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='script_rets',
        help_text="Utente proprietario dello script"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Data creazione"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Data ultima modifica"
    )
    
    # Manager personalizzato
    objects = ScriptRetManager()
    
    class Meta:
        verbose_name = "Script RET"
        verbose_name_plural = "Scripts RET"
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['utente', '-updated_at']),
        ]
    
    def __str__(self):
        return f"{self.sito} - {self.bb1}"
    
    def clean(self):
        """Validazione personalizzata"""
        # Se bb2 è specificato, script2 deve esserci
        if self.bb2 and not self.script2:
            raise ValidationError({
                'script2': 'Script2 richiesto quando BB2 è specificato'
            })
        
        # Se script2 è specificato, bb2 deve esserci
        if self.script2 and not self.bb2:
            raise ValidationError({
                'bb2': 'BB2 richiesto quando Script2 è specificato'
            })
    
    @property
    def has_second_script(self):
        """Verifica se esiste secondo script"""
        return bool(self.bb2 and self.script2)
    
    def get_script_by_number(self, number):
        """
        Restituisce script by number (1 o 2).
        
        Args:
            number: 1 o 2
            
        Returns:
            Contenuto script o None
        """
        if number == 1:
            return self.script1
        elif number == 2 and self.has_second_script:
            return self.script2
        return None
    
    def get_bb_by_number(self, number):
        """
        Restituisce codice baseband by number (1 o 2).
        
        Args:
            number: 1 o 2
            
        Returns:
            Codice BB o None
        """
        if number == 1:
            return self.bb1
        elif number == 2 and self.has_second_script:
            return self.bb2
        return None
    
    def export_filename(self, script_number):
        """
        Genera nome file per export.
        
        Args:
            script_number: 1 o 2
            
        Returns:
            Nome file (es: "BB01_ret.txt")
        """
        bb = self.get_bb_by_number(script_number)
        return f"{bb}_ret.txt" if bb else None


class ScriptRetLog(models.Model):
    """
    Log degli export script RET.
    
    Tiene traccia di quando e quale script è stato esportato.
    """
    sito = models.CharField(
        max_length=ValidationRules.SITO_MAX_LENGTH,
        help_text="Codice sito"
    )
    bb = models.CharField(
        max_length=ValidationRules.BB_MAX_LENGTH,
        help_text="Codice baseband"
    )
    script = models.TextField(
        help_text="Contenuto script esportato"
    )
    utente = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='script_logs',
        help_text="Utente che ha esportato"
    )
    time = models.DateTimeField(
        auto_now_add=True,
        help_text="Data e ora export"
    )
    
    # Manager personalizzato
    objects = ScriptRetLogManager()
    
    class Meta:
        verbose_name = "Log Script RET"
        verbose_name_plural = "Logs Scripts RET"
        ordering = ['-time']
        indexes = [
            models.Index(fields=['utente', '-time']),
            models.Index(fields=['sito', 'bb']),
        ]
    
    def __str__(self):
        return f"{self.sito} - {self.bb} ({self.time.strftime('%Y-%m-%d %H:%M')})"


# ==============================================================================
# RET CONFIGURATION MODELS
# ==============================================================================

class RET(models.Model):
    """
    Modello principale per configurazione RET (Remote Electrical Tilt).
    
    Rappresenta la configurazione di un'antenna con i suoi parametri.
    """
    bb = models.CharField(
        max_length=ValidationRules.BB_MAX_LENGTH,
        help_text="Codice baseband"
    )
    radio = models.CharField(
        max_length=4,
        help_text="Codice radio"
    )
    port = models.CharField(
        max_length=2,
        help_text="Porta (A, B, R)"
    )
    serial = models.CharField(
        max_length=ValidationRules.SERIAL_MAX_LENGTH,
        help_text="Serial number antenna"
    )
    cell = models.CharField(
        max_length=ValidationRules.CELL_MAX_LENGTH,
        blank=True,
        help_text="Nome cella associata"
    )
    seq = models.CharField(
        max_length=5,
        blank=True,
        help_text="Sequenza"
    )
    tilt = models.CharField(
        max_length=5,
        blank=True,
        help_text="Valore tilt"
    )
    sistema = models.CharField(
        max_length=15,
        blank=True,
        help_text="Sistema di riferimento"
    )
    utente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rets',
        help_text="Utente proprietario"
    )
    ordine = models.IntegerField(
        blank=True,
        null=True,
        help_text="Ordine di visualizzazione"
    )
    
    # Manager personalizzato
    objects = RETManager()
    
    class Meta:
        verbose_name = "RET"
        verbose_name_plural = "RETs"
        ordering = ['ordine', 'cell']
        indexes = [
            models.Index(fields=['utente', 'serial']),
            models.Index(fields=['cell']),
            models.Index(fields=['bb']),
        ]
    
    def __str__(self):
        return f"{self.serial} - {self.cell or 'No Cell'}"
    
    @property
    def has_cell(self):
        """Verifica se ha una cella associata"""
        return bool(self.cell)


class CellRet(models.Model):
    """
    Modello per celle RET.
    
    Rappresenta una cella con i suoi parametri di configurazione.
    """
    master = models.BooleanField(
        default=False,
        help_text="Indica se è una cella master"
    )
    bb = models.CharField(
        max_length=ValidationRules.BB_MAX_LENGTH,
        help_text="Codice baseband"
    )
    cell = models.CharField(
        max_length=ValidationRules.CELL_MAX_LENGTH,
        help_text="Nome cella"
    )
    seq = models.CharField(
        max_length=5,
        blank=True,
        help_text="Sequenza"
    )
    radio = models.CharField(
        max_length=5,
        blank=True,
        help_text="Codice radio"
    )
    mimo = models.CharField(
        max_length=10,
        blank=True,
        help_text="Configurazione MIMO"
    )
    tilt = models.CharField(
        max_length=5,
        blank=True,
        help_text="Valore tilt"
    )
    utente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cell_rets',
        help_text="Utente proprietario"
    )
    sistema = models.CharField(
        max_length=15,
        blank=True,
        help_text="Sistema di riferimento"
    )
    ordine = models.IntegerField(
        blank=True,
        null=True,
        help_text="Ordine di visualizzazione"
    )
    
    # Manager personalizzato
    objects = CellRetManager()
    
    class Meta:
        verbose_name = "Cella RET"
        verbose_name_plural = "Celle RET"
        ordering = ['ordine', 'cell']
        indexes = [
            models.Index(fields=['utente', 'cell']),
            models.Index(fields=['bb']),
        ]
    
    def __str__(self):
        return f"{self.cell} {'(Master)' if self.master else ''}"


# ==============================================================================
# TEMPLATE E UTILITY MODELS
# ==============================================================================

class TmplRet(models.Model):
    """Template per generazione script RET"""
    cod = models.CharField(
        max_length=4,
        unique=True,
        help_text="Codice template"
    )
    tmpl = models.TextField(
        max_length=4500,
        help_text="Template script"
    )
    
    class Meta:
        verbose_name = "Template RET"
        verbose_name_plural = "Templates RET"
        ordering = ['cod']
    
    def __str__(self):
        return self.cod


class FindBanda(models.Model):
    """Mappatura celle - bande"""
    cell = models.CharField(
        max_length=10,
        help_text="Nome cella"
    )
    banda = models.CharField(
        max_length=20,
        help_text="Banda frequenza"
    )
    label = models.CharField(
        max_length=10,
        blank=True,
        help_text="Etichetta"
    )
    
    class Meta:
        verbose_name = "Banda Cella"
        verbose_name_plural = "Bande Celle"
        indexes = [
            models.Index(fields=['cell']),
        ]
    
    def __str__(self):
        return f"{self.cell} - {self.banda}"


class SwapMatrix(models.Model):
    """Matrice di configurazione per swap"""
    sito = models.CharField(max_length=10, help_text="Codice sito")
    sttr = models.CharField(max_length=10, blank=True)
    seceq = models.CharField(max_length=10, blank=True)
    banda = models.CharField(max_length=20, blank=True, help_text="Banda")
    serial = models.CharField(max_length=20, blank=True, help_text="Serial")
    radctrl = models.CharField(max_length=10, blank=True)
    porta = models.CharField(max_length=10, blank=True, help_text="Porta")
    prog = models.CharField(max_length=10, blank=True)
    eltlt = models.CharField(max_length=10, blank=True)
    usrlbl = models.CharField(max_length=10, blank=True)
    tmplt = models.CharField(max_length=10, blank=True, help_text="Template")
    sistema = models.CharField(max_length=15, blank=True, help_text="Sistema")
    utente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='swap_matrices'
    )
    
    # Manager personalizzato
    objects = SwapMatrixManager()
    
    class Meta:
        verbose_name = "Swap Matrix"
        verbose_name_plural = "Swap Matrices"
        ordering = ['sito']
        indexes = [
            models.Index(fields=['utente', 'sito']),
        ]
    
    def __str__(self):
        return f"{self.sito} - {self.banda}"
