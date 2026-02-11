#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepL Subtitle Translator - Interfaz Gráfica Completa
Versión 2.0 con soporte para archivos MKV
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import deepl
import re
import os
import subprocess
import threading
from pathlib import Path
from tkinterdnd2 import DND_FILES, TkinterDnD
import json
from datetime import datetime
import shutil

# Configuración de tema
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


class MKVProcessor:
    """Procesador de archivos MKV usando mkvtoolnix"""
    
    @staticmethod
    def check_mkvtoolnix():
        """Verifica si mkvtoolnix está instalado"""
        try:
            result = subprocess.run(
                ['mkvmerge', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    @staticmethod
    def get_mkv_info(mkv_file):
        """Obtiene información de pistas del MKV"""
        try:
            result = subprocess.run(
                ['mkvmerge', '-J', mkv_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                return None
            
            import json
            return json.loads(result.stdout)
        except Exception as e:
            print(f"Error obteniendo info MKV: {e}")
            return None
    
    @staticmethod
    def extract_subtitle(mkv_file, track_id, output_file):
        """Extrae un subtítulo específico del MKV"""
        try:
            result = subprocess.run(
                ['mkvextract', mkv_file, 'tracks', f'{track_id}:{output_file}'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return result.returncode == 0
        except Exception as e:
            print(f"Error extrayendo subtítulo: {e}")
            return False
    
    @staticmethod
    def remux_mkv(mkv_file, subtitle_file, output_file, subtitle_name="Español (Latinoamérica)"):
        """Remueve todos los subs y añade solo el nuevo subtítulo en español"""
        try:
            # Construir comando mkvmerge
            # -o output --no-subtitles input.mkv --language 0:spa --track-name "0:Español (Latinoamérica)" subtitle.srt
            
            cmd = [
                'mkvmerge',
                '-o', output_file,
                '--no-subtitles',  # Remover todos los subtítulos existentes
                mkv_file,
                '--language', '0:spa',  # Marcar como español
                '--track-name', f'0:{subtitle_name}',  # Nombre del track
                '--default-track', '0:yes',  # Marcar como predeterminado
                subtitle_file
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos max
            )
            
            return result.returncode == 0, result.stderr
        
        except Exception as e:
            return False, str(e)


class SubtitleTranslator:
    """Motor de traducción"""
    
    def __init__(self, api_key):
        self.translator = deepl.Translator(api_key)
        self.usage = None
        
    def get_usage(self):
        """Obtiene el uso actual de la API"""
        try:
            self.usage = self.translator.get_usage()
            if self.usage.character.limit_reached:
                return None, "Límite alcanzado"
            
            used = self.usage.character.count
            limit = self.usage.character.limit
            remaining = limit - used
            
            return {
                'used': used,
                'limit': limit,
                'remaining': remaining,
                'percent': (used / limit) * 100 if limit > 0 else 0
            }, None
        except Exception as e:
            return None, str(e)
    
    def translate_text(self, text, source_lang="EN", target_lang="ES"):
        if not text.strip():
            return text
        
        try:
            result = self.translator.translate_text(
                text, 
                source_lang=source_lang,
                target_lang=target_lang,
                formality="default"
            )
            return result.text
        except Exception as e:
            raise Exception(f"Error traduciendo: {e}")
    
    def parse_ass_line(self, line):
        if not line.startswith("Dialogue:"):
            return None, None
        
        parts = line.split(",", 9)
        if len(parts) < 10:
            return None, None
        
        prefix = ",".join(parts[:9])
        text = parts[9].strip()
        
        return prefix, text
    
    def clean_ass_text(self, text):
        tags = re.findall(r'\{[^}]+\}', text)
        clean = re.sub(r'\{[^}]+\}', '<<<TAG>>>', text)
        clean = clean.replace('\\N', ' <<<NEWLINE>>> ')
        clean = clean.replace('\\n', ' <<<NEWLINE>>> ')
        return clean, tags
    
    def restore_ass_tags(self, translated, original_tags):
        tag_index = 0
        result = translated
        while '<<<TAG>>>' in result and tag_index < len(original_tags):
            result = result.replace('<<<TAG>>>', original_tags[tag_index], 1)
            tag_index += 1
        
        result = result.replace('<<<NEWLINE>>>', '\\N')
        result = result.replace(' \\N ', '\\N')
        return result.strip()
    
    def translate_ass(self, input_file, output_file, source_lang="EN", target_lang="ES", 
                     progress_callback=None):
        with open(input_file, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
        
        translated_lines = []
        dialogue_count = 0
        
        for i, line in enumerate(lines):
            if progress_callback:
                progress_callback(i, len(lines), f"Línea {i}/{len(lines)}")
            
            prefix, text = self.parse_ass_line(line)
            
            if prefix is None:
                translated_lines.append(line)
                continue
            
            clean_text, tags = self.clean_ass_text(text)
            translated = self.translate_text(clean_text, source_lang, target_lang)
            final_text = self.restore_ass_tags(translated, tags)
            
            new_line = f"{prefix},{final_text}\n"
            translated_lines.append(new_line)
            dialogue_count += 1
        
        with open(output_file, 'w', encoding='utf-8-sig') as f:
            f.writelines(translated_lines)
        
        return dialogue_count
    
    def parse_srt_block(self, block):
        lines = block.strip().split('\n')
        if len(lines) < 3:
            return None
        
        try:
            index = lines[0]
            timing = lines[1]
            text = '\n'.join(lines[2:])
            return index, timing, text
        except:
            return None
    
    def translate_srt(self, input_file, output_file, source_lang="EN", target_lang="ES",
                     progress_callback=None):
        with open(input_file, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        
        blocks = content.strip().split('\n\n')
        translated_blocks = []
        
        for i, block in enumerate(blocks):
            if progress_callback:
                progress_callback(i, len(blocks), f"Subtítulo {i+1}/{len(blocks)}")
            
            parsed = self.parse_srt_block(block)
            if parsed is None:
                translated_blocks.append(block)
                continue
            
            index, timing, text = parsed
            translated = self.translate_text(text, source_lang, target_lang)
            new_block = f"{index}\n{timing}\n{translated}"
            translated_blocks.append(new_block)
        
        result = '\n\n'.join(translated_blocks) + '\n'
        with open(output_file, 'w', encoding='utf-8-sig') as f:
            f.write(result)
        
        return len(blocks)


class SubtitleSelectorDialog(ctk.CTkToplevel):
    """Diálogo para seleccionar subtítulo de un MKV"""
    
    def __init__(self, parent, subtitles):
        super().__init__(parent)
        
        self.selected_track = None
        self.subtitles = subtitles
        
        self.title("Seleccionar Subtítulo")
        self.geometry("600x400")
        
        # Centrar ventana
        self.transient(parent)
        self.grab_set()
        
        self.create_widgets()
    
    def create_widgets(self):
        # Título
        ctk.CTkLabel(
            self,
            text="Selecciona el subtítulo a traducir:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=20)
        
        # Frame para lista
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Lista de subtítulos
        self.sub_listbox = tk.Listbox(
            list_frame,
            height=10,
            bg="#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#f0f0f0",
            fg="white" if ctk.get_appearance_mode() == "Dark" else "black",
            font=("Consolas", 10)
        )
        self.sub_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Llenar lista
        for sub in self.subtitles:
            track_id = sub['id']
            codec = sub.get('codec', 'unknown')
            lang = sub.get('properties', {}).get('language', 'und')
            track_name = sub.get('properties', {}).get('track_name', 'Sin nombre')
            forced = sub.get('properties', {}).get('forced_track', False)
            default = sub.get('properties', {}).get('default_track', False)
            
            flags = []
            if default:
                flags.append('DEFAULT')
            if forced:
                flags.append('FORCED')
            
            flag_str = f" [{', '.join(flags)}]" if flags else ""
            
            display = f"Track {track_id}: {lang.upper()} - {codec.upper()} - {track_name}{flag_str}"
            self.sub_listbox.insert(tk.END, display)
        
        # Botones
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(
            btn_frame,
            text="Seleccionar",
            command=self.select,
            width=120
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=self.cancel,
            width=120,
            fg_color="gray"
        ).pack(side="left", padx=10)
    
    def select(self):
        selection = self.sub_listbox.curselection()
        if not selection:
            messagebox.showwarning("Sin selección", "Selecciona un subtítulo")
            return
        
        self.selected_track = self.subtitles[selection[0]]
        self.destroy()
    
    def cancel(self):
        self.selected_track = None
        self.destroy()


class SubtitleTranslatorGUI(ctk.CTk, TkinterDnD.DnDWrapper):
    """Interfaz gráfica completa con soporte MKV"""
    
    def __init__(self):
        super().__init__()
        
        # Inicializar DnD
        self.TkdndVersion = TkinterDnD._require(self)
        
        self.title("DeepL Subtitle Translator v2.0")
        self.geometry("950x800")
        
        # Configuración
        self.config_file = "translator_config.json"
        self.translator = None
        self.files_to_translate = []
        self.mkv_files_to_process = []
        self.is_translating = False
        self.current_mode = "subtitle"  # "subtitle" o "mkv"
        
        # Cargar configuración
        self.load_config()
        
        # Verificar mkvtoolnix
        self.has_mkvtoolnix = MKVProcessor.check_mkvtoolnix()
        
        # Crear interfaz
        self.create_widgets()
        
        # Verificar API key al inicio
        if self.api_key.get():
            self.verify_api_key()
    
    def load_config(self):
        """Carga la configuración guardada"""
        self.api_key = tk.StringVar(value="")
        self.source_lang = tk.StringVar(value="EN")
        self.target_lang = tk.StringVar(value="ES")
        self.output_suffix = tk.StringVar(value="_ES")
        self.auto_open = tk.BooleanVar(value=False)
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.api_key.set(config.get('api_key', ''))
                    self.source_lang.set(config.get('source_lang', 'EN'))
                    self.target_lang.set(config.get('target_lang', 'ES'))
                    self.output_suffix.set(config.get('output_suffix', '_ES'))
                    self.auto_open.set(config.get('auto_open', False))
            except:
                pass
    
    def save_config(self):
        """Guarda la configuración"""
        config = {
            'api_key': self.api_key.get(),
            'source_lang': self.source_lang.get(),
            'target_lang': self.target_lang.get(),
            'output_suffix': self.output_suffix.get(),
            'auto_open': self.auto_open.get()
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def create_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        title = ctk.CTkLabel(
            header,
            text="🎬 DeepL Subtitle Translator v2.0",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack()
        
        # Advertencia MKVToolNix
        if not self.has_mkvtoolnix:
            warning_frame = ctk.CTkFrame(self, fg_color="#d32f2f")
            warning_frame.pack(fill="x", padx=20, pady=5)
            
            ctk.CTkLabel(
                warning_frame,
                text="⚠️ MKVToolNix no detectado. La función MKV no estará disponible.",
                font=ctk.CTkFont(size=11),
                text_color="white"
            ).pack(pady=5)
        
        # Selector de modo
        mode_frame = ctk.CTkFrame(self)
        mode_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            mode_frame,
            text="Modo de trabajo:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left", padx=10)
        
        self.mode_var = tk.StringVar(value="subtitle")
        
        ctk.CTkRadioButton(
            mode_frame,
            text="📄 Traducir Subtítulos (SRT/ASS)",
            variable=self.mode_var,
            value="subtitle",
            command=self.switch_mode
        ).pack(side="left", padx=10)
        
        mkv_radio = ctk.CTkRadioButton(
            mode_frame,
            text="🎥 Procesar Archivos MKV",
            variable=self.mode_var,
            value="mkv",
            command=self.switch_mode
        )
        mkv_radio.pack(side="left", padx=10)
        
        if not self.has_mkvtoolnix:
            mkv_radio.configure(state="disabled")
        
        # API Key Frame
        api_frame = ctk.CTkFrame(self)
        api_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            api_frame,
            text="API Key de DeepL:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.api_entry = ctk.CTkEntry(
            api_frame,
            textvariable=self.api_key,
            width=400,
            placeholder_text="Ingresa tu API key de DeepL"
        )
        self.api_entry.grid(row=0, column=1, padx=10, pady=10)
        
        self.verify_btn = ctk.CTkButton(
            api_frame,
            text="Verificar",
            width=100,
            command=self.verify_api_key
        )
        self.verify_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Status de API
        self.api_status = ctk.CTkLabel(
            api_frame,
            text="",
            font=ctk.CTkFont(size=11)
        )
        self.api_status.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 10))
        
        # Configuración de idiomas
        lang_frame = ctk.CTkFrame(self)
        lang_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(lang_frame, text="De:", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, padx=(10, 5), pady=10
        )
        
        source_langs = ["EN", "ES", "JA", "KO", "ZH", "FR", "DE", "IT", "PT", "RU"]
        self.source_combo = ctk.CTkComboBox(
            lang_frame,
            values=source_langs,
            variable=self.source_lang,
            width=100
        )
        self.source_combo.grid(row=0, column=1, padx=5, pady=10)
        
        ctk.CTkLabel(lang_frame, text="A:", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=2, padx=(20, 5), pady=10
        )
        
        target_langs = ["ES", "EN-US", "EN-GB", "PT-BR", "FR", "DE", "IT", "JA"]
        self.target_combo = ctk.CTkComboBox(
            lang_frame,
            values=target_langs,
            variable=self.target_lang,
            width=100
        )
        self.target_combo.grid(row=0, column=3, padx=5, pady=10)
        
        # Sufijo (solo para modo subtitle)
        ctk.CTkLabel(lang_frame, text="Sufijo:", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=4, padx=(20, 5), pady=10
        )
        
        self.suffix_entry = ctk.CTkEntry(
            lang_frame,
            textvariable=self.output_suffix,
            width=80
        )
        self.suffix_entry.grid(row=0, column=5, padx=5, pady=10)
        
        self.auto_open_check = ctk.CTkCheckBox(
            lang_frame,
            text="Abrir carpeta al terminar",
            variable=self.auto_open
        )
        self.auto_open_check.grid(row=0, column=6, padx=20, pady=10)
        
        # Área de archivos
        self.files_frame = ctk.CTkFrame(self)
        self.files_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.files_label = ctk.CTkLabel(
            self.files_frame,
            text="Archivos a traducir (arrastra aquí o usa los botones):",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.files_label.pack(pady=(10, 5))
        
        # Lista de archivos
        self.files_list = tk.Listbox(
            self.files_frame,
            height=10,
            bg="#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#f0f0f0",
            fg="white" if ctk.get_appearance_mode() == "Dark" else "black",
            selectmode=tk.EXTENDED
        )
        self.files_list.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Configurar drag and drop
        self.files_list.drop_target_register(DND_FILES)
        self.files_list.dnd_bind('<<Drop>>', self.drop_files)
        
        # Botones de archivos
        self.btn_frame = ctk.CTkFrame(self.files_frame, fg_color="transparent")
        self.btn_frame.pack(fill="x", padx=10, pady=5)
        
        self.add_files_btn = ctk.CTkButton(
            self.btn_frame,
            text="➕ Agregar archivos",
            command=self.add_files
        )
        self.add_files_btn.pack(side="left", padx=5)
        
        self.add_folder_btn = ctk.CTkButton(
            self.btn_frame,
            text="📁 Agregar carpeta",
            command=self.add_folder
        )
        self.add_folder_btn.pack(side="left", padx=5)
        
        ctk.CTkButton(
            self.btn_frame,
            text="🗑️ Limpiar lista",
            command=self.clear_files,
            fg_color="#d32f2f",
            hover_color="#b71c1c"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            self.btn_frame,
            text="❌ Quitar seleccionados",
            command=self.remove_selected
        ).pack(side="left", padx=5)
        
        # Progress
        progress_frame = ctk.CTkFrame(self)
        progress_frame.pack(fill="x", padx=20, pady=10)
        
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="Listo para traducir",
            font=ctk.CTkFont(size=11)
        )
        self.progress_label.pack(pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=400)
        self.progress_bar.pack(pady=5)
        self.progress_bar.set(0)
        
        self.file_progress = ctk.CTkLabel(
            progress_frame,
            text="",
            font=ctk.CTkFont(size=10)
        )
        self.file_progress.pack(pady=5)
        
        # Botón traducir
        self.translate_btn = ctk.CTkButton(
            self,
            text="🚀 TRADUCIR ARCHIVOS",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=50,
            command=self.start_translation,
            fg_color="#2e7d32",
            hover_color="#1b5e20"
        )
        self.translate_btn.pack(pady=10, padx=20, fill="x")
    
    def switch_mode(self):
        """Cambia entre modo subtítulos y modo MKV"""
        mode = self.mode_var.get()
        self.current_mode = mode
        
        # Limpiar listas
        self.clear_files()
        
        if mode == "subtitle":
            self.files_label.configure(
                text="Archivos a traducir (arrastra aquí o usa los botones):"
            )
            self.add_files_btn.configure(text="➕ Agregar archivos")
            self.add_folder_btn.configure(text="📁 Agregar carpeta")
            self.translate_btn.configure(text="🚀 TRADUCIR ARCHIVOS")
            self.suffix_entry.configure(state="normal")
        else:  # mkv
            self.files_label.configure(
                text="Archivos MKV a procesar (se extraerá, traducirá y reinsertará subtítulo):"
            )
            self.add_files_btn.configure(text="➕ Agregar archivos MKV")
            self.add_folder_btn.configure(text="📁 Agregar carpeta MKV")
            self.translate_btn.configure(text="🎥 PROCESAR ARCHIVOS MKV")
            self.suffix_entry.configure(state="disabled")
    
    def verify_api_key(self):
        """Verifica la API key"""
        api_key = self.api_key.get().strip()
        
        if not api_key:
            self.api_status.configure(
                text="⚠️ Ingresa una API key",
                text_color="orange"
            )
            return
        
        try:
            self.translator = SubtitleTranslator(api_key)
            usage, error = self.translator.get_usage()
            
            if error:
                self.api_status.configure(
                    text=f"❌ Error: {error}",
                    text_color="red"
                )
                self.translator = None
            else:
                percent = usage['percent']
                remaining = usage['remaining']
                
                self.api_status.configure(
                    text=f"✅ API válida | Uso: {percent:.1f}% | Restante: {remaining:,} caracteres",
                    text_color="green"
                )
                self.save_config()
        
        except Exception as e:
            self.api_status.configure(
                text=f"❌ Error: {str(e)}",
                text_color="red"
            )
            self.translator = None
    
    def drop_files(self, event):
        """Maneja archivos arrastrados"""
        files = self.tk.splitlist(event.data)
        
        for file in files:
            file = file.strip('{}')
            if not os.path.isfile(file):
                continue
            
            ext = Path(file).suffix.lower()
            
            if self.current_mode == "subtitle":
                if ext in ['.ass', '.srt']:
                    if file not in self.files_to_translate:
                        self.files_to_translate.append(file)
                        self.files_list.insert(tk.END, Path(file).name)
            else:  # mkv
                if ext == '.mkv':
                    if file not in self.mkv_files_to_process:
                        self.mkv_files_to_process.append(file)
                        self.files_list.insert(tk.END, Path(file).name)
    
    def add_files(self):
        """Agregar archivos manualmente"""
        if self.current_mode == "subtitle":
            files = filedialog.askopenfilenames(
                title="Seleccionar subtítulos",
                filetypes=[
                    ("Archivos de subtítulos", "*.ass *.srt"),
                    ("ASS files", "*.ass"),
                    ("SRT files", "*.srt"),
                    ("Todos los archivos", "*.*")
                ]
            )
            
            for file in files:
                if file not in self.files_to_translate:
                    self.files_to_translate.append(file)
                    self.files_list.insert(tk.END, Path(file).name)
        
        else:  # mkv
            files = filedialog.askopenfilenames(
                title="Seleccionar archivos MKV",
                filetypes=[
                    ("Archivos MKV", "*.mkv"),
                    ("Todos los archivos", "*.*")
                ]
            )
            
            for file in files:
                if file not in self.mkv_files_to_process:
                    self.mkv_files_to_process.append(file)
                    self.files_list.insert(tk.END, Path(file).name)
    
    def add_folder(self):
        """Agregar todos los archivos de una carpeta"""
        folder = filedialog.askdirectory(title="Seleccionar carpeta")
        
        if not folder:
            return
        
        count = 0
        
        if self.current_mode == "subtitle":
            for file in Path(folder).rglob("*"):
                if file.suffix.lower() in ['.ass', '.srt']:
                    file_str = str(file)
                    if file_str not in self.files_to_translate:
                        self.files_to_translate.append(file_str)
                        self.files_list.insert(tk.END, file.name)
                        count += 1
        else:  # mkv
            for file in Path(folder).rglob("*.mkv"):
                file_str = str(file)
                if file_str not in self.mkv_files_to_process:
                    self.mkv_files_to_process.append(file_str)
                    self.files_list.insert(tk.END, file.name)
                    count += 1
        
        messagebox.showinfo("Archivos agregados", f"Se agregaron {count} archivos")
    
    def clear_files(self):
        """Limpiar lista de archivos"""
        self.files_to_translate.clear()
        self.mkv_files_to_process.clear()
        self.files_list.delete(0, tk.END)
    
    def remove_selected(self):
        """Quitar archivos seleccionados"""
        selected = self.files_list.curselection()
        
        for index in reversed(selected):
            self.files_list.delete(index)
            
            if self.current_mode == "subtitle":
                del self.files_to_translate[index]
            else:
                del self.mkv_files_to_process[index]
    
    def start_translation(self):
        """Inicia la traducción en un hilo separado"""
        if self.is_translating:
            messagebox.showwarning("Ocupado", "Ya hay una traducción en proceso")
            return
        
        if not self.translator:
            messagebox.showerror("Error", "Verifica tu API key primero")
            return
        
        if self.current_mode == "subtitle":
            if not self.files_to_translate:
                messagebox.showwarning("Sin archivos", "Agrega archivos para traducir")
                return
        else:  # mkv
            if not self.mkv_files_to_process:
                messagebox.showwarning("Sin archivos", "Agrega archivos MKV para procesar")
                return
        
        # Guardar configuración
        self.save_config()
        
        # Deshabilitar botón
        self.translate_btn.configure(state="disabled", text="⏳ Procesando...")
        
        # Iniciar traducción en hilo
        self.is_translating = True
        
        if self.current_mode == "subtitle":
            thread = threading.Thread(target=self.translate_files, daemon=True)
        else:
            thread = threading.Thread(target=self.process_mkv_files, daemon=True)
        
        thread.start()
    
    def translate_files(self):
        """Traduce archivos de subtítulos"""
        total_files = len(self.files_to_translate)
        successful = 0
        failed = []
        
        for i, file_path in enumerate(self.files_to_translate):
            try:
                self.progress_label.configure(
                    text=f"Traduciendo archivo {i+1}/{total_files}: {Path(file_path).name}"
                )
                
                file_obj = Path(file_path)
                output_name = f"{file_obj.stem}{self.output_suffix.get()}{file_obj.suffix}"
                output_path = file_obj.parent / output_name
                
                ext = file_obj.suffix.lower()
                
                def update_progress(current, total, msg):
                    progress = (current / total) if total > 0 else 0
                    self.progress_bar.set(progress)
                    self.file_progress.configure(text=msg)
                
                if ext == '.ass':
                    count = self.translator.translate_ass(
                        file_path,
                        str(output_path),
                        self.source_lang.get(),
                        self.target_lang.get(),
                        update_progress
                    )
                else:
                    count = self.translator.translate_srt(
                        file_path,
                        str(output_path),
                        self.source_lang.get(),
                        self.target_lang.get(),
                        update_progress
                    )
                
                successful += 1
                
            except Exception as e:
                failed.append((Path(file_path).name, str(e)))
        
        self.finish_translation(successful, total_files, failed)
    
    def process_mkv_files(self):
        """Procesa archivos MKV: extrae, traduce y reinserta subtítulos"""
        total_files = len(self.mkv_files_to_process)
        successful = 0
        failed = []
        
        for i, mkv_path in enumerate(self.mkv_files_to_process):
            try:
                self.progress_label.configure(
                    text=f"Procesando MKV {i+1}/{total_files}: {Path(mkv_path).name}"
                )
                self.progress_bar.set(0)
                
                # 1. Obtener info del MKV
                self.file_progress.configure(text="Analizando MKV...")
                mkv_info = MKVProcessor.get_mkv_info(mkv_path)
                
                if not mkv_info:
                    raise Exception("No se pudo leer información del MKV")
                
                # 2. Filtrar subtítulos
                subtitles = [track for track in mkv_info.get('tracks', []) 
                           if track['type'] == 'subtitles']
                
                if not subtitles:
                    raise Exception("El MKV no contiene subtítulos")
                
                # 3. Seleccionar subtítulo (en el hilo principal)
                selected_track = None
                
                def select_subtitle():
                    nonlocal selected_track
                    dialog = SubtitleSelectorDialog(self, subtitles)
                    self.wait_window(dialog)
                    selected_track = dialog.selected_track
                
                self.after(0, select_subtitle)
                
                # Esperar a que el usuario seleccione
                while selected_track is None and self.is_translating:
                    import time
                    time.sleep(0.1)
                
                if not selected_track:
                    raise Exception("No se seleccionó ningún subtítulo")
                
                # 4. Extraer subtítulo
                self.file_progress.configure(text="Extrayendo subtítulo...")
                self.progress_bar.set(0.2)
                
                track_id = selected_track['id']
                codec = selected_track.get('codec', 'srt')
                
                # Determinar extensión
                if 'ass' in codec.lower() or 'ssa' in codec.lower():
                    sub_ext = '.ass'
                else:
                    sub_ext = '.srt'
                
                temp_sub = Path(mkv_path).parent / f"temp_subtitle{sub_ext}"
                
                if not MKVProcessor.extract_subtitle(mkv_path, track_id, str(temp_sub)):
                    raise Exception("No se pudo extraer el subtítulo")
                
                # 5. Traducir subtítulo
                self.file_progress.configure(text="Traduciendo subtítulo...")
                self.progress_bar.set(0.4)
                
                translated_sub = Path(mkv_path).parent / f"temp_translated{sub_ext}"
                
                def update_progress(current, total, msg):
                    base_progress = 0.4
                    progress = base_progress + (current / total) * 0.4 if total > 0 else base_progress
                    self.progress_bar.set(progress)
                
                if sub_ext == '.ass':
                    self.translator.translate_ass(
                        str(temp_sub),
                        str(translated_sub),
                        self.source_lang.get(),
                        self.target_lang.get(),
                        update_progress
                    )
                else:
                    self.translator.translate_srt(
                        str(temp_sub),
                        str(translated_sub),
                        self.source_lang.get(),
                        self.target_lang.get(),
                        update_progress
                    )
                
                # 6. Remuxear MKV
                self.file_progress.configure(text="Reinsertando subtítulo en MKV...")
                self.progress_bar.set(0.8)
                
                temp_output = Path(mkv_path).parent / f"temp_output.mkv"
                
                success, error = MKVProcessor.remux_mkv(
                    mkv_path,
                    str(translated_sub),
                    str(temp_output),
                    "Español (Latinoamérica)"
                )
                
                if not success:
                    raise Exception(f"Error al remuxear: {error}")
                
                # 7. Reemplazar archivo original
                self.file_progress.configure(text="Reemplazando archivo original...")
                self.progress_bar.set(0.9)
                
                # Backup del original (opcional)
                # backup_path = Path(mkv_path).with_suffix('.mkv.backup')
                # shutil.copy2(mkv_path, backup_path)
                
                # Reemplazar
                os.remove(mkv_path)
                shutil.move(str(temp_output), mkv_path)
                
                # 8. Limpiar archivos temporales
                if temp_sub.exists():
                    temp_sub.unlink()
                if translated_sub.exists():
                    translated_sub.unlink()
                
                self.progress_bar.set(1.0)
                successful += 1
                
            except Exception as e:
                failed.append((Path(mkv_path).name, str(e)))
                
                # Limpiar temporales en caso de error
                temp_files = [
                    Path(mkv_path).parent / "temp_subtitle.ass",
                    Path(mkv_path).parent / "temp_subtitle.srt",
                    Path(mkv_path).parent / "temp_translated.ass",
                    Path(mkv_path).parent / "temp_translated.srt",
                    Path(mkv_path).parent / "temp_output.mkv"
                ]
                
                for temp_file in temp_files:
                    if temp_file.exists():
                        try:
                            temp_file.unlink()
                        except:
                            pass
        
        self.finish_translation(successful, total_files, failed)
    
    def finish_translation(self, successful, total, failed):
        """Finaliza el proceso de traducción"""
        self.is_translating = False
        self.progress_bar.set(1.0)
        self.file_progress.configure(text="")
        
        # Mensaje final
        if successful == total:
            message = f"✅ {successful} archivos procesados exitosamente"
            self.progress_label.configure(text=message)
            
            # Abrir carpeta si está habilitado
            if self.auto_open.get():
                if self.current_mode == "subtitle" and self.files_to_translate:
                    folder = Path(self.files_to_translate[0]).parent
                elif self.current_mode == "mkv" and self.mkv_files_to_process:
                    folder = Path(self.mkv_files_to_process[0]).parent
                else:
                    folder = None
                
                if folder:
                    os.startfile(folder)
            
            messagebox.showinfo("Completado", message)
        else:
            message = f"✅ {successful} exitosos\n❌ {len(failed)} fallidos"
            self.progress_label.configure(text=message)
            
            error_details = "\n".join([f"- {name}: {error}" for name, error in failed])
            messagebox.showwarning("Completado con errores", f"{message}\n\n{error_details}")
        
        # Rehabilitar botón
        if self.current_mode == "subtitle":
            self.translate_btn.configure(state="normal", text="🚀 TRADUCIR ARCHIVOS")
        else:
            self.translate_btn.configure(state="normal", text="🎥 PROCESAR ARCHIVOS MKV")


def main():
    """Función principal"""
    # Verificar dependencias
    try:
        import customtkinter
        import deepl
        from tkinterdnd2 import TkinterDnD
    except ImportError as e:
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()
        
        missing = str(e).split("'")[1]
        messagebox.showerror(
            "Dependencias faltantes",
            f"Falta instalar: {missing}\n\n"
            "Ejecuta en la terminal:\n"
            "pip install customtkinter deepl tkinterdnd2"
        )
        return
    
    app = SubtitleTranslatorGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
