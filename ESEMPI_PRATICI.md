# 💡 ESEMPI PRATICI DI UTILIZZO

## 📖 Come Usare i File Refactored

---

## 1️⃣ MANAGERS - Query Semplificate

### PRIMA (codice ripetuto ovunque):

```python
# views.py - ogni volta che servono i dati utente
def view_ret(request):
    rets = RET.objects.filter(utente=request.user.id)
    # ...

def edit_ret(request):
    rets = RET.objects.filter(utente=request.user.id)
    # ...

def delete_ret(request):
    rets = RET.objects.filter(utente=request.user.id)
    # ...
```

### DOPO (manager riutilizzabile):

```python
# models.py
class RET(models.Model):
    # ... campi ...
    objects = RETManager()  # <-- Aggiungi questo

# views.py - molto più pulito!
def view_ret(request):
    rets = RET.objects.for_user(request.user)  # ✅ Leggibile!
    
def edit_ret(request):
    rets = RET.objects.for_user(request.user).ordered()  # ✅ + Ordinato!
    
def delete_ret(request):
    RET.objects.for_user(request.user).delete()  # ✅ Semplice!
```

### Altri esempi di manager:

```python
# Filtra per baseband
rets_bb01 = RET.objects.for_user(request.user).by_baseband('BB01')

# Filtra per porta
rets_port_a = RET.objects.for_user(request.user).by_port('A')

# Query ottimizzata con relazioni
rets = RET.objects.for_user(request.user).with_cells()

# Trova duplicati
duplicates = RET.objects.get_duplicates_by_serial()

# Rimuovi duplicati automaticamente
removed = RET.objects.remove_duplicates_by_serial()
print(f"Rimossi {removed} duplicati")
```

---

## 2️⃣ DECORATORS - Controlli Automatici

### PRIMA (controlli ripetuti in ogni view):

```python
def view_ret(request):
    # Ogni view deve controllare se utente ha dati
    if not RET.objects.filter(utente=request.user).exists():
        messages.warning(request, "Devi prima elaborare i dati RET")
        return redirect('edit_ret')
    
    # ... resto della logica ...

def export_script(request):
    # Stessi controlli ripetuti!
    if not ScriptRet.objects.filter(utente=request.user).exists():
        messages.warning(request, "Devi prima generare uno script")
        return redirect('generate_script')
    
    # ... resto della logica ...
```

### DOPO (decoratore fa il controllo):

```python
from ret.decorators import require_ret_data, require_script

@login_required
@require_ret_data()  # ✅ Controllo automatico!
def view_ret(request):
    # Qui sei sicuro che ci sono dati RET
    rets = RET.objects.for_user(request.user)
    # ...

@login_required
@require_script()  # ✅ Controllo automatico!
def export_script(request):
    # Qui sei sicuro che c'è uno script
    script = ScriptRet.objects.for_user(request.user).first()
    # ...
```

### Esempio con logging automatico:

```python
from ret.decorators import log_action

@login_required
@log_action("Delete RET Data")  # ✅ Log automatico
def delete_ret(request):
    RET.objects.for_user(request.user).delete()
    return redirect('home')

# Nel log vedrai:
# INFO: Delete RET Data - User: mario.rossi
# INFO: Delete RET Data completed - User: mario.rossi
```

### Esempio con gestione errori:

```python
from ret.decorators import handle_exceptions

@login_required
@handle_exceptions(
    error_message="Errore durante elaborazione",
    redirect_to='home'
)
def complex_operation(request):
    # Qualsiasi errore viene gestito automaticamente
    # L'utente vede il messaggio e viene reindirizzato
    result = do_complex_stuff()
    return render(request, 'result.html', {'result': result})
```

---

## 3️⃣ SERVICES - Logica Business Separata

### PRIMA (logica nelle views):

```python
def export_script1_ret(request):
    # 50 righe di logica...
    script = ScriptRet.objects.filter(utente=request.user.id)
    sito = script[0].sito
    bb1 = script[0].bb1
    script = script[0].script1
    nomefile = bb1 + "_ret.txt"
    
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="{nomefile}"'
    
    with open(nomefile, 'w') as f:
        f.write(script)
    with open(nomefile, 'r') as f:
        response.write(f.read())
    os.remove(nomefile)
    
    # Logging manuale
    elemento = ScriptRetLog(...)
    elemento.save()
    
    return response

def export_script2_ret(request):
    # Altre 50 righe IDENTICHE!
    # ...
```

### DOPO (service riutilizzabile):

```python
from ret.services.export_service import ExportService

def export_script_ret(request, script_number):
    # 4 righe invece di 100!
    response = ExportService.export_script(request.user, script_number)
    messages.success(request, f"Script {script_number} esportato")
    return response

# Il service gestisce tutto:
# - Validazione
# - Generazione file
# - Logging
# - Gestione errori
```

### Usare il service altrove:

```python
# In un'altra view
def bulk_export(request):
    """Esporta tutti gli script dell'utente"""
    try:
        script1 = ExportService.export_script(request.user, 1)
        script2 = ExportService.export_script(request.user, 2)
        
        # Crea ZIP con entrambi
        # ...
        
    except ValueError:
        messages.error(request, "Alcuni script non disponibili")

# In un comando management
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in User.objects.all():
            try:
                ExportService.export_script(user, 1)
                print(f"Exported for {user.username}")
            except:
                print(f"Skipped {user.username}")
```

---

## 4️⃣ CONSTANTS - Valori Centralizzati

### PRIMA (magic numbers ovunque):

```python
# views.py
cell = item.cella[4:6]  # ❌ Cosa significa 4 e 6?

# altro_file.py  
cell = nome[4:6]  # ❌ Stesso valore ripetuto

# models.py
max_length=5  # ❌ Perché 5?

# forms.py
rows=10  # ❌ Perché 10?
```

### DOPO (costanti autodocumentanti):

```python
# constants.py
class CellNaming:
    CELL_NAME_START = 4
    CELL_NAME_END = 6

class ValidationRules:
    BB_MAX_LENGTH = 5
    
class ScriptSettings:
    TEXTAREA_ROWS = 10

# Ora in tutto il codice:
from ret.constants import CellNaming, ValidationRules

# views.py
cell = item.cella[CellNaming.CELL_NAME_START:CellNaming.CELL_NAME_END]  # ✅ Chiaro!

# models.py
bb = models.CharField(max_length=ValidationRules.BB_MAX_LENGTH)  # ✅ Consistente!

# forms.py
widgets = {"script1": forms.Textarea(attrs={'rows': ScriptSettings.TEXTAREA_ROWS})}
```

### Cambiare un valore in un posto solo:

```python
# Se devi cambiare, modifichi SOLO constants.py
class CellNaming:
    CELL_NAME_START = 3  # Era 4, ora 3
    CELL_NAME_END = 7    # Era 6, ora 7

# Tutto il codice si aggiorna automaticamente! ✅
```

---

## 5️⃣ LOGGING - Debug Semplificato

### PRIMA (print statements):

```python
def edit_ret(request):
    print("Starting edit_ret")  # ❌ Va su console
    # ...
    print(f"Processed {count} items")  # ❌ Perso al restart
```

### DOPO (logging professionale):

```python
import logging
logger = logging.getLogger('ret')

def edit_ret(request):
    logger.info(f"Edit RET started by {request.user.username}")
    
    try:
        # logica...
        logger.debug(f"Processing {count} items")
        logger.info("Edit RET completed successfully")
    except Exception as e:
        logger.error(f"Error in edit_ret: {e}", exc_info=True)
        raise

# I log vanno in logs/django.log e sono permanenti!
```

### Vedere i log:

```bash
# Log in tempo reale
tail -f logs/django.log

# Ultimi 100 errori
grep ERROR logs/django.log | tail -100

# Log di un utente specifico
grep "mario.rossi" logs/django.log

# Log di oggi
grep "$(date +%Y-%m-%d)" logs/django.log
```

---

## 6️⃣ MODELS PROPERTIES - Logica Riutilizzabile

### PRIMA (logica ripetuta):

```python
# views.py
script = ScriptRet.objects.get(utente=request.user)
if script.bb2 and script.script2:  # ❌ Ripetuto ovunque
    # ha secondo script
    pass

# altro_file.py
if obj.bb2 and obj.script2:  # ❌ Stesso controllo
    pass
```

### DOPO (property nel model):

```python
# models.py
class ScriptRet(models.Model):
    # ... campi ...
    
    @property
    def has_second_script(self):
        """Verifica se esiste secondo script"""
        return bool(self.bb2 and self.script2)

# Ora ovunque:
script = ScriptRet.objects.get(utente=request.user)
if script.has_second_script:  # ✅ Leggibile e riutilizzabile!
    pass

# Nel template:
{% if script.has_second_script %}
    <a href="{% url 'export_script_ret' 2 %}">Esporta Script 2</a>
{% endif %}
```

---

## 7️⃣ ESEMPIO COMPLETO: Refactoring Step-by-Step

### View complessa da refactorare:

```python
# VECCHIO views.py
def process_data(request):
    # 150 righe di codice!
    objs = Model.objects.filter(utente=request.user.id)
    if not objs.exists():
        messages.warning(request, "No data")
        return redirect('home')
    
    for obj in objs:
        # Logica complessa...
        if obj.type == "A":
            # 30 righe
            pass
        elif obj.type == "B":
            # 30 righe
            pass
    
    # Genera output
    # 50 righe di codice...
    
    return render(request, 'template.html', context)
```

### PASSO 1: Estrai helper functions

```python
# NUOVO views.py
def process_data(request):
    objs = _get_user_data(request.user)
    if not objs:
        return _handle_no_data(request)
    
    results = _process_objects(objs)
    output = _generate_output(results)
    
    return render(request, 'template.html', {'output': output})

def _get_user_data(user):
    return Model.objects.for_user(user)  # Manager!

def _handle_no_data(request):
    messages.warning(request, "No data")
    return redirect('home')

def _process_objects(objs):
    return [_process_single_object(obj) for obj in objs]

def _process_single_object(obj):
    if obj.type == "A":
        return _process_type_a(obj)
    elif obj.type == "B":
        return _process_type_b(obj)

def _process_type_a(obj):
    # Logica tipo A
    pass

def _process_type_b(obj):
    # Logica tipo B
    pass

def _generate_output(results):
    # Generazione output
    pass
```

### PASSO 2: Aggiungi decoratori

```python
from ret.decorators import require_data, log_action, handle_exceptions

@login_required
@require_data()  # Controllo automatico
@log_action("Process Data")  # Logging automatico
@handle_exceptions(error_message="Errore elaborazione")  # Errori automatici
def process_data(request):
    objs = Model.objects.for_user(request.user)
    results = _process_objects(objs)
    output = _generate_output(results)
    return render(request, 'template.html', {'output': output})
```

### PASSO 3: Crea service

```python
# services/data_processor.py
class DataProcessor:
    def __init__(self, user):
        self.user = user
        self.data = None
        self.results = None
    
    def process(self):
        """Pipeline completa di elaborazione"""
        self.data = self._fetch_data()
        self.results = self._process_data()
        return self._generate_output()
    
    def _fetch_data(self):
        return Model.objects.for_user(self.user)
    
    def _process_data(self):
        return [self._process_item(item) for item in self.data]
    
    def _process_item(self, item):
        if item.type == "A":
            return self._process_type_a(item)
        elif item.type == "B":
            return self._process_type_b(item)
    
    def _generate_output(self):
        # Logica generazione
        pass

# views.py - ora è SEMPLICISSIMO!
from .services.data_processor import DataProcessor

@login_required
@require_data()
@log_action("Process Data")
def process_data(request):
    processor = DataProcessor(request.user)
    output = processor.process()
    return render(request, 'template.html', {'output': output})
```

### RISULTATO:

- ✅ Da 150 righe → a 5 righe nella view
- ✅ Logica testabile separatamente
- ✅ Riutilizzabile in altri contesti
- ✅ Facile da mantenere
- ✅ Autodocumentante

---

## 🎯 ESERCIZIO PRATICO

Prova a refactorare questa funzione:

```python
def my_complex_view(request):
    items = MyModel.objects.filter(user=request.user.id)
    if not items.exists():
        return redirect('home')
    
    result = []
    for item in items:
        if item.status == "active":
            result.append({
                'name': item.name,
                'value': item.value * 2
            })
    
    return render(request, 'page.html', {'data': result})
```

### SOLUZIONE:

```python
# 1. Aggiungi manager
class MyModel(models.Model):
    # ...
    objects = MyModelManager()

class MyModelManager(models.Manager):
    def for_user(self, user):
        return self.filter(user=user)
    
    def active_only(self):
        return self.filter(status="active")

# 2. Usa decoratore
from ret.decorators import require_data

@login_required
@require_data(model=MyModel)
def my_complex_view(request):
    items = MyModel.objects.for_user(request.user).active_only()
    data = [{'name': i.name, 'value': i.value * 2} for i in items]
    return render(request, 'page.html', {'data': data})

# 3. Ancora meglio - method nel model
class MyModel(models.Model):
    # ...
    def get_display_data(self):
        return {
            'name': self.name,
            'value': self.value * 2
        }

# View finale - SEMPLICISSIMA!
@login_required
@require_data(model=MyModel)
def my_complex_view(request):
    items = MyModel.objects.for_user(request.user).active_only()
    data = [item.get_display_data() for item in items]
    return render(request, 'page.html', {'data': data})
```

---

## 📚 RISORSE EXTRA

### Dove trovare aiuto:

1. **Django Documentation**: https://docs.djangoproject.com/
2. **Real Python**: https://realpython.com/tutorials/django/
3. **Two Scoops of Django**: Best practices book
4. **Django Best Practices**: https://django-best-practices.readthedocs.io/

### Pattern comuni:

- **Fat Models, Thin Views**: Logica nei models, views orchestrano
- **Service Layer**: Business logic separata
- **Manager Methods**: Query comuni riutilizzabili
- **DRY**: Don't Repeat Yourself

---

**Continua a refactorare! Ogni piccolo miglioramento conta. 🚀**
