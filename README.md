# 🎬 DeepL Subtitle Translator

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%2F11-lightgrey.svg)](https://www.microsoft.com/windows)

Aplicación de escritorio con interfaz gráfica para traducir subtítulos usando la API de DeepL. Soporta archivos individuales (.srt/.ass) y procesamiento completo de archivos MKV.

![Screenshot](https://via.placeholder.com/800x500.png?text=Screenshot+Placeholder)

## ✨ Características

### 📄 Modo Traducción de Subtítulos
- ✅ Traduce archivos **SRT** y **ASS**
- ✅ Procesamiento **por lotes** (múltiples archivos)
- ✅ Preserva **formato, timing y estilos**
- ✅ **Drag & Drop** de archivos
- ✅ Interfaz moderna con **tema claro/oscuro** automático

### 🎥 Modo Procesamiento MKV
- ✅ **Extrae** subtítulos automáticamente de archivos MKV
- ✅ **Selector interactivo** cuando hay múltiples subtítulos
- ✅ **Traduce** usando DeepL API
- ✅ **Remueve** todos los subtítulos antiguos
- ✅ **Inserta** solo el subtítulo en español latino
- ✅ Proceso **completamente automático**

### 🎨 Interfaz
- 🌓 Tema automático según Windows 10/11
- 📊 Progreso en tiempo real
- 💾 Guarda configuración y API key
- 🌍 Múltiples idiomas soportados

## 📋 Requisitos

### Software Necesario

1. **Python 3.12+**
   - Descarga: https://www.python.org/downloads/

2. **DeepL API Key** (Gratis)
   - Plan Free: 500,000 caracteres/mes
   - Registro: https://www.deepl.com/pro-api

3. **MKVToolNix** (Solo para modo MKV)
   - Descarga: https://mkvtoolnix.download/downloads.html
   - ⚠️ Durante instalación marcar: **"Add to PATH"**

### Dependencias Python

```bash
pip install customtkinter deepl tkinterdnd2
```

## 🚀 Instalación

### Windows - Instalación Rápida

1. **Clona este repositorio:**
   ```bash
   git clone https://github.com/TU_USUARIO/deepl-subtitle-translator.git
   cd deepl-subtitle-translator
   ```

2. **Instala dependencias Python:**
   ```bash
   # Doble clic en:
   instalar.bat
   
   # O manualmente:
   pip install -r requirements.txt
   ```

3. **Instala MKVToolNix** (opcional, solo para modo MKV):
   - Descarga e instala desde: https://mkvtoolnix.download/downloads.html
   - ⚠️ **Importante:** Marca "Add to PATH" durante instalación
   - Verifica con: `verificar_mkvtoolnix.bat`

4. **Ejecuta la aplicación:**
   ```bash
   # Doble clic en:
   Ejecutar_Traductor.bat
   
   # O manualmente:
   python subtitle_translator_gui_v2.py
   ```

## 📖 Uso

### Primera Vez

1. **Obtén tu API Key de DeepL:**
   - Ve a: https://www.deepl.com/pro-api
   - Regístrate para el plan Free
   - Copia tu API key

2. **Configura la aplicación:**
   - Pega tu API key en el campo superior
   - Haz clic en "Verificar"
   - La configuración se guardará automáticamente

### Modo 1: Traducir Subtítulos

```
1. Selecciona: 📄 Traducir Subtítulos (SRT/ASS)
2. Configura idiomas (De: EN → A: ES)
3. Arrastra archivos .srt o .ass
4. Clic en "🚀 TRADUCIR ARCHIVOS"
5. ¡Listo!
```

**Resultado:**
```
Serie.S01E01.srt         → Original
Serie.S01E01_ES.srt      → Traducido
```

### Modo 2: Procesar Archivos MKV

```
1. Selecciona: 🎥 Procesar Archivos MKV
2. Configura idiomas (De: EN → A: ES)
3. Arrastra archivos .mkv
4. Clic en "🎥 PROCESAR ARCHIVOS MKV"
5. Selecciona el subtítulo a traducir
6. Espera 3-5 minutos
7. ¡El MKV ahora solo tiene subtítulo en español!
```

**Proceso automático:**
```
MKV con múltiples subs → Extrae → Traduce → Limpia → Inserta solo español
```

## 🎯 Casos de Uso

### Serie de TV completa
```python
# Arrastra carpeta de temporada con 10 episodios
# Resultado: 10 archivos traducidos en minutos
```

### Película MKV
```python
# Arrastra pelicula.mkv (con subs en inglés, francés, japonés)
# Selecciona el subtítulo en inglés
# Resultado: pelicula.mkv solo con español latino
```

### Anime
```python
# Configura: De: JA (Japonés) → A: ES (Español)
# Arrastra episodios .mkv
# Resultado: Anime con subtítulos en español
```

## 📁 Estructura del Proyecto

```
deepl-subtitle-translator/
├── subtitle_translator_gui_v2.py    # Aplicación principal
├── instalar.bat                     # Instalador de dependencias
├── Ejecutar_Traductor.bat          # Ejecutor de la app
├── verificar_mkvtoolnix.bat        # Verificador de MKVToolNix
├── agregar_mkv_path.bat            # Agrega MKVToolNix al PATH
├── requirements.txt                 # Dependencias Python
├── .gitignore                       # Archivos ignorados por Git
├── README.md                        # Este archivo
├── README_v2.md                     # Manual completo
├── AGREGAR_PATH_MANUAL.md          # Guía para agregar al PATH
└── GUIA_AVANZADA.md                # Configuración avanzada
```

## ⚙️ Configuración

### Idiomas Soportados

**Origen:** EN, ES, JA, KO, ZH, FR, DE, IT, PT, RU  
**Destino:** ES (Latino), EN-US, EN-GB, PT-BR, FR, DE, IT, JA

### Personalización

```python
# Cambia el sufijo de archivos traducidos
Sufijo: _ES  → Serie.S01E01_ES.srt
Sufijo: .spa → Serie.S01E01.spa.srt
Sufijo: .es  → Serie.S01E01.es.srt
```

## 🔧 Solución de Problemas

### ❌ "MKVToolNix no detectado"

**Solución:**
```bash
# Ejecuta como administrador:
agregar_mkv_path.bat
```

O sigue la guía manual: `AGREGAR_PATH_MANUAL.md`

### ❌ "Error: Authentication failed"

**Solución:**
- Verifica que tu API key sea de **DeepL** (no DeepSeek)
- Haz clic en "Verificar" después de pegar la key

### ❌ "Module not found"

**Solución:**
```bash
pip install customtkinter deepl tkinterdnd2
```

Ver más soluciones en: `README_v2.md`

## 📊 Uso de API DeepL

### Plan Free (500,000 caracteres/mes)

| Tipo | Duración | Caracteres | Cantidad/mes |
|------|----------|------------|--------------|
| Serie TV | 45 min | ~30,000 | ~16 episodios |
| Anime | 24 min | ~15,000 | ~30 episodios |
| Película | 90 min | ~60,000 | ~8 películas |

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## ⚠️ Advertencia

- El modo MKV **reemplaza el archivo original**
- Haz backups antes de procesar archivos importantes
- Respeta los derechos de autor al traducir contenido

## 🙏 Agradecimientos

- [DeepL](https://www.deepl.com/) - API de traducción
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Framework de UI
- [MKVToolNix](https://mkvtoolnix.download/) - Herramientas MKV

## 📧 Contacto

- GitHub: [@YersonGD](https://github.com/YersonGD)
- Email: yerdiaz784@gmail.com

## 🗺️ Roadmap

- [ ] Soporte para múltiples idiomas de destino simultáneos
- [ ] Previsualización de subtítulos antes de traducir
- [ ] Caché de traducciones para ahorrar caracteres
- [ ] Soporte para archivos MP4
- [ ] Interfaz en múltiples idiomas
- [ ] Modo batch con cola de procesamiento

---

⭐ Si este proyecto te fue útil, dale una estrella en GitHub!
