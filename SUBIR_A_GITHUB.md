# 📤 GUÍA PASO A PASO: SUBIR A GITHUB

## 🎯 Objetivo
Subir el proyecto "DeepL Subtitle Translator" a tu cuenta de GitHub.

---

## 📋 REQUISITOS PREVIOS

### 1️⃣ Tener una cuenta de GitHub
- Si NO tienes: Ve a https://github.com/signup y créala
- Si ya tienes: Inicia sesión en https://github.com

### 2️⃣ Instalar Git en Windows
- Descarga: https://git-scm.com/download/win
- Ejecuta el instalador
- Deja todas las opciones por defecto
- Verifica instalación:
  ```bash
  # Abre CMD o PowerShell:
  git --version
  ```

---

## 🚀 OPCIÓN 1: SUBIR USANDO GITHUB DESKTOP (MÁS FÁCIL)

### Paso 1: Descargar GitHub Desktop
1. Ve a: https://desktop.github.com/
2. Descarga e instala
3. Inicia sesión con tu cuenta de GitHub

### Paso 2: Crear Repositorio
1. Abre GitHub Desktop
2. Click en **"File"** → **"New Repository"**
3. Rellena:
   - **Name:** `deepl-subtitle-translator`
   - **Description:** `Traductor de subtítulos con DeepL API y soporte MKV`
   - **Local Path:** Elige donde crear la carpeta
   - ✅ **Initialize with README:** (Desmarcado, ya tenemos README)
   - **Git Ignore:** None
   - **License:** MIT
4. Click en **"Create Repository"**

### Paso 3: Copiar tus archivos
1. Abre la carpeta del repositorio recién creado
2. Copia TODOS estos archivos a esa carpeta:
   ```
   ✅ subtitle_translator_gui_v2.py
   ✅ instalar.bat
   ✅ Ejecutar_Traductor.bat
   ✅ verificar_mkvtoolnix.bat
   ✅ agregar_mkv_path.bat
   ✅ README.md
   ✅ README_v2.md
   ✅ AGREGAR_PATH_MANUAL.md
   ✅ GUIA_AVANZADA.md
   ✅ requirements.txt
   ✅ LICENSE
   ✅ .gitignore
   ```

### Paso 4: Hacer Commit
1. Vuelve a GitHub Desktop
2. Verás todos los archivos en la lista de cambios
3. En la esquina inferior izquierda:
   - **Summary:** Escribe `Initial commit`
   - **Description:** `v2.0 - Soporte para MKV y traducción de subtítulos`
4. Click en **"Commit to main"**

### Paso 5: Publicar en GitHub
1. Click en **"Publish repository"**
2. Desmarca **"Keep this code private"** (si quieres que sea público)
3. Click en **"Publish Repository"**

### ✅ ¡LISTO!
Tu proyecto está en: `https://github.com/TU_USUARIO/deepl-subtitle-translator`

---

## 🚀 OPCIÓN 2: SUBIR USANDO LÍNEA DE COMANDOS (GIT)

### Paso 1: Configurar Git (solo la primera vez)
```bash
# Abre CMD o PowerShell y ejecuta:
git config --global user.name "Tu Nombre"
git config --global user.email "tu_email@ejemplo.com"
```

### Paso 2: Crear repositorio en GitHub.com
1. Ve a: https://github.com/new
2. Rellena:
   - **Repository name:** `deepl-subtitle-translator`
   - **Description:** `Traductor de subtítulos con DeepL API y soporte MKV`
   - **Public** o **Private**
   - ❌ NO marques "Add a README"
   - ❌ NO marques ".gitignore"
   - ❌ NO marques "license"
3. Click en **"Create repository"**
4. **NO CIERRES** esta página (la necesitarás)

### Paso 3: Preparar tu carpeta local
1. Abre CMD o PowerShell
2. Ve a la carpeta donde tienes todos los archivos:
   ```bash
   cd C:\ruta\donde\estan\tus\archivos
   ```
3. Verifica que estén todos los archivos:
   ```bash
   dir
   ```

### Paso 4: Inicializar Git
```bash
git init
```

### Paso 5: Agregar archivos
```bash
# Agregar todos los archivos
git add .

# Verificar qué se agregó
git status
```

### Paso 6: Hacer el primer commit
```bash
git commit -m "Initial commit - v2.0 con soporte MKV"
```

### Paso 7: Conectar con GitHub
```bash
# Reemplaza TU_USUARIO con tu usuario de GitHub
git remote add origin https://github.com/TU_USUARIO/deepl-subtitle-translator.git

# Configurar rama principal
git branch -M main
```

### Paso 8: Subir a GitHub
```bash
git push -u origin main
```

**Te pedirá autenticación:**
- **Usuario:** Tu usuario de GitHub
- **Contraseña:** Token de acceso personal (NO tu contraseña)

#### ¿Cómo crear un Token?
1. Ve a: https://github.com/settings/tokens
2. Click en **"Generate new token (classic)"**
3. Marca **"repo"**
4. Click en **"Generate token"**
5. **COPIA EL TOKEN** (no podrás verlo después)
6. Úsalo como contraseña cuando Git te lo pida

### ✅ ¡LISTO!
Tu proyecto está en: `https://github.com/TU_USUARIO/deepl-subtitle-translator`

---

## 🔄 ACTUALIZAR EL REPOSITORIO (Después de hacer cambios)

### Usando GitHub Desktop:
1. Abre GitHub Desktop
2. Verás los cambios automáticamente
3. Escribe mensaje de commit
4. Click en **"Commit to main"**
5. Click en **"Push origin"**

### Usando línea de comandos:
```bash
# 1. Ver qué cambió
git status

# 2. Agregar cambios
git add .

# 3. Hacer commit
git commit -m "Descripción de los cambios"

# 4. Subir a GitHub
git push
```

---

## 📝 BUENAS PRÁCTICAS

### ✅ Mensajes de Commit Claros
```bash
❌ git commit -m "cambios"
✅ git commit -m "Agregado selector de subtítulos múltiples"
✅ git commit -m "Corregido bug en extracción de MKV"
✅ git commit -m "Actualizada documentación README"
```

### ✅ Archivo .gitignore
Ya incluido, evita subir:
- `translator_config.json` (contiene tu API key)
- Archivos temporales
- Archivos de cache

### ✅ README.md Completo
Ya incluido con:
- Descripción del proyecto
- Instalación
- Uso
- Screenshots (agrega capturas si quieres)

---

## 🎨 PERSONALIZAR TU REPOSITORIO

### 1. Agregar Screenshot
1. Toma captura de pantalla de la app
2. Guárdala como `screenshot.png`
3. Súbela a GitHub
4. Edita README.md, reemplaza:
   ```markdown
   ![Screenshot](https://via.placeholder.com/800x500.png?text=Screenshot+Placeholder)
   ```
   Por:
   ```markdown
   ![Screenshot](screenshot.png)
   ```

### 2. Agregar Topics (Etiquetas)
1. Ve a tu repositorio en GitHub
2. Click en ⚙️ junto a "About"
3. Agrega topics:
   ```
   python, deepl, subtitles, translation, mkv, gui, customtkinter
   ```

### 3. Editar Información
En el README.md, reemplaza:
- `TU_USUARIO` → Tu usuario de GitHub
- `tu_email@ejemplo.com` → Tu email
- `[Tu Nombre]` → Tu nombre en LICENSE

---

## ❓ SOLUCIÓN DE PROBLEMAS

### ❌ "git: command not found"
**Solución:** Instala Git desde https://git-scm.com/download/win

### ❌ "Permission denied"
**Solución:** Usa Token de acceso personal en vez de contraseña

### ❌ "remote: Repository not found"
**Solución:** Verifica que el nombre de usuario y repositorio sean correctos

### ❌ Archivos grandes (>100MB)
**Solución:** 
- No subas archivos .mkv de prueba
- El .gitignore ya excluye archivos grandes
- Si necesitas subir archivos grandes, usa Git LFS

---

## 📚 RECURSOS ADICIONALES

- **GitHub Docs:** https://docs.github.com/
- **Git Tutorial:** https://git-scm.com/book/es/v2
- **GitHub Desktop:** https://docs.github.com/en/desktop

---

## ✅ CHECKLIST FINAL

Antes de publicar, verifica:

- [ ] Todos los archivos están en la carpeta
- [ ] No has subido `translator_config.json` (tu API key)
- [ ] README.md está completo
- [ ] LICENSE tiene tu nombre
- [ ] El proyecto funciona después de clonar
- [ ] Has agregado una descripción al repositorio
- [ ] (Opcional) Has agregado un screenshot

---

## 🎉 ¡FELICIDADES!

Tu proyecto está público en GitHub y otros pueden:
- ⭐ Darle estrella
- 🍴 Hacer fork
- 🐛 Reportar bugs
- 🤝 Contribuir con mejoras

**URL de tu proyecto:**
```
https://github.com/TU_USUARIO/deepl-subtitle-translator
```

¡Compártelo con la comunidad! 🚀
