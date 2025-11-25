# 📘 GUIDA INSTALLAZIONE FILES REFACTORED

## 🎯 PANORAMICA

Questa guida ti spiega come integrare i file refactored nel tuo progetto Django TURAPS.
I file sono stati organizzati per fasi, dalla più critica (sicurezza) alla più avanzata.

---

## ⚠️ IMPORTANTE: BACKUP PRIMA DI TUTTO

```bash
# Sul tuo server, fai backup completo
cd /home/django
tar -czf backup_turaps_$(date +%Y%m%d_%H%M%S).tar.gz apps_turi/
cp apps_turi/db.sqlite3 db.sqlite3.backup
```

---

## 📦 FASE 1: SICUREZZA E CONFIGURAZIONE (30 minuti)

### 1.1 Installa python-decouple

```bash
# Attiva virtual environment
source /home/django/django_env/bin/activate

# Installa python-decouple
pip install python-decouple

# Aggiorna requirements
pip freeze > /home/django/apps_turi/requirements.txt
```

### 1.2 Crea file .env

```bash
cd /home/django/apps_turi

# Copia il template .env.example (dal file che ti ho dato)
nano .env
```

Inserisci questi valori (PERSONALIZZALI!):

```bash
# Genera nuova SECRET_KEY
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Copia l'output e incollalo nel .env
SECRET_KEY=il-tuo-secret-key-generato

# Altre configurazioni
DEBUG=False
ALLOWED_HOSTS=tuo-ip-o-dominio.com,localhost

# Database (lascia così per SQLite)
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Security (se usi HTTPS)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

LOG_LEVEL=INFO
```

### 1.3 Sostituisci settings.py

```bash
# Backup settings originale
cp apps_turi/settings.py apps_turi/settings.py.original

# Copia il nuovo settings (dal file settings.py che ti ho dato)
# Usa il contenuto del file refactored_turaps/settings.py
nano apps_turi/apps_turi/settings.py
# Incolla il contenuto
```

### 1.4 Verifica che funzioni

```bash
# Test settings
python manage.py check

# Se va tutto bene dovresti vedere:
# System check identified no issues (0 silenced).

# Se ci sono errori, verifica il file .env
```

### 1.5 Crea directory logs

```bash
cd /home/django/apps_turi
mkdir -p logs
chmod 755 logs
```

### 1.6 Aggiorna .gitignore

```bash
nano .gitignore

# Aggiungi queste righe se non ci sono già
.env
*.log
logs/
db.sqlite3
```

---

## 📦 FASE 2: REFACTORING APP RET (1-2 ore)

### 2.1 Crea nuove directory

```bash
cd /home/django/apps_turi/ret

# Crea directory per servizi
mkdir -p services
touch services/__init__.py

# Crea directory per test (opzionale per ora)
mkdir -p tests
touch tests/__init__.py
```

### 2.2 Copia i nuovi file

```bash
cd /home/django/apps_turi/ret

# Copia questi file dalla cartella refactored_turaps/ret/
# 1. constants.py
nano constants.py
# [Incolla contenuto di refactored_turaps/ret/constants.py]

# 2. decorators.py
nano decorators.py
# [Incolla contenuto di refactored_turaps/ret/decorators.py]

# 3. managers.py
nano managers.py
# [Incolla contenuto di refactored_turaps/ret/managers.py]

# 4. services/export_service.py
nano services/export_service.py
# [Incolla contenuto di refactored_turaps/ret/services/export_service.py]
```

### 2.3 Aggiorna models.py (GRADUALE)

**OPZIONE A - Conservativa (CONSIGLIATA per iniziare):**

Aggiungi solo i managers ai modelli esistenti senza modificare altro:

```bash
nano models.py
```

Aggiungi all'inizio del file:

```python
from .managers import (
    RETManager, 
    CellRetManager, 
    SwapMatrixManager,
    ScriptRetManager,
    ScriptRetLogManager
)
```

Poi in ogni modello, aggiungi la riga del manager:

```python
class RET(models.Model):
    # ... campi esistenti ...
    
    objects = RETManager()  # <-- AGGIUNGI QUESTA RIGA

class CellRet(models.Model):
    # ... campi esistenti ...
    
    objects = CellRetManager()  # <-- AGGIUNGI QUESTA RIGA

# E così via per tutti i modelli
```

**OPZIONE B - Completa (dopo che la A funziona):**

Sostituisci completamente il models.py con quello migliorato:

```bash
cp models.py models.py.original
# Copia il contenuto di models_improved.py in models.py
```

Poi esegui le migrazioni:

```bash
python manage.py makemigrations ret
python manage.py migrate
```

### 2.4 Aggiorna views.py (GRADUALE)

**INIZIA SOSTITUENDO SOLO LE FUNZIONI DI EXPORT:**

```bash
nano views.py
```

1. Aggiungi import all'inizio:

```python
from .services.export_service import ExportService
from .decorators import require_script, log_action
from .constants import Messages
import logging

logger = logging.getLogger('ret')
```

2. COMMENTA (non eliminare) le vecchie funzioni export_script1_ret ed export_script2_ret:

```python
# def export_script1_ret(request):
#     ... tutto il codice vecchio ...

# def export_script2_ret(request):
#     ... tutto il codice vecchio ...
```

3. Aggiungi la nuova funzione unificata:

```python
@login_required
@require_script()
@log_action("Export Script")
def export_script_ret(request, script_number):
    """
    Esporta script RET (versione unificata e migliorata)
    """
    try:
        response = ExportService.export_script(request.user, script_number)
        messages.success(request, f"Script {script_number} esportato con successo")
        return response
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('view_script_ret')
    except Exception as e:
        logger.error(f"Export error: {e}", exc_info=True)
        messages.error(request, Messages.ERROR_GENERIC)
        return redirect('view_script_ret')
```

### 2.5 Aggiorna urls.py

```bash
nano urls.py
```

SOSTITUISCI le vecchie righe:

```python
# VECCHIO
path('export-script1-ret/', export_script1_ret, name='export_script1_ret'),
path('export-script2-ret/', export_script2_ret, name='export_script2_ret'),
```

Con:

```python
# NUOVO
path('export-script-ret/<int:script_number>/', export_script_ret, name='export_script_ret'),
```

### 2.6 Aggiorna i template HTML (se necessario)

Se hai template che linkano direttamente agli URL vecchi, aggiornali:

```html
<!-- VECCHIO -->
<a href="{% url 'export_script1_ret' %}">Esporta Script 1</a>
<a href="{% url 'export_script2_ret' %}">Esporta Script 2</a>

<!-- NUOVO -->
<a href="{% url 'export_script_ret' 1 %}">Esporta Script 1</a>
<a href="{% url 'export_script_ret' 2 %}">Esporta Script 2</a>
```

### 2.7 Testa!

```bash
# Riavvia server
python manage.py runserver

# Oppure se usi gunicorn
sudo systemctl restart gunicorn

# Testa export script nel browser
# Verifica i log
tail -f logs/django.log
```

---

## 📦 FASE 3: TESTING (Opzionale ma consigliato)

### 3.1 Crea file di test

```bash
cd /home/django/apps_turi/ret/tests

nano test_export_service.py
```

Contenuto:

```python
from django.test import TestCase
from django.contrib.auth.models import User
from ret.models import ScriptRet
from ret.services.export_service import ExportService


class ExportServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', password='12345')
        self.script = ScriptRet.objects.create(
            sito='TEST',
            script1='test script 1',
            bb1='BB01',
            script2='test script 2',
            bb2='BB02',
            utente=self.user
        )
    
    def test_export_script_1(self):
        """Test export primo script"""
        response = ExportService.export_script(self.user, 1)
        self.assertEqual(response.status_code, 200)
        self.assertIn('BB01_ret.txt', response['Content-Disposition'])
    
    def test_export_script_2(self):
        """Test export secondo script"""
        response = ExportService.export_script(self.user, 2)
        self.assertEqual(response.status_code, 200)
        self.assertIn('BB02_ret.txt', response['Content-Disposition'])
```

### 3.2 Esegui i test

```bash
python manage.py test ret
```

---

## 🔧 TROUBLESHOOTING

### Problema: ImportError con decouple

```bash
pip install python-decouple
```

### Problema: KeyError per SECRET_KEY

Verifica che il file `.env` esista e contenga `SECRET_KEY=...`

```bash
cat /home/django/apps_turi/.env | grep SECRET_KEY
```

### Problema: Directory logs non trovata

```bash
mkdir -p /home/django/apps_turi/logs
chmod 755 /home/django/apps_turi/logs
```

### Problema: Decoratori non funzionano

Verifica gli import:

```python
from ret.decorators import require_script, log_action
from django.contrib.auth.decorators import login_required
```

### Vedere i log in tempo reale

```bash
tail -f /home/django/apps_turi/logs/django.log
```

---

## ✅ CHECKLIST VERIFICA

Dopo l'installazione, verifica che:

- [ ] `python manage.py check` non dà errori
- [ ] Il server si avvia correttamente
- [ ] Il file .env esiste e contiene SECRET_KEY
- [ ] DEBUG=False in produzione
- [ ] La directory logs esiste
- [ ] Export script funziona
- [ ] I log vengono scritti in logs/django.log
- [ ] Non ci sono errori 500 nel browser

---

## 🚀 PROSSIMI PASSI

Dopo aver implementato Fase 1 e 2:

1. **Monitora i log** per 1-2 giorni
2. **Refactora altre view** complesse seguendo lo stesso pattern
3. **Aggiungi test** per le funzionalità critiche
4. **Implementa CI/CD** (GitHub Actions)
5. **Setup monitoring** (Sentry per errori)

---

## 📞 SUPPORTO

Se hai problemi:

1. Controlla i log: `tail -f logs/django.log`
2. Verifica settings: `python manage.py check`
3. Testa import: `python manage.py shell` poi `from ret.decorators import *`

---

## 📝 NOTE IMPORTANTI

- **NON committare il file .env** su Git
- **Fai backup** prima di ogni modifica
- **Testa in staging** prima di production (se possibile)
- **Monitora i log** dopo ogni deploy
- **Documenta** le modifiche che fai

---

## 🎓 ESEMPIO COMPLETO DI WORKFLOW

```bash
# 1. Backup
cd /home/django
tar -czf backup_$(date +%Y%m%d).tar.gz apps_turi/

# 2. Installa dipendenze
source django_env/bin/activate
pip install python-decouple

# 3. Crea .env
cd apps_turi
nano .env
# [Configura valori]

# 4. Aggiorna settings
cp apps_turi/settings.py apps_turi/settings.py.original
nano apps_turi/settings.py
# [Incolla nuovo contenuto]

# 5. Test
python manage.py check

# 6. Crea directory
mkdir -p logs ret/services

# 7. Copia file refactored
# [Copia constants.py, decorators.py, etc.]

# 8. Test finale
python manage.py runserver
# Apri browser e testa

# 9. Riavvia produzione
sudo systemctl restart gunicorn

# 10. Monitora
tail -f logs/django.log
```

---

**BUON LAVORO! 🚀**

Per domande o problemi, controlla sempre i log e fai test graduali.
