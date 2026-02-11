# 🎬 DeepL Subtitle Translator v2.0

Traductor de subtítulos con interfaz moderna que **procesa archivos MKV completos** además de subtítulos individuales.

## 🆕 NOVEDADES v2.0

### 🎥 Modo MKV (¡NUEVO!)
- ✅ **Extrae subtítulos** automáticamente de archivos MKV
- ✅ **Traduce al español latino** usando DeepL
- ✅ **Reinserta SOLO el subtítulo traducido** al MKV
- ✅ **Remueve todos los demás subtítulos** del archivo
- ✅ **Selector interactivo** cuando hay múltiples subtítulos
- ✅ **Reemplaza el archivo original** automáticamente

### Resultado Final
**Antes:** `pelicula.mkv` con 5 subtítulos (inglés, inglés SDH, francés, alemán, japonés)  
**Después:** `pelicula.mkv` con 1 subtítulo (Español (Latinoamérica))

## ✨ Características Completas

### 📄 Modo Subtítulos (Original)
- Traduce archivos .srt y .ass individuales
- Procesamiento por lotes
- Preserva formato y timing

### 🎥 Modo MKV (Nuevo)
- Procesamiento integral de archivos de video
- Detección automática de subtítulos
- Selector visual cuando hay múltiples opciones
- Limpieza completa de subtítulos antiguos

### 🎨 Interfaz
- Tema automático claro/oscuro según Windows
- Drag & Drop
- Dos modos de trabajo seleccionables
- Progreso detallado en tiempo real

## 📦 Instalación

### Requisitos Previos

1. **Python 3.12** ✓
2. **API Key de DeepL** (gratis: 500K caracteres/mes)
3. **MKVToolNix** (solo para modo MKV)

### Instalación Paso a Paso

#### 1️⃣ Instalar Dependencias de Python

```powershell
# Doble clic en:
instalar.bat
```

Esto instalará:
- customtkinter
- deepl
- tkinterdnd2

#### 2️⃣ Instalar MKVToolNix (para modo MKV)

**Opción A - Verificador automático:**
```powershell
# Doble clic en:
verificar_mkvtoolnix.bat
```

**Opción B - Manual:**
1. Descarga desde: https://mkvtoolnix.download/downloads.html
2. Ejecuta el instalador
3. **IMPORTANTE:** Durante instalación marca:
   ```
   [X] Add mkvtoolnix to PATH
   ```
4. Completa la instalación

#### 3️⃣ Ejecutar la Aplicación

```powershell
# Doble clic en:
Ejecutar_Traductor.bat
```

## 🚀 Guía de Uso

### 🎯 Modo 1: Traducir Subtítulos Individuales

Para traducir archivos .srt o .ass:

1. **Selecciona modo:** 📄 Traducir Subtítulos (SRT/ASS)
2. **Configura API key** y idiomas (De: EN → A: ES)
3. **Arrastra archivos** .srt/.ass a la lista
4. **Clic en** "🚀 TRADUCIR ARCHIVOS"
5. Los archivos traducidos se guardan como `Original_ES.srt`

**Resultado:**
```
📁 Carpeta/
  ├── Serie.S01E01.srt         (original inglés)
  └── Serie.S01E01_ES.srt      (nuevo español)
```

### 🎥 Modo 2: Procesar Archivos MKV

Para extraer, traducir y reinsertar subtítulos en MKV:

1. **Selecciona modo:** 🎥 Procesar Archivos MKV
2. **Configura API key** y idiomas (De: EN → A: ES)
3. **Arrastra archivos** .mkv a la lista
4. **Clic en** "🎥 PROCESAR ARCHIVOS MKV"
5. **Selecciona el subtítulo** a traducir (aparecerá un diálogo)
6. Espera a que termine el proceso

**Proceso automático:**
```
1. Analiza el MKV
2. Muestra lista de subtítulos disponibles
3. Extrae el subtítulo seleccionado
4. Lo traduce a español latino
5. Remueve TODOS los subtítulos del MKV
6. Inserta SOLO el subtítulo en español
7. Reemplaza el archivo original
```

**Resultado:**
```
Antes: pelicula.mkv
  └── Subtítulos: [Inglés, Inglés SDH, Francés, Japonés]

Después: pelicula.mkv
  └── Subtítulos: [Español (Latinoamérica)]
```

### 📋 Selector de Subtítulos

Cuando el MKV tiene múltiples subtítulos, verás una ventana como esta:

```
┌─────────────────────────────────────────────────┐
│  Selecciona el subtítulo a traducir:           │
├─────────────────────────────────────────────────┤
│  Track 2: EN - SRT - English                   │
│  Track 3: EN - SRT - English [FORCED]          │
│  Track 4: EN - SRT - English (SDH) [DEFAULT]   │
│  Track 5: JA - ASS - Japanese                  │
└─────────────────────────────────────────────────┘
     [Seleccionar]  [Cancelar]
```

**Recomendaciones:**
- Evita subtítulos marcados como **[FORCED]** (solo diálogos forzados)
- Prefiere subtítulos **[DEFAULT]** o sin etiquetas especiales
- Si dice **SDH**, incluye descripciones de audio (puedes usarlo)

## ⚙️ Configuración

### Idiomas Disponibles

**De (Origen):**
- EN (Inglés)
- JA (Japonés) - Para anime
- KO (Coreano) - Para K-dramas
- ES, FR, DE, IT, PT, RU, ZH

**A (Destino):**
- **ES** - Español latino/neutral (recomendado)
- EN-US, EN-GB
- PT-BR (Portugués brasileño)
- FR, DE, IT, JA

### Sufijo de Archivos

Solo aplica en **modo Subtítulos**:
- `_ES` → `pelicula_ES.srt`
- `.spa` → `pelicula.spa.srt`
- `.es` → `pelicula.es.srt`

En **modo MKV** no se usa sufijo (se reemplaza el archivo original).

## 🎯 Casos de Uso

### Caso 1: Serie de TV completa
```
1. Selecciona modo: 📄 Traducir Subtítulos
2. Arrastra carpeta de temporada con 10 episodios .srt
3. Traduce todos a la vez
4. Resultado: 10 archivos _ES.srt nuevos
```

### Caso 2: Película MKV con múltiples subtítulos
```
1. Selecciona modo: 🎥 Procesar Archivos MKV
2. Arrastra pelicula.mkv
3. En el selector, elige "Track 2: EN - SRT - English"
4. Espera 3-5 minutos
5. Resultado: pelicula.mkv ahora solo tiene español
```

### Caso 3: Colección de anime
```
1. Selecciona modo: 🎥 Procesar Archivos MKV
2. Configura: De: JA → A: ES
3. Arrastra carpeta con 12 episodios .mkv
4. Para cada uno, selecciona el subtítulo japonés
5. Resultado: 12 MKV con subtítulos en español
```

## ⚠️ Advertencias Importantes - Modo MKV

### ⚡ El Archivo Original SE REEMPLAZA

El modo MKV **sobrescribe el archivo original**. Si quieres conservar el original:

**Opción 1 - Copia manual antes:**
```
Antes de procesar:
1. Copia pelicula.mkv a pelicula.BACKUP.mkv
2. Procesa pelicula.mkv
3. Si algo sale mal, renombra el backup
```

**Opción 2 - Procesa en carpeta temporal:**
```
1. Copia archivos MKV a carpeta "Por Procesar"
2. Procesa esa carpeta
3. Los originales quedan intactos en otra ubicación
```

### 🕒 Tiempos de Procesamiento

**Modo Subtítulos:**
- Archivo SRT/ASS: 20-30 segundos

**Modo MKV:**
- Película (90 min): 3-5 minutos
- Serie (45 min): 2-3 minutos
- Anime (24 min): 1-2 minutos

*El tiempo depende del tamaño del MKV y cantidad de diálogos*

### 💾 Espacio en Disco

Durante el procesamiento MKV se crean archivos temporales:
- Subtítulo extraído: ~1-5 MB
- Subtítulo traducido: ~1-5 MB
- MKV temporal: Mismo tamaño que el original

**Espacio necesario:** ~2x el tamaño del MKV más grande

Los archivos temporales se eliminan automáticamente al terminar.

## 🔧 Solución de Problemas

### ❌ "MKVToolNix no detectado"

**Problema:** La función MKV no está disponible

**Solución:**
1. Ejecuta `verificar_mkvtoolnix.bat`
2. Si no está instalado, descárgalo
3. Durante instalación marca "Add to PATH"
4. Reinicia la aplicación

### ❌ "El MKV no contiene subtítulos"

**Problema:** El archivo MKV no tiene subtítulos incrustados

**Solución:**
- Usa modo Subtítulos con archivos .srt/.ass externos
- Descarga subtítulos y tradúcelos por separado
- Luego usa MKVToolNix GUI para insertarlos manualmente

### ❌ "Error al remuxear"

**Problema:** Error al reinsertar subtítulo en MKV

**Solución:**
1. Verifica que tienes espacio en disco
2. Cierra reproductores de video que usen el archivo
3. Verifica permisos de escritura en la carpeta
4. Si el MKV está en red, cópialo localmente primero

### ❌ Subtítulos desincronizados después de procesar

**Problema:** El timing no coincide con el video

**Solución:**
- Esto es raro, pero puede pasar si el subtítulo original ya estaba mal
- Prueba con un subtítulo diferente del MKV
- Verifica que elegiste el subtítulo correcto (no FORCED)

### ❌ "No se seleccionó ningún subtítulo"

**Problema:** Cerraste el selector sin elegir

**Solución:**
- El archivo se salta automáticamente
- Vuelve a procesarlo y selecciona un subtítulo

## 📊 Comparación de Modos

| Característica | Modo Subtítulos | Modo MKV |
|----------------|-----------------|----------|
| **Input** | .srt, .ass | .mkv |
| **Output** | Archivo nuevo | Reemplaza original |
| **Velocidad** | Rápido (30 seg) | Lento (3-5 min) |
| **Preserva video** | N/A | Sí (sin recodificar) |
| **Subs múltiples** | No aplica | Remueve todos menos español |
| **Reversible** | Sí (archivo original intacto) | No (sobrescribe) |
| **Requiere MKVToolNix** | No | Sí |

## 💡 Mejores Prácticas

### ✅ Para Subtítulos Individuales
1. Usa modo Subtítulos para máxima velocidad
2. Procesa temporadas completas a la vez
3. Los archivos originales siempre quedan intactos

### ✅ Para Archivos MKV
1. **Haz backup** si el archivo es irreemplazable
2. Prueba con 1 archivo antes de procesar lotes
3. Elige subtítulos sin etiquetas FORCED/SDH cuando sea posible
4. Ten paciencia, el proceso es lento pero seguro

### ✅ Organización
```
📁 Mis Videos/
├── 📁 Originales/          (siempre conserva una copia)
├── 📁 Por Procesar/        (trabaja aquí)
└── 📁 Procesados/          (mueve aquí al terminar)
```

## 📈 Uso de Caracteres DeepL

**Un episodio típico:**
- Serie 45 min: ~30,000 caracteres
- Anime 24 min: ~15,000 caracteres
- Película 90 min: ~60,000 caracteres

**Con 500,000 caracteres/mes:**
- ~16 episodios de serie
- ~30 episodios de anime
- ~8 películas

*Es el mismo consumo en ambos modos (subtítulos o MKV)*

## 🎉 Ventajas de v2.0

### Antes (v1.0)
```
1. Descargar archivo MKV
2. Extraer subtítulo manualmente con MKVToolNix GUI
3. Traducir el .srt con la app
4. Abrir MKVToolNix GUI
5. Remover subtítulos viejos
6. Agregar subtítulo nuevo
7. Remuxear (5-10 minutos)
= Total: 20-30 minutos de trabajo manual
```

### Ahora (v2.0)
```
1. Arrastra MKV a la app
2. Selecciona subtítulo
3. Espera 3-5 minutos
= Total: 3-5 minutos automático
```

**¡Ahorro de tiempo: ~85%!** 🚀

## 📁 Archivos Incluidos

1. **subtitle_translator_gui_v2.py** - Aplicación principal v2.0
2. **instalar.bat** - Instalador de dependencias Python
3. **verificar_mkvtoolnix.bat** - Verificador de MKVToolNix
4. **Ejecutar_Traductor.bat** - Ejecuta la app fácilmente
5. **README_v2.md** - Este manual
6. **GUIA_AVANZADA.md** - Tips y configuración avanzada

## 🔄 Actualizar desde v1.0

Si ya tienes v1.0 instalada:

1. **No necesitas reinstalar** dependencias Python
2. **Instala MKVToolNix** para usar modo MKV
3. **Tu API key y configuración** se mantienen
4. **Ambas versiones** pueden coexistir

## 🆘 Soporte y Ayuda

1. Revisa esta guía completa
2. Consulta GUIA_AVANZADA.md
3. Ejecuta `verificar_mkvtoolnix.bat` si hay problemas con MKV
4. Prueba con 1 archivo antes de procesar lotes grandes

---

**Versión:** 2.0  
**Requiere:** Python 3.12+, MKVToolNix (opcional)  
**Licencia:** Uso personal  
**Última actualización:** Febrero 2026
