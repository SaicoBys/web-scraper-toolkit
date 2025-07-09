# 📋 Tutorial: Gestión Masiva de Sitios Web

## 🎯 **Cómo Agregar Múltiples Sitios de Forma Profesional**

### **Método 1: Archivo CSV (Recomendado)**

#### **Paso 1: Editar el archivo CSV**
Abrir `config/target_sites.csv` y agregar sitios:

```csv
site_url,category,priority,enabled
indeed.com,job_board,high,true
linkedin.com/jobs,job_board,high,true
glassdoor.com,job_board,medium,true
monster.com,job_board,medium,false
dice.com,job_board,low,true
upwork.com,freelance,high,true
freelancer.com,freelance,medium,true
fiverr.com,freelance,low,false
google.com/careers,company,high,true
microsoft.com/careers,company,high,true
```

#### **Columnas Explicadas:**
- **site_url**: URL del sitio web
- **category**: Categoría (job_board, company, freelance, etc.)
- **priority**: Prioridad (high, medium, low)
- **enabled**: Activado (true/false)

#### **Paso 2: Configurar filtros**
Editar `config/job_scraper_config.json`:

```json
{
  "target_sites_csv": "config/target_sites.csv",
  "target_categories": ["job_board", "company"],
  "min_priority": "medium",
  "rate_limit": 2,
  "max_results": 100
}
```

#### **Paso 3: Ejecutar**
```bash
python3 src/job_scraper.py --keywords "python developer" --max-results 50
```

---

### **Método 2: Código Python para Agregar Masivamente**

```python
from src.site_manager import SiteManager

# Inicializar manager
manager = SiteManager()

# Agregar múltiples sitios
new_sites = [
    {"site_url": "stackoverflow.com/jobs", "category": "job_board", "priority": "high", "enabled": True},
    {"site_url": "github.com/jobs", "category": "tech", "priority": "high", "enabled": True},
    {"site_url": "angel.co/jobs", "category": "startup", "priority": "medium", "enabled": True}
]

manager.add_sites_bulk(new_sites)
```

---

### **Método 3: Gestión por Categorías**

#### **Activar solo sitios de una categoría:**
```python
# Obtener sitios por categoría
company_sites = manager.get_sites_by_category('company')
job_board_sites = manager.get_sites_by_category('job_board')

# Habilitar/deshabilitar sitios
manager.enable_disable_sites(company_sites, True)
manager.enable_disable_sites(job_board_sites, False)
```

#### **Configurar por prioridad:**
```json
{
  "target_sites_csv": "config/target_sites.csv",
  "min_priority": "high",
  "target_categories": ["job_board"]
}
```

---

## 🚀 **Casos de Uso Comunes**

### **Caso 1: Cliente con 50+ sitios**
1. Crear CSV con todos los sitios
2. Categorizar por industria
3. Establecer prioridades
4. Filtrar por categoría activa

### **Caso 2: Testing gradual**
1. Empezar con prioridad "high"
2. Probar resultados
3. Ir bajando a "medium" y "low"
4. Ajustar rate_limit según necesidad

### **Caso 3: Campaña específica**
1. Crear categoría personalizada
2. Agregar sitios relevantes
3. Configurar filtros específicos
4. Ejecutar campaña dirigida

---

## 📊 **Comandos Útiles**

### **Ver estadísticas:**
```bash
python3 src/site_manager.py
```

### **Scraping con filtros:**
```bash
python3 src/job_scraper.py --keywords "python developer" --max-results 100
```

### **Verificar sitios activos:**
```python
manager = SiteManager()
print(f"Sitios activos: {len(manager.active_sites)}")
manager.print_site_stats()
```

---

## ⚠️ **Mejores Prácticas**

1. **Empezar pequeño**: Probar con 5-10 sitios primero
2. **Rate limiting**: Usar 2-3 segundos para evitar bloqueos
3. **Categorizar**: Organizar sitios por industria/tipo
4. **Monitorear**: Verificar resultados antes de escalar
5. **Backup**: Guardar CSV antes de cambios importantes

---

## 🛠️ **Solución de Problemas**

### **Si no encuentra sitios:**
- Verificar que `enabled = true`
- Revisar filtros de categoría
- Comprobar nivel de prioridad mínimo

### **Si scraping es lento:**
- Aumentar `rate_limit`
- Reducir `max_results`
- Filtrar por prioridad más alta

### **Si hay errores:**
- Verificar formato CSV
- Comprobar URLs válidas
- Revisar configuración JSON

---

## 📈 **Escalabilidad**

- **Sitios soportados**: Ilimitados
- **Categorías**: Personalizables
- **Filtros**: Múltiples niveles
- **Formatos**: CSV, JSON, Excel
- **Automatización**: Scripts programables

**🎯 Resultado:** Sistema profesional y escalable para gestionar cientos de sitios web de forma eficiente.