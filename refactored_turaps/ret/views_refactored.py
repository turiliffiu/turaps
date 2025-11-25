"""
Views REFACTORED per l'app RET

NOVITÀ IN QUESTA VERSIONE:
- Views più semplici e leggibili
- Logica business estratta in services
- Uso di decoratori per controlli comuni
- Gestione errori migliorata
- Logging appropriato
- Codice DRY (non ripetuto)

CONFRONTA CON LA VERSIONE ORIGINALE:
- export_script1_ret e export_script2_ret erano 2 funzioni quasi identiche
- Ora c'è UNA SOLA funzione export_script_ret con parametro
"""

import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from .models import RET, CellRet, ScriptRet
from .decorators import require_ret_data, require_script, handle_exceptions, log_action
from .services.export_service import ExportService
from .constants import Messages, ScriptSettings

logger = logging.getLogger('ret')


# ==============================================================================
# DELETE OPERATIONS
# ==============================================================================

@login_required
@log_action("Delete All RET")
@handle_exceptions(error_message=Messages.ERROR_GENERIC, redirect_to='view_ret')
def delete_allret(request):
    """
    Elimina tutti i dati RET dell'utente corrente.
    
    MIGLIORAMENTI:
    - Aggiunto logging
    - Gestione errori automatica
    - Messaggio di conferma
    """
    count = RET.objects.for_user(request.user).count()
    RET.objects.for_user(request.user).delete()
    
    messages.success(request, f"{count} record RET eliminati con successo")
    logger.info(f"Deleted {count} RET records for user {request.user.username}")
    
    return redirect('view_ret')


# ==============================================================================
# EXPORT OPERATIONS - ESEMPIO DI REFACTORING
# ==============================================================================

@login_required
@require_script()
@log_action("Export Script")
def export_script_ret(request, script_number):
    """
    Esporta script RET (unificazione di export_script1_ret ed export_script2_ret).
    
    PRIMA (codice duplicato):
        def export_script1_ret(request):
            # 50 righe di codice
            script = ScriptRet.objects.filter(utente=request.user.id)
            sito = script[0].sito
            bb1 = script[0].bb1
            script = script[0].script1
            nomefile = bb1 + "_ret.txt"
            # ... resto identico a export_script2_ret ...
        
        def export_script2_ret(request):
            # 50 righe di codice identico con bb1 -> bb2, script1 -> script2
    
    DOPO (DRY - Don't Repeat Yourself):
        Una sola funzione con parametro script_number
        Logica estratta in ExportService
    
    Args:
        script_number: 1 o 2 per selezionare quale script esportare
        
    Returns:
        HttpResponse con file da scaricare
    """
    try:
        # Delega la logica al service
        response = ExportService.export_script(request.user, script_number)
        
        messages.success(request, f"Script {script_number} esportato con successo")
        return response
        
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('view_script_ret')
        
    except ScriptRet.DoesNotExist:
        messages.error(request, Messages.NO_SCRIPT_FOUND)
        return redirect('generate_script_ret')


# ==============================================================================
# VIEW OPERATIONS
# ==============================================================================

@login_required
@require_ret_data()
def view_ret(request):
    """
    Visualizza e modifica dati RET.
    
    MIGLIORAMENTI:
    - Usa manager personalizzato (for_user)
    - Decoratore @require_ret_data per controllo dati
    - Codice più leggibile
    """
    # Recupera dati con manager
    rets = RET.objects.for_user(request.user).ordered()
    cells = CellRet.objects.for_user(request.user).ordered()
    
    # Prepara choices per dropdown
    cell_choices = [('', '')] + cells.get_choices()
    
    # TODO: Logica formset qui (vedi versione completa sotto)
    
    context = {
        'rets': rets,
        'cells': cells,
        'cell_choices': cell_choices,
    }
    
    return render(request, 'ret/view_ret.html', context)


@login_required
@require_script()
def view_script_ret(request):
    """
    Visualizza script generati.
    
    MIGLIORAMENTI:
    - Usa get_or_none invece di filter()[0]
    - Gestione caso script non trovato
    - Codice più sicuro
    """
    script = ScriptRet.objects.get_or_none(request.user)
    
    if not script:
        messages.warning(request, Messages.NO_SCRIPT_FOUND)
        return redirect('generate_script_ret')
    
    context = {
        "sito": script.sito,
        "script1": script.script1,
        "script2": script.script2,
        "bb1": script.bb1,
        "bb2": script.bb2,
        "has_script2": script.has_second_script,  # Property del model
    }
    
    return render(request, 'ret/view_script_ret.html', context)


# ==============================================================================
# UTILITY VIEWS
# ==============================================================================

@login_required
def export_history(request):
    """
    Visualizza storico export dell'utente.
    
    NUOVA FUNZIONALITÀ:
    - Mostra gli ultimi 20 export
    - Utile per tracking e audit
    """
    history = ExportService.get_export_history(request.user, limit=20)
    
    context = {
        'history': history,
    }
    
    return render(request, 'ret/export_history.html', context)


@login_required
@log_action("Clear Export History")
def clear_export_history(request):
    """
    Cancella storico export dell'utente.
    
    NUOVA FUNZIONALITÀ:
    - Permette pulizia dati vecchi
    """
    if request.method == 'POST':
        count = ExportService.clear_export_history(request.user)
        messages.success(request, f"Eliminati {count} record dallo storico")
        return redirect('export_history')
    
    return render(request, 'ret/clear_history_confirm.html')


# ==============================================================================
# ESEMPIO DI COME REFACTORARE UNA VIEW COMPLESSA
# ==============================================================================

"""
PRIMA - edit_ret originale (154 righe, logica complessa):

def edit_ret(request):
    adpr = Adpr.objects.filter(utente=request.user.id).order_by('pk')
    scan = Scan.objects.filter(type='RET', utente=request.user.id)
    objs = RET.objects.filter(utente=request.user.id)
    objs.delete()
    
    cell = ""
    bb_acq = False
    mimo = False
    lte700 = False
    
    for item in adpr:
        if item.mimo == "MIMO2x4":
            lte700 = True
        if item.mimo == "MIMO4x4":
            mimo = True
        if item.layer != "primo":
            # ... 100 righe di logica complessa ...
    
    # ... altro codice ...
    return redirect('view_ret')


DOPO - Versione refactored:

from .services.ret_processor import RETProcessor

@login_required
@log_action("Edit RET")
@handle_exceptions(error_message="Errore durante elaborazione RET")
def edit_ret(request):
    '''
    Elabora dati ADPR e Scan per creare configurazione RET.
    
    Questa view è molto più semplice perché delega al RETProcessor:
    - La logica complessa è nel service
    - La view si occupa solo di orchestrazione
    - Più facile da testare
    - Più facile da mantenere
    '''
    processor = RETProcessor()
    
    # Pulisci dati esistenti
    processor.clear_user_data(request.user)
    
    # Elabora ADPR -> CellRet
    cells_created = processor.process_adpr(request.user)
    logger.info(f"Created {cells_created} CellRet records")
    
    # Elabora Scan -> RET
    rets_created = processor.process_scan(request.user)
    logger.info(f"Created {rets_created} RET records")
    
    # Rimuovi duplicati
    duplicates_removed = processor.remove_duplicate_serials(request.user)
    if duplicates_removed > 0:
        logger.info(f"Removed {duplicates_removed} duplicate RET records")
    
    # Determina redirect
    next_view = processor.get_next_view(request.user)
    
    messages.success(request, "Dati RET elaborati con successo")
    return redirect(next_view)

# Ora la logica complessa è in services/ret_processor.py
# Molto più facile da testare, debuggare e mantenere!
"""
