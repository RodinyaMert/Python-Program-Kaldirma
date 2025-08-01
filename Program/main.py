from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton,
    QLabel, QMessageBox, QTextEdit, QTabWidget
)
from PyQt5.QtCore import Qt
import subprocess
import sys

from uninstall_utils import get_installed_apps

class Tab1_ListOnly(QWidget):
    def __init__(self, apps):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Yüklü Programlar (Sadece Liste)")
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName("headerLabel")
        layout.addWidget(label)

        self.list_widget = QListWidget()
        for app in apps:
            self.list_widget.addItem(app[0])
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

class Tab2_Uninstall(QWidget):
    def __init__(self, apps):
        super().__init__()
        self.apps = apps
        layout = QVBoxLayout()

        label = QLabel("Program Seçip Kaldır")
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName("headerLabel")
        layout.addWidget(label)

        self.list_widget = QListWidget()
        for app in apps:
            self.list_widget.addItem(app[0])
        layout.addWidget(self.list_widget)

        self.uninstall_btn = QPushButton("Kaldır")
        self.uninstall_btn.clicked.connect(self.uninstall_selected)
        layout.addWidget(self.uninstall_btn)

        self.setLayout(layout)

    def uninstall_selected(self):
        index = self.list_widget.currentRow()
        if index < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen kaldırmak için bir program seçin!")
            return

        app_name, uninstall_cmd = self.apps[index]

        reply = QMessageBox.question(
            self, "Kaldırmayı Onayla",
            f"\"{app_name}\" uygulamasını kaldırmak istediğine emin misin?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                subprocess.Popen(uninstall_cmd, shell=True)
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Kaldırma işlemi başarısız oldu:\n{str(e)}")

class Tab3_Info(QWidget):
    def __init__(self, apps):
        super().__init__()
        self.apps = apps
        layout = QVBoxLayout()

        label = QLabel("Program Bilgileri")
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName("headerLabel")
        layout.addWidget(label)

        self.list_widget = QListWidget()
        self.list_widget.currentRowChanged.connect(self.show_details)
        for app in apps:
            self.list_widget.addItem(app[0])
        layout.addWidget(self.list_widget)

        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        layout.addWidget(self.details_text)

        self.setLayout(layout)

    def show_details(self, index):
        if index < 0:
            self.details_text.clear()
            return
        app_name, uninstall_cmd = self.apps[index]
        detail_text = f"Program Adı: {app_name}\n\nKaldırma Komutu:\n{uninstall_cmd}"
        self.details_text.setPlainText(detail_text)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Program Kaldırıcı - Modern Sekmeli Arayüz")
        self.setGeometry(300, 150, 850, 600)

        self.apps = get_installed_apps()

        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.tabs.addTab(Tab1_ListOnly(self.apps), "Uygulamalar")
        self.tabs.addTab(Tab2_Uninstall(self.apps), "Kaldır")
        self.tabs.addTab(Tab3_Info(self.apps), "Bilgi")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #181818;
                color: #e0e0e0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QTabWidget::pane {
                border-top: 2px solid #3a86ff;
            }
            QTabBar::tab {
                background: #2a2a2a;
                color: #ccc;
                min-width: 110px;
                min-height: 40px;
                margin-right: 5px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                padding: 10px 15px;
                font-weight: 600;
                transition: all 0.3s;
            }
            QTabBar::tab:selected {
                background: #3a86ff;
                color: white;
                font-weight: 700;
            }
            QTabBar::tab:hover {
                background: #5aa3ff;
                color: white;
            }
            QListWidget {
                background-color: #2c2c3e;
                border-radius: 10px;
                padding: 10px;
                font-size: 14pt;
            }
            QListWidget::item {
                padding: 12px 15px;
                border-radius: 8px;
                margin-bottom: 6px;
                color: #ddd;
            }
            QListWidget::item:hover {
                background-color: #5aa3ff;
                color: white;
            }
            QListWidget::item:selected {
                background-color: #3a86ff;
                color: white;
                font-weight: bold;
            }
            QPushButton {
                background-color: #3a86ff;
                border: none;
                border-radius: 14px;
                color: white;
                font-size: 16pt;
                font-weight: 700;
                padding: 14px 60px;
                margin-top: 20px;
                box-shadow: 0 5px 15px rgba(58, 134, 255, 0.7);
                transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: #5aa3ff;
                cursor: pointer;
                box-shadow: 0 7px 20px rgba(90, 163, 255, 0.9);
            }
            QLabel#headerLabel {
                font-size: 22px;
                font-weight: 700;
                margin-bottom: 15px;
            }
            QTextEdit {
                background-color: #2c2c3e;
                border-radius: 10px;
                padding: 12px;
                font-size: 13pt;
                color: #ddd;
            }
        """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
