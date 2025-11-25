"""
Decoratori personalizzati per l'app RET

Questi decoratori semplificano la gestione di controlli ricorrenti
nelle views, rendendo il codice più pulito e riutilizzabile.
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .models import RET, ScriptRet, SwapMatrix
from .constants import Messages


def require_ret_data(redirect_to='edit_ret'):
    """
    Decorator che verifica la presenza di dati RET per l'utente corrente.
    
    Args:
        redirect_to: Nome della view a cui reindirizzare se non ci sono dati
    
    Uso:
        @login_required
        @require_ret_data()
        def view_ret(request):
            # Qui sei sicuro che ci sono dati RET
            pass
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not RET.objects.filter(utente=request.user).exists():
                messages.warning(request, Messages.NO_RET_DATA)
                return redirect(redirect_to)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_script(redirect_to='generate_script_ret'):
    """
    Decorator che verifica la presenza di script per l'utente corrente.
    
    Args:
        redirect_to: Nome della view a cui reindirizzare se non c'è script
    
    Uso:
        @login_required
        @require_script()
        def view_script_ret(request):
            # Qui sei sicuro che c'è uno script
            pass
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not ScriptRet.objects.filter(utente=request.user).exists():
                messages.warning(request, Messages.NO_SCRIPT_FOUND)
                return redirect(redirect_to)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_swap_matrix(redirect_to='home'):
    """
    Decorator che verifica la presenza di dati SwapMatrix.
    
    Args:
        redirect_to: Nome della view a cui reindirizzare se non ci sono dati
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not SwapMatrix.objects.filter(utente=request.user).exists():
                messages.warning(request, "Devi prima creare una SwapMatrix")
                return redirect(redirect_to)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def handle_exceptions(error_message=Messages.ERROR_GENERIC, redirect_to='home'):
    """
    Decorator che gestisce le eccezioni in modo centralizzato.
    
    Args:
        error_message: Messaggio da mostrare in caso di errore
        redirect_to: View a cui reindirizzare in caso di errore
    
    Uso:
        @login_required
        @handle_exceptions(error_message="Errore elaborazione dati")
        def complex_view(request):
            # Eventuali eccezioni vengono gestite automaticamente
            pass
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            try:
                return view_func(request, *args, **kwargs)
            except Exception as e:
                # Log dell'errore
                import logging
                logger = logging.getLogger('ret')
                logger.error(
                    f"Error in {view_func.__name__}: {str(e)}", 
                    exc_info=True,
                    extra={'user': request.user.id if request.user.is_authenticated else None}
                )
                
                # Mostra messaggio all'utente
                messages.error(request, error_message)
                return redirect(redirect_to)
        return wrapper
    return decorator


def log_action(action_name):
    """
    Decorator che logga l'esecuzione di una view.
    
    Args:
        action_name: Nome dell'azione da loggare
    
    Uso:
        @login_required
        @log_action("Export Script")
        def export_script(request):
            pass
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            import logging
            logger = logging.getLogger('ret')
            
            user = request.user.username if request.user.is_authenticated else 'Anonymous'
            logger.info(f"{action_name} - User: {user}")
            
            result = view_func(request, *args, **kwargs)
            
            logger.info(f"{action_name} completed - User: {user}")
            return result
        return wrapper
    return decorator


# ==============================================================================
# UTILITY DECORATORS
# ==============================================================================

def ajax_required(view_func):
    """
    Decorator che permette solo richieste AJAX.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            messages.error(request, "Richiesta non valida")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def post_required(view_func):
    """
    Decorator che permette solo richieste POST.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.method != 'POST':
            messages.error(request, "Metodo non permesso")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper
