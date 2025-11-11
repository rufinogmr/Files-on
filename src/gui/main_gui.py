"""
Main GUI - Interactive graphical interface for file processing
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import time
import os
from pathlib import Path
from typing import List, Dict
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from processors.file_processor import FileProcessor
from processors.duplicate_detector import DuplicateDetector
from processors.data_extractor import DataExtractor
from utils.suggestion_engine import SuggestionEngine


class FileProcessorGUI:
    """Main GUI Application"""

    def __init__(self, root):
        self.root = root
        self.root.title("Organizador de Comprovantes - Files-On")
        self.root.geometry("1000x700")
        self.root.minsize(900, 600)

        # Initialize processors
        self.file_processor = FileProcessor()
        self.duplicate_detector = DuplicateDetector()
        self.data_extractor = DataExtractor()
        self.suggestion_engine = SuggestionEngine()

        # State variables
        self.selected_files = []
        self.processed_results = []
        self.extraction_results = []
        self.organization_plan = []
        self.is_processing = False
        self.start_time = None

        # Create GUI
        self.create_widgets()

    def create_widgets(self):
        """Create all GUI widgets"""

        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        title_label = tk.Label(
            title_frame,
            text="📁 Organizador de Comprovantes",
            font=('Arial', 18, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=15)

        # Main container
        main_container = tk.Frame(self.root, padx=20, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)

        # File selection section
        file_section = tk.LabelFrame(
            main_container,
            text="Seleção de Arquivos",
            font=('Arial', 11, 'bold'),
            padx=10,
            pady=10
        )
        file_section.pack(fill=tk.X, pady=(0, 10))

        # Buttons row
        button_row = tk.Frame(file_section)
        button_row.pack(fill=tk.X)

        self.select_files_btn = tk.Button(
            button_row,
            text="📂 Selecionar Arquivos",
            command=self.select_files,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8
        )
        self.select_files_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.select_folder_btn = tk.Button(
            button_row,
            text="📁 Selecionar Pasta",
            command=self.select_folder,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8
        )
        self.select_folder_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.clear_btn = tk.Button(
            button_row,
            text="🗑️ Limpar",
            command=self.clear_selection,
            bg='#95a5a6',
            fg='white',
            font=('Arial', 10, 'bold'),
            padx=20,
            pady=8
        )
        self.clear_btn.pack(side=tk.LEFT)

        # File count label
        self.file_count_label = tk.Label(
            file_section,
            text="Nenhum arquivo selecionado",
            font=('Arial', 10)
        )
        self.file_count_label.pack(anchor=tk.W, pady=(10, 0))

        # Progress section
        progress_section = tk.LabelFrame(
            main_container,
            text="Progresso",
            font=('Arial', 11, 'bold'),
            padx=10,
            pady=10
        )
        progress_section.pack(fill=tk.X, pady=(0, 10))

        # Status label
        self.status_label = tk.Label(
            progress_section,
            text="Aguardando seleção de arquivos...",
            font=('Arial', 10),
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, pady=(0, 5))

        # Progress bar
        self.progress_bar = ttk.Progressbar(
            progress_section,
            mode='determinate',
            length=400
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))

        # Time and stats row
        stats_row = tk.Frame(progress_section)
        stats_row.pack(fill=tk.X)

        self.time_label = tk.Label(
            stats_row,
            text="Tempo: 0s",
            font=('Arial', 9),
            fg='#7f8c8d'
        )
        self.time_label.pack(side=tk.LEFT, padx=(0, 20))

        self.files_processed_label = tk.Label(
            stats_row,
            text="Processados: 0/0",
            font=('Arial', 9),
            fg='#7f8c8d'
        )
        self.files_processed_label.pack(side=tk.LEFT)

        # Action buttons
        action_section = tk.Frame(main_container)
        action_section.pack(fill=tk.X, pady=(0, 10))

        self.process_btn = tk.Button(
            action_section,
            text="▶️ Processar Arquivos",
            command=self.start_processing,
            bg='#27ae60',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=30,
            pady=10,
            state=tk.DISABLED
        )
        self.process_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.organize_btn = tk.Button(
            action_section,
            text="📋 Organizar Arquivos",
            command=self.organize_files,
            bg='#f39c12',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=30,
            pady=10,
            state=tk.DISABLED
        )
        self.organize_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.export_btn = tk.Button(
            action_section,
            text="💾 Exportar Relatório",
            command=self.export_report,
            bg='#9b59b6',
            fg='white',
            font=('Arial', 11, 'bold'),
            padx=30,
            pady=10,
            state=tk.DISABLED
        )
        self.export_btn.pack(side=tk.LEFT)

        # Results section
        results_section = tk.LabelFrame(
            main_container,
            text="Resultados",
            font=('Arial', 11, 'bold'),
            padx=10,
            pady=10
        )
        results_section.pack(fill=tk.BOTH, expand=True)

        # Scrolled text for results
        self.results_text = scrolledtext.ScrolledText(
            results_section,
            wrap=tk.WORD,
            font=('Courier', 9),
            bg='#ecf0f1',
            height=15
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)

        # Initial message
        self.log_message("Bem-vindo ao Organizador de Comprovantes!")
        self.log_message("Selecione arquivos ou uma pasta para começar.")

    def select_files(self):
        """Open file selection dialog"""
        files = filedialog.askopenfilenames(
            title="Selecionar Arquivos",
            filetypes=[
                ("Todos os arquivos suportados", "*.pdf *.png *.jpg *.jpeg *.txt"),
                ("PDF", "*.pdf"),
                ("Imagens", "*.png *.jpg *.jpeg"),
                ("Texto", "*.txt"),
                ("Todos os arquivos", "*.*")
            ]
        )
        if files:
            self.selected_files.extend(files)
            self.update_file_count()
            self.process_btn.config(state=tk.NORMAL)

    def select_folder(self):
        """Open folder selection dialog"""
        folder = filedialog.askdirectory(title="Selecionar Pasta")
        if folder:
            # Find all supported files in folder
            supported_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.txt', '.bmp', '.tiff', '.gif']
            files = []
            for root, dirs, filenames in os.walk(folder):
                for filename in filenames:
                    if Path(filename).suffix.lower() in supported_extensions:
                        files.append(os.path.join(root, filename))

            if files:
                self.selected_files.extend(files)
                self.update_file_count()
                self.process_btn.config(state=tk.NORMAL)
                self.log_message(f"Encontrados {len(files)} arquivos na pasta selecionada.")
            else:
                messagebox.showwarning(
                    "Nenhum arquivo",
                    "Nenhum arquivo suportado encontrado na pasta selecionada."
                )

    def clear_selection(self):
        """Clear selected files and results"""
        self.selected_files = []
        self.processed_results = []
        self.extraction_results = []
        self.organization_plan = []
        self.update_file_count()
        self.progress_bar['value'] = 0
        self.status_label.config(text="Aguardando seleção de arquivos...")
        self.time_label.config(text="Tempo: 0s")
        self.files_processed_label.config(text="Processados: 0/0")
        self.results_text.delete(1.0, tk.END)
        self.log_message("Seleção limpa. Pronto para novos arquivos.")
        self.process_btn.config(state=tk.DISABLED)
        self.organize_btn.config(state=tk.DISABLED)
        self.export_btn.config(state=tk.DISABLED)

    def update_file_count(self):
        """Update file count label"""
        count = len(self.selected_files)
        if count == 0:
            self.file_count_label.config(text="Nenhum arquivo selecionado")
        elif count == 1:
            self.file_count_label.config(text="1 arquivo selecionado")
        else:
            self.file_count_label.config(text=f"{count} arquivos selecionados")

    def log_message(self, message: str):
        """Add message to results text area"""
        self.results_text.insert(tk.END, f"{message}\n")
        self.results_text.see(tk.END)
        self.root.update_idletasks()

    def start_processing(self):
        """Start file processing in separate thread"""
        if self.is_processing:
            return

        self.is_processing = True
        self.start_time = time.time()
        self.process_btn.config(state=tk.DISABLED)
        self.select_files_btn.config(state=tk.DISABLED)
        self.select_folder_btn.config(state=tk.DISABLED)
        self.clear_btn.config(state=tk.DISABLED)

        # Start processing in separate thread
        thread = threading.Thread(target=self.process_files, daemon=True)
        thread.start()

        # Start time updater
        self.update_time()

    def process_files(self):
        """Process all selected files (runs in separate thread)"""
        try:
            total = len(self.selected_files)
            self.root.after(0, self.log_message, f"\n{'='*60}")
            self.root.after(0, self.log_message, f"Iniciando processamento de {total} arquivos...")
            self.root.after(0, self.log_message, f"{'='*60}\n")

            # Step 1: Extract text from files
            self.root.after(0, self.status_label.config, {'text': 'Extraindo texto dos arquivos...'})
            self.processed_results = self.file_processor.process_multiple_files(
                self.selected_files,
                progress_callback=self.update_progress
            )

            # Step 2: Detect duplicates
            self.root.after(0, self.status_label.config, {'text': 'Detectando duplicatas...'})
            self.root.after(0, self.log_message, "\n--- DETECÇÃO DE DUPLICATAS ---")
            duplicate_report = self.duplicate_detector.generate_duplicate_report(self.processed_results)

            exact_dups = duplicate_report['exact_duplicate_count']
            similar_files = duplicate_report['similar_file_count']
            self.root.after(0, self.log_message, f"✓ Duplicatas exatas: {exact_dups}")
            self.root.after(0, self.log_message, f"✓ Arquivos similares: {similar_files}")

            # Step 3: Extract data
            self.root.after(0, self.status_label.config, {'text': 'Extraindo dados (data, nome, valor)...'})
            self.root.after(0, self.log_message, "\n--- EXTRAÇÃO DE DADOS ---")
            self.extraction_results = self.data_extractor.extract_from_multiple_files(self.processed_results)

            success_count = sum(1 for r in self.extraction_results if r.get('success'))
            self.root.after(0, self.log_message, f"✓ Dados extraídos de {success_count}/{total} arquivos")

            # Step 4: Generate organization suggestions
            self.root.after(0, self.status_label.config, {'text': 'Gerando sugestões de organização...'})
            self.root.after(0, self.log_message, "\n--- SUGESTÕES DE ORGANIZAÇÃO ---")
            output_dir = os.path.join(os.path.dirname(self.selected_files[0]), "Organizados")
            self.organization_plan = self.suggestion_engine.generate_organization_plan(
                self.extraction_results,
                output_dir
            )

            summary = self.suggestion_engine.get_organization_summary(self.organization_plan)
            self.root.after(0, self.log_message, f"✓ Pastas sugeridas: {summary['total_folders']}")
            self.root.after(0, self.log_message, f"✓ Arquivos a renomear: {summary['files_to_rename']}")

            # Display sample results
            self.root.after(0, self.log_message, "\n--- EXEMPLO DE DADOS EXTRAÍDOS ---")
            for i, result in enumerate(self.extraction_results[:5]):
                if result.get('success'):
                    extracted = result['extracted_data']
                    filename = Path(result['file_name']).name
                    self.root.after(0, self.log_message, f"\n{i+1}. {filename}")

                    if extracted.get('primary_date'):
                        date_str = self.data_extractor.format_date(extracted['primary_date'])
                        self.root.after(0, self.log_message, f"   Data: {date_str}")

                    if extracted.get('primary_name'):
                        self.root.after(0, self.log_message, f"   Nome: {extracted['primary_name']}")

                    if extracted.get('primary_value'):
                        value_str = self.data_extractor.format_value(extracted['primary_value'])
                        self.root.after(0, self.log_message, f"   Valor: {value_str}")

            # Complete
            self.root.after(0, self.status_label.config, {'text': 'Processamento concluído!'})
            self.root.after(0, self.log_message, f"\n{'='*60}")
            self.root.after(0, self.log_message, "✅ PROCESSAMENTO CONCLUÍDO!")
            self.root.after(0, self.log_message, f"{'='*60}\n")

            # Enable organize button
            self.root.after(0, self.organize_btn.config, {'state': tk.NORMAL})
            self.root.after(0, self.export_btn.config, {'state': tk.NORMAL})

        except Exception as e:
            self.root.after(0, self.log_message, f"\n❌ ERRO: {str(e)}")
            self.root.after(0, self.status_label.config, {'text': f'Erro: {str(e)}'})

        finally:
            self.is_processing = False
            self.root.after(0, self.process_btn.config, {'state': tk.NORMAL})
            self.root.after(0, self.select_files_btn.config, {'state': tk.NORMAL})
            self.root.after(0, self.select_folder_btn.config, {'state': tk.NORMAL})
            self.root.after(0, self.clear_btn.config, {'state': tk.NORMAL})

    def update_progress(self, current: int, total: int, file_path: str):
        """Update progress bar and labels"""
        progress = (current / total) * 100
        self.root.after(0, self.progress_bar.config, {'value': progress})
        self.root.after(0, self.files_processed_label.config, {'text': f"Processados: {current}/{total}"})
        filename = Path(file_path).name
        self.root.after(0, self.log_message, f"  [{current}/{total}] {filename}")

    def update_time(self):
        """Update elapsed time label"""
        if self.is_processing and self.start_time:
            elapsed = int(time.time() - self.start_time)
            self.time_label.config(text=f"Tempo: {elapsed}s")
            self.root.after(1000, self.update_time)

    def organize_files(self):
        """Execute the organization plan"""
        if not self.organization_plan:
            messagebox.showwarning("Nenhum plano", "Processe os arquivos primeiro!")
            return

        # Ask user for output directory
        output_dir = filedialog.askdirectory(
            title="Selecionar pasta de destino",
            initialdir=os.path.dirname(self.selected_files[0])
        )

        if not output_dir:
            return

        # Update plan with new output directory
        for item in self.organization_plan:
            folder_rel = item['suggested_folder']
            full_folder = os.path.join(output_dir, folder_rel)
            item['full_folder_path'] = full_folder
            item['full_new_path'] = os.path.join(full_folder, item['suggested_filename'])

        # Ask if copy or move
        response = messagebox.askyesnocancel(
            "Copiar ou Mover?",
            "Deseja COPIAR os arquivos (Sim) ou MOVÊ-LOS (Não)?\n\nCancelar para voltar."
        )

        if response is None:
            return

        copy_files = response

        self.log_message(f"\n{'='*60}")
        self.log_message(f"Organizando arquivos...")
        self.log_message(f"{'='*60}\n")

        # Execute organization
        results = self.suggestion_engine.execute_organization_plan(self.organization_plan, copy_files)

        success_count = sum(1 for r in results if r.get('success'))
        fail_count = len(results) - success_count

        self.log_message(f"\n✅ Arquivos organizados com sucesso: {success_count}")
        if fail_count > 0:
            self.log_message(f"❌ Falhas: {fail_count}")

        messagebox.showinfo(
            "Concluído",
            f"Organização concluída!\n\nSucesso: {success_count}\nFalhas: {fail_count}"
        )

    def export_report(self):
        """Export detailed report to text file"""
        if not self.extraction_results:
            messagebox.showwarning("Nenhum dado", "Processe os arquivos primeiro!")
            return

        file_path = filedialog.asksaveasfilename(
            title="Salvar Relatório",
            defaultextension=".txt",
            filetypes=[("Arquivo de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )

        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("RELATÓRIO DE PROCESSAMENTO - FILES-ON\n")
                f.write("=" * 80 + "\n\n")

                f.write(f"Total de arquivos: {len(self.extraction_results)}\n")
                f.write(f"Data do relatório: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")

                f.write("=" * 80 + "\n")
                f.write("DETALHES DOS ARQUIVOS\n")
                f.write("=" * 80 + "\n\n")

                for i, result in enumerate(self.extraction_results, 1):
                    f.write(f"{i}. {result['file_name']}\n")
                    f.write(f"   Caminho: {result['file_path']}\n")

                    if result.get('success'):
                        extracted = result['extracted_data']
                        if extracted.get('primary_date'):
                            f.write(f"   Data: {self.data_extractor.format_date(extracted['primary_date'])}\n")
                        if extracted.get('primary_name'):
                            f.write(f"   Nome: {extracted['primary_name']}\n")
                        if extracted.get('primary_value'):
                            f.write(f"   Valor: {self.data_extractor.format_value(extracted['primary_value'])}\n")

                        # Organization suggestion
                        plan_item = next((p for p in self.organization_plan if p['original_path'] == result['file_path']), None)
                        if plan_item:
                            f.write(f"   Novo nome sugerido: {plan_item['suggested_filename']}\n")
                            f.write(f"   Pasta sugerida: {plan_item['suggested_folder']}\n")
                    else:
                        f.write(f"   Erro: {result.get('error', 'Desconhecido')}\n")

                    f.write("\n")

            self.log_message(f"\n✅ Relatório exportado: {file_path}")
            messagebox.showinfo("Sucesso", f"Relatório exportado com sucesso!\n\n{file_path}")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar relatório:\n{str(e)}")

from datetime import datetime

def main():
    """Main entry point"""
    root = tk.Tk()
    app = FileProcessorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
