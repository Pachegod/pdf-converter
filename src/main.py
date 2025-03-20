import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                            QRadioButton, QButtonGroup, QCheckBox, QProgressBar, 
                            QMessageBox, QFrame)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QIcon, QDragEnterEvent, QDropEvent, QPixmap
from pdf_to_txt import converter_pdf_para_txt, converter_pdf_para_docx
import darkdetect

class PDFConverterThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, files, output_format, use_ocr):
        super().__init__()
        self.files = files
        self.output_format = output_format
        self.use_ocr = use_ocr
    
    def run(self):
        try:
            # Cria pasta de saída se não existir
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "arquivos_convertidos")
            os.makedirs(output_dir, exist_ok=True)

            total_files = len(self.files)
            for i, pdf_file in enumerate(self.files, 1):
                # Define o caminho do arquivo de saída
                output_name = os.path.splitext(os.path.basename(pdf_file))[0]
                output_ext = ".txt" if self.output_format.lower() == "txt" else ".docx"
                output_path = os.path.join(output_dir, output_name + output_ext)

                # Converte o arquivo
                if self.output_format.lower() == "txt":
                    success, message = converter_pdf_para_txt(pdf_file, output_path, self.use_ocr)
                else:
                    success, message = converter_pdf_para_docx(pdf_file, output_path, self.use_ocr)

                if not success:
                    self.error.emit(message)
                    return

                self.progress.emit(int((i / total_files) * 100))

            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

class DropArea(QWidget):
    filesDropped = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        layout = QVBoxLayout()
        self.label = QLabel("Arraste arquivos PDF aqui ou clique para selecionar")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setMinimumHeight(100)
        self.setStyleSheet("""
            QWidget {
                border: 2px dashed #aaa;
                border-radius: 5px;
                padding: 10px;
            }
        """)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        pdf_files = [f for f in files if f.lower().endswith('.pdf')]
        if pdf_files:
            self.filesDropped.emit(pdf_files)

    def mousePressEvent(self, event):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecione arquivos PDF",
            "",
            "Arquivos PDF (*.pdf)"
        )
        if files:
            self.filesDropped.emit(files)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Conversor de PDF")
        self.setMinimumWidth(700)
        self.selected_files = []

        # Configurar ícone da janela
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resources", "logo.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Área de arrastar e soltar
        self.drop_area = DropArea()
        self.drop_area.filesDropped.connect(self.handle_dropped_files)
        layout.addWidget(self.drop_area)

        # Container para opções
        options_container = QWidget()
        options_layout = QVBoxLayout(options_container)
        options_layout.setSpacing(15)
        options_layout.setContentsMargins(0, 0, 0, 0)

        # Formato de saída com RadioButtons em layout horizontal
        format_layout = QHBoxLayout()
        format_label = QLabel("Formato de saída:")
        format_layout.addWidget(format_label)
        
        self.format_group = QButtonGroup()
        self.docx_radio = QRadioButton("DOCX")
        self.txt_radio = QRadioButton("TXT")
        self.docx_radio.setChecked(True)
        
        format_layout.addWidget(self.docx_radio)
        format_layout.addWidget(self.txt_radio)
        format_layout.addStretch()
        
        self.format_group.addButton(self.docx_radio)
        self.format_group.addButton(self.txt_radio)
        
        options_layout.addLayout(format_layout)

        # Opção de OCR
        self.ocr_checkbox = QCheckBox("Usar reconhecimento de imagem para texto (OCR)")
        options_layout.addWidget(self.ocr_checkbox)
        
        layout.addWidget(options_container)

        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedHeight(15)
        layout.addWidget(self.progress_bar)

        # Container para botões
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        # Botão de converter
        self.convert_button = QPushButton("Converter")
        self.convert_button.setEnabled(False)
        self.convert_button.clicked.connect(self.start_conversion)
        self.convert_button.setMinimumWidth(150)
        self.convert_button.setFixedHeight(45)
        buttons_layout.addWidget(self.convert_button)

        # Botão para abrir pasta de arquivos convertidos
        self.open_folder_button = QPushButton("Ver Arquivos Convertidos")
        self.open_folder_button.clicked.connect(self.open_output_folder)
        self.open_folder_button.setMinimumWidth(180)
        self.open_folder_button.setFixedHeight(45)
        buttons_layout.addWidget(self.open_folder_button)

        layout.addLayout(buttons_layout)

        # Configurar tema
        self.setup_theme()

        # Inicializar thread de conversão
        self.converter_thread = None

    def setup_theme(self):
        is_dark = darkdetect.isDark()
        if is_dark:
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #1a1a1a;
                    color: #ffffff;
                }
                QPushButton {
                    background-color: #2d5a7c;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #3d7aa6;
                }
                QPushButton:disabled {
                    background-color: #4a4a4a;
                }
                QRadioButton {
                    color: white;
                    font-size: 14px;
                    padding: 5px;
                    spacing: 8px;
                }
                QRadioButton::indicator {
                    width: 18px;
                    height: 18px;
                }
                QCheckBox {
                    color: white;
                    font-size: 14px;
                    padding: 5px;
                    spacing: 8px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
                QProgressBar {
                    border: none;
                    border-radius: 7px;
                    text-align: center;
                    font-size: 12px;
                    font-weight: bold;
                    background-color: #2a2a2a;
                }
                QProgressBar::chunk {
                    background-color: #2d5a7c;
                    border-radius: 7px;
                }
                QLabel {
                    font-size: 14px;
                    font-weight: bold;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #f5f5f5;
                    color: #333333;
                }
                QPushButton {
                    background-color: #2d5a7c;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #3d7aa6;
                }
                QPushButton:disabled {
                    background-color: #cccccc;
                }
                QRadioButton {
                    font-size: 14px;
                    padding: 5px;
                    spacing: 8px;
                }
                QRadioButton::indicator {
                    width: 18px;
                    height: 18px;
                }
                QCheckBox {
                    font-size: 14px;
                    padding: 5px;
                    spacing: 8px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
                QProgressBar {
                    border: none;
                    border-radius: 7px;
                    text-align: center;
                    font-size: 12px;
                    font-weight: bold;
                    background-color: #e0e0e0;
                }
                QProgressBar::chunk {
                    background-color: #2d5a7c;
                    border-radius: 7px;
                }
                QLabel {
                    font-size: 14px;
                    font-weight: bold;
                }
            """)

    def get_output_format(self):
        return "DOCX" if self.docx_radio.isChecked() else "TXT"

    def open_output_folder(self):
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "arquivos_convertidos")
        os.makedirs(output_dir, exist_ok=True)
        
        if sys.platform == 'win32':
            os.startfile(output_dir)
        elif sys.platform == 'darwin':  # macOS
            subprocess.run(['open', output_dir])
        else:  # linux
            subprocess.run(['xdg-open', output_dir])

    def handle_dropped_files(self, files):
        self.selected_files = files
        self.convert_button.setEnabled(True)
        self.drop_area.label.setText(f"{len(files)} arquivo(s) selecionado(s)")

    def start_conversion(self):
        if not self.selected_files:
            return

        # Desabilita botões durante a conversão
        self.convert_button.setEnabled(False)
        self.drop_area.setAcceptDrops(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        # Configura e inicia a thread de conversão
        output_format = "DOCX" if self.docx_radio.isChecked() else "TXT"
        self.converter_thread = PDFConverterThread(
            self.selected_files,
            output_format,
            self.ocr_checkbox.isChecked()
        )
        self.converter_thread.progress.connect(self.update_progress)
        self.converter_thread.finished.connect(self.conversion_finished)
        self.converter_thread.error.connect(self.show_error)
        self.converter_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def conversion_finished(self):
        self.progress_bar.setVisible(False)
        self.convert_button.setEnabled(True)
        self.drop_area.setAcceptDrops(True)
        self.drop_area.label.setText("Arraste arquivos PDF aqui ou clique para selecionar")
        self.selected_files = []
        
        QMessageBox.information(
            self,
            "Sucesso",
            "Conversão concluída com sucesso!"
        )

    def show_error(self, message):
        self.progress_bar.setVisible(False)
        self.convert_button.setEnabled(True)
        self.drop_area.setAcceptDrops(True)
        
        QMessageBox.critical(
            self,
            "Erro",
            f"Erro durante a conversão: {message}"
        )

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 