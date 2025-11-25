"""
Costanti per l'app RET

Questo file centralizza tutti i valori "magic number" e stringhe hardcoded
per migliorare la manutenibilità del codice.
"""

# ==============================================================================
# LAYER TYPES
# ==============================================================================

class LayerType:
    """Tipi di layer per configurazione antenne"""
    FIRST = "primo"
    SECOND = "secondo"


# ==============================================================================
# MIMO CONFIGURATIONS
# ==============================================================================

class MIMOConfig:
    """Configurazioni MIMO"""
    MIMO_2X4 = "MIMO2x4"
    MIMO_4X4 = "MIMO4x4"
    
    LTE_700_TYPES = [MIMO_2X4]
    HIGH_MIMO_TYPES = [MIMO_4X4]


# ==============================================================================
# CELL NAMING
# ==============================================================================

class CellNaming:
    """Costanti per naming celle"""
    CELL_NAME_START = 4
    CELL_NAME_END = 6
    SEPARATOR = "-"
    SUFFIX_1 = "_1"
    SUFFIX_2 = "_2"


# ==============================================================================
# PORT TYPES
# ==============================================================================

class PortType:
    """Tipi di porte per RET"""
    PORT_A = "A"
    PORT_B = "B"
    PORT_R = "R"
    
    ALL_PORTS = [PORT_A, PORT_B, PORT_R]


# ==============================================================================
# SCRIPT SETTINGS
# ==============================================================================

class ScriptSettings:
    """Impostazioni per generazione script"""
    SCRIPT_NUMBER_1 = 1
    SCRIPT_NUMBER_2 = 2
    
    FILE_EXTENSION = ".txt"
    FILE_SUFFIX = "_ret"
    
    # Template placeholders
    PLACEHOLDERS = {
        'SITO': 'sito',
        'STTR': 'sttr',
        'SECEQ': 'seceq',
        'BANDA': 'banda',
        'SERIAL': 'serial',
        'RADCTRL': 'radctrl',
        'PORTA': 'porta',
        'PROG': 'prog',
        'ELTLT': 'eltlt',
        'USRLBL': 'usrlbl',
        'SISTEMA': 'sistema',
    }


# ==============================================================================
# VALIDATION RULES
# ==============================================================================

class ValidationRules:
    """Regole di validazione"""
    SITO_MIN_LENGTH = 4
    SITO_MAX_LENGTH = 5
    BB_MAX_LENGTH = 5
    CELL_MAX_LENGTH = 10
    SERIAL_MAX_LENGTH = 30
    
    SCRIPT_MIN_LENGTH = 10


# ==============================================================================
# DATABASE SETTINGS
# ==============================================================================

class DatabaseSettings:
    """Impostazioni database"""
    DELETE_MARKER = "delete"  # Marker per record da eliminare


# ==============================================================================
# FILE SETTINGS
# ==============================================================================

class FileSettings:
    """Impostazioni per gestione file"""
    CONTENT_TYPE_TEXT = 'text/plain'
    CONTENT_TYPE_JSON = 'application/json'
    
    DISPOSITION_ATTACHMENT = 'attachment; filename="{filename}"'


# ==============================================================================
# MESSAGES
# ==============================================================================

class Messages:
    """Messaggi utente"""
    NO_SCRIPT_FOUND = "Nessuno script trovato. Genera prima uno script."
    NO_RET_DATA = "Nessun dato RET disponibile. Elabora prima i dati."
    SCRIPT_GENERATED = "Script generato con successo."
    DATA_SAVED = "Dati salvati con successo."
    DATA_DELETED = "Dati eliminati con successo."
    
    ERROR_GENERIC = "Si è verificato un errore. Riprova."
    ERROR_NO_TEMPLATE = "Template {code} non trovato."
    ERROR_INVALID_DATA = "Dati non validi."
