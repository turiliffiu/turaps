"""
Service per gestione export file

Centralizza tutta la logica di export degli script RET,
eliminando codice duplicato e semplificando la manutenzione.
"""

import logging
from django.http import HttpResponse
from ..models import ScriptRet, ScriptRetLog
from ..constants import ScriptSettings, FileSettings

logger = logging.getLogger('ret')


class ExportService:
    """Service per gestione export script RET"""
    
    @staticmethod
    def export_script(user, script_number):
        """
        Esporta script RET per l'utente specificato.
        
        Args:
            user: Oggetto User
            script_number: 1 o 2 per selezionare script1 o script2
            
        Returns:
            HttpResponse con file da scaricare
            
        Raises:
            ValueError: Se script_number non è valido
            ScriptRet.DoesNotExist: Se non esiste script per l'utente
        """
        logger.info(f"Export script {script_number} for user {user.username}")
        
        # Valida script_number
        if script_number not in [ScriptSettings.SCRIPT_NUMBER_1, ScriptSettings.SCRIPT_NUMBER_2]:
            raise ValueError(f"Invalid script_number: {script_number}")
        
        # Recupera script
        script_obj = ScriptRet.objects.for_user(user).first()
        if not script_obj:
            raise ScriptRet.DoesNotExist("Nessuno script disponibile per questo utente")
        
        # Estrai dati script
        if script_number == ScriptSettings.SCRIPT_NUMBER_1:
            bb = script_obj.bb1
            script_content = script_obj.script1
        else:
            bb = script_obj.bb2
            script_content = script_obj.script2
            
            # Verifica che esista script2
            if not bb or not script_content:
                raise ValueError("Script 2 non disponibile")
        
        # Genera nome file
        filename = ExportService._generate_filename(bb)
        
        # Crea response HTTP
        response = ExportService._create_file_response(script_content, filename)
        
        # Log export
        ExportService._log_export(
            sito=script_obj.sito[:4],
            bb=bb,
            script=script_content,
            user=user
        )
        
        logger.info(f"Export completed: {filename} for user {user.username}")
        return response
    
    @staticmethod
    def _generate_filename(bb):
        """
        Genera nome file per export.
        
        Args:
            bb: Codice baseband
            
        Returns:
            Nome file (es: "BB01_ret.txt")
        """
        return f"{bb}{ScriptSettings.FILE_SUFFIX}{ScriptSettings.FILE_EXTENSION}"
    
    @staticmethod
    def _create_file_response(content, filename):
        """
        Crea HTTP response per download file.
        
        Args:
            content: Contenuto del file
            filename: Nome del file
            
        Returns:
            HttpResponse configurato per download
        """
        response = HttpResponse(
            content, 
            content_type=FileSettings.CONTENT_TYPE_TEXT
        )
        response['Content-Disposition'] = FileSettings.DISPOSITION_ATTACHMENT.format(
            filename=filename
        )
        return response
    
    @staticmethod
    def _log_export(sito, bb, script, user):
        """
        Registra l'export nel log.
        
        Args:
            sito: Codice sito
            bb: Codice baseband
            script: Contenuto script
            user: Oggetto User
        """
        try:
            ScriptRetLog.objects.create(
                sito=sito,
                bb=bb,
                script=script,
                utente=user
            )
            logger.debug(f"Export logged: {sito} - {bb}")
        except Exception as e:
            # Log error ma non bloccare export
            logger.error(f"Failed to log export: {e}", exc_info=True)
    
    @staticmethod
    def get_export_history(user, limit=10):
        """
        Recupera storico export per un utente.
        
        Args:
            user: Oggetto User
            limit: Numero massimo di record
            
        Returns:
            QuerySet di ScriptRetLog
        """
        return ScriptRetLog.objects.for_user(user).recent(limit)
    
    @staticmethod
    def clear_export_history(user):
        """
        Cancella storico export per un utente.
        
        Args:
            user: Oggetto User
            
        Returns:
            Numero di record eliminati
        """
        queryset = ScriptRetLog.objects.for_user(user)
        count = queryset.count()
        queryset.delete()
        logger.info(f"Cleared {count} export history records for user {user.username}")
        return count
