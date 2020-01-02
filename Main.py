import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import clipboard

import Mailtemplates


class TemplateGUI(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.x = 800
        self.y = 600

        self.setWindowTitle("Templates")
        self.setFixedSize(self.x, self.y)
        self.db = Mailtemplates.Templates("Mail.db")
        
        self.current_template = ""
        self.lb_status = QLabel(self)
        self.lb_status.setGeometry(QRect(15, self.y-35, self.x - 30, 25))

        self.initUI()

    def initUI(self):
        # Menüpunkte
        action_new_template = QAction("&Neues Template", self)
        action_new_template.setStatusTip("Erstelle ein neues Template")
        action_new_template.triggered.connect(self.show_new_template_UI)

        action_edit_template = QAction("&Template bearbeiten", self)
        action_edit_template.setStatusTip("Bearbeite ein Template")
        action_edit_template.triggered.connect(self.edit_template_dialog)

        action_delete_template = QAction("&Lösche Template", self)
        action_delete_template.setStatusTip("Lösche ein Template")
        action_delete_template.triggered.connect(self.delete_template_dialog)

        action_copy_template = QAction("&Kopiere Template", self)
        action_copy_template.setStatusTip("Kopiere ein Template")
        action_copy_template.triggered.connect(self.copy_template_dialog)

        self.statusBar()

        mainMenu = self.menuBar()
        menu = mainMenu.addMenu("&Menü")
        menu.addAction(action_new_template)
        menu.addAction(action_edit_template)
        menu.addAction(action_delete_template)
        menu.addAction(action_copy_template)

        # Alle UIs werden initialisiert
        self.home()
        self.new_template_UI()
        self.edit_template_UI()
        self.copy_template_UI()
    
    def home(self):
        self.gb_home = QGroupBox("Home", self)
        self.gb_home.setGeometry(QRect(10, 30, self.x-20, self.y-40))

    def new_template_UI(self):
        # Groupbox erstellt, in der alle Widgets für das new_template_UI geplaced werden
        self.gb_new_template = QGroupBox("Neues Template", self)
        self.gb_new_template.setGeometry(QRect(10, 30, self.x-20, self.y-40))
        # Nicht sichtbar
        self.gb_new_template.setHidden(True)
        
        self.lb_subject = QLabel("Beschreibung", self.gb_new_template)
        self.lb_subject.setGeometry(QRect(10, 20, 80, 25))

        self.lb_attributes = QLabel("Attribute", self.gb_new_template)
        self.lb_attributes.setGeometry(QRect(10, 50, 80, 25))

        self.lb_message = QLabel("Nachricht", self.gb_new_template)
        self.lb_message.setGeometry(QRect(10, 80, 80, 25))

        self.le_new_subject = QLineEdit(self.gb_new_template)
        self.le_new_subject.setGeometry(QRect(120, 20, 600, 25))

        self.attribute = ["a", "d", "p"]
        x = 120
        for att in self.attribute:
            self.cb_new_attributes = QCheckBox(att, self.gb_new_template)
            self.cb_new_attributes.setObjectName("checkbox_new_{}".format(att))
            self.cb_new_attributes.setGeometry(QRect(x, 50, 50, 25))
            x += 50

        self.te_new_message = QTextEdit(self.gb_new_template)
        self.te_new_message.setGeometry(QRect(120, 80, 600, 400))

        self.btn_new_save = QPushButton("Speichern", self.gb_new_template)
        self.btn_new_save.setGeometry(QRect(self.x-100, self.y-65, 80, 25))
        self.btn_new_save.clicked.connect(self.save_new_template)

    def edit_template_UI(self):
        
        self.gb_edit_template = QGroupBox("Template bearbeiten", self)
        self.gb_edit_template.setGeometry(QRect(10, 30, self.x-20, self.y-40))
        self.gb_edit_template.setHidden(True)

        self.lb_subject = QLabel("Beschreibung", self.gb_edit_template)
        self.lb_subject.setGeometry(QRect(10, 20, 80, 25))

        self.lb_attributes = QLabel("Attribute", self.gb_edit_template)
        self.lb_attributes.setGeometry(QRect(10, 50, 80, 25))

        self.lb_message = QLabel("Nachricht", self.gb_edit_template)
        self.lb_message.setGeometry(QRect(10, 80, 80, 25))

        self.le_edit_subject = QLineEdit(self.gb_edit_template)
        self.le_edit_subject.setGeometry(QRect(120, 20, 600, 25))

        self.attribute = ["a", "d", "p"]
        x = 120
        for att in self.attribute:
            self.cb_edit_attributes = QCheckBox(att, self.gb_edit_template)
            self.cb_edit_attributes.setObjectName("checkbox_edit_{}".format(att))
            self.cb_edit_attributes.setGeometry(QRect(x, 50, 50, 25))
            x += 50
        
        self.te_edit_message = QTextEdit(self.gb_edit_template)
        self.te_edit_message.setGeometry(QRect(120, 80, 600, 400))

        self.btn_edit_save = QPushButton("Speichern", self.gb_edit_template)
        self.btn_edit_save.setGeometry(QRect(self.x-100, self.y-65, 80, 25))

        self.btn_edit_save.clicked.connect(self.save_edit_template)

    def copy_template_UI(self):
        self.gb_copy_template = QGroupBox(f"Template kopieren", self)
        self.gb_copy_template.setGeometry(QRect(10, 30, self.x-20, self.y-40))
        self.gb_copy_template.setHidden(True)

        self.lb_chosen_template = QLabel(self.gb_copy_template)
        self.lb_chosen_template.setGeometry(QRect(10, 20, 400, 40))
        self.lb_chosen_template.setStyleSheet("color: green; font: bold 15px;")

        self.rb_anrede_herr = QRadioButton("Herr", self.gb_copy_template)
        self.rb_anrede_herr.setGeometry(QRect(10, 60, 80, 25))

        self.rb_anrede_frau = QRadioButton("Frau", self.gb_copy_template)
        self.rb_anrede_frau.setGeometry(QRect(100, 60, 80, 25))

        self.le_name = QLineEdit(self.gb_copy_template)
        self.le_name.setGeometry(QRect(10, 90, 200, 25))

        self.de_date = QDateEdit(self.gb_copy_template)
        self.de_date.setGeometry(QRect(10, 150, 100, 25))
        self.de_date.setDateTime(QDateTime.currentDateTime())
        self.de_date.setCalendarPopup(True)

        self.lb_price = QLabel("Preis in €", self.gb_copy_template)
        self.lb_price.setGeometry(QRect(10, 200, 200, 25))

        self.le_price = QLineEdit(self.gb_copy_template)
        self.le_price.setGeometry(QRect(10, 225, 100, 25))

        self.btn_copy = QPushButton("Kopieren", self.gb_copy_template)
        self.btn_copy.setGeometry(QRect(10, self.y-100, 80, 25))

        self.lb_current_text = QLabel("Aktuelle Vorlage:", self.gb_copy_template)
        self.lb_current_text.setGeometry(QRect((self.x-20)/2-30, 15, 200, 25))
        self.lb_current_text.setStyleSheet("color: green; font: bold 15px;")

        self.te_current_text = QTextEdit(self.gb_copy_template)
        self.te_current_text.setGeometry(QRect((self.x-20)/2-30, 40, (self.x-20)/2, self.y-100))
        self.te_current_text.setReadOnly(True)

        self.btn_copy.clicked.connect(self.copy)

    def save_new_template(self):
        # Methode, wenn auf den Speichern-Button geklickt wird (bei Erstellung eines neuen Templates)
        self.lb_status.clear()

        # Überprüfung, ob bereits ein Datensatz in der Datenbank mit dem gleichen Subject vorhanden ist
        if self.le_new_subject.text() in self.db.get_templates_subjects():
            self.lb_status.setStyleSheet("color: red")
            self.lb_status.setText("Template Beschreibung existiert bereits")
        else:
            if self.le_new_subject.text() == "":
                self.lb_status.setStyleSheet("color: red")
                self.lb_status.setText("Subject nicht ausgefüllt")
                return

            # Überprüfung, ob die Checkboxen (für die Attribute) angecheckt sind.
            checked_attributes = []
            for att in self.attribute:
                if self.findChild(QCheckBox, "checkbox_new_{}".format(att)).isChecked():
                    checked_attributes.append(self.findChild(QCheckBox, "checkbox_new_{}".format(att)).text())

            if len(checked_attributes) == 0:
                self.lb_status.setStyleSheet("color: red")
                self.lb_status.setText("Keine Attribute ausgefüllt")
                return

            if self.te_new_message.toPlainText() == "":
                self.lb_status.setStyleSheet("color: red")
                self.lb_status.setText("Message ist nicht ausgefüllt")
                return 

            # Es wird gecheckt, ob die angecheckten Attribute auch mit dem Format {attribut} im Text auftaucht
            for attribute in checked_attributes:
                if not "{" + attribute + "}" in self.te_new_message.toPlainText():
                    self.lb_status.setStyleSheet("color: red")
                    self.lb_status.setText(attribute + " ist im Nachrichtentext nicht vorhanden. Layout: {Attribut}")
                    return

            # Wenn alle Prüfungen i. O. sind, werden die Daten in die Datenbank geschrieben und alle Felder resettet
            self.db.new_template(self.le_new_subject.text(), "".join(checked_attributes), self.te_new_message.toPlainText())
            self.le_new_subject.clear()
            for att in self.attribute:
                self.findChild(QCheckBox, "checkbox_new_{}".format(att)).setChecked(False)
            self.te_new_message.clear()
            self.lb_status.setStyleSheet("color: green")
            self.lb_status.setText("Template gespeichert")

    def save_edit_template(self):
        # Methode, wenn auf den Speichern-Button geklickt wird (bei Bearbeitung eines Templates)
        self.lb_status.clear()
        
        if not self.current_template == self.le_edit_subject.text():
            if self.le_edit_subject.text() in self.db.get_templates_subjects():
                self.lb_status.setStyleSheet("color: red")
                self.lb_status.setText("Template Beschreibung existiert bereits")
                return

            else:
                if self.le_edit_subject.text() == "":
                    self.lb_status.setStyleSheet("color: red")
                    self.lb_status.setText("Subject nicht ausgefüllt")
                    return
                
                checked_attributes = []
                for att in self.attribute:
                    if self.findChild(QCheckBox, "checkbox_edit_{}".format(att)).isChecked():
                        checked_attributes.append(self.findChild(QCheckBox, "checkbox_edit_{}".format(att)).text())

                if len(checked_attributes) == 0:
                    self.lb_status.setStyleSheet("color: red")
                    self.lb_status.setText("Keine Attribute ausgefüllt")
                    return
                
                if self.te_edit_message.toPlainText() == "":
                    self.lb_status.setStyleSheet("color: red")
                    self.lb_status.setText("Message ist nicht ausgefüllt")
                    return
                
                for attribute in checked_attributes:
                    if not "{" + attribute + "}" in self.te_edit_message.toPlainText():
                        self.lb_status.setStyleSheet("color: red")
                        self.lb_status.setText(attribute + " ist im Nachrichtentext nicht vorhanden. Layout: {Attribut}")
                        return
                
                self.db.change_templates_attributes("".join(checked_attributes), self.current_template)
                self.db.change_templates_message(self.current_template, self.te_edit_message.toPlainText())

                self.db.change_templates_subject(self.current_template, self.le_edit_subject.text())
                self.current_template = self.le_edit_subject.text()
                self.lb_status.setStyleSheet("color: green")
                self.lb_status.setText("Template-Änderungen gespeichert")

        else:
            if self.le_edit_subject.text() == "":
                self.lb_status.setStyleSheet("color: red")
                self.lb_status.setText("Subject nicht ausgefüllt")
                return
            
            checked_attributes = []
            for att in self.attribute:
                if self.findChild(QCheckBox, "checkbox_edit_{}".format(att)).isChecked():
                    checked_attributes.append(self.findChild(QCheckBox,"checkbox_edit_{}".format(att)).text())
            
            if len(checked_attributes) == 0:
                self.lb_status.setStyleSheet("color: red")
                self.lb_status.setText("Keine Attribute ausgefüllt")
                return

            if self.te_edit_message.toPlainText() == "":
                self.lb_status.setStyleSheet("color: red")
                self.lb_status.setText("Message ist nicht ausgefüllt")
                return 

            for attribute in checked_attributes:
                if not "{" + attribute + "}" in self.te_edit_message.toPlainText():
                    self.lb_status.setStyleSheet("color: red")
                    self.lb_status.setText(attribute + " ist im Nachrichtentext nicht vorhanden. Layout: {Attribut}")
                    return

            self.db.change_templates_attributes("".join(checked_attributes), self.current_template)
            self.db.change_templates_message(self.current_template, self.te_edit_message.toPlainText())
            
            self.lb_status.setStyleSheet("color: green")
            self.lb_status.setText("Template-Änderungen gespeichert")
        
    def edit_template_dialog(self):
        # Wenn der Menüpunkt "Template bearbeiten" geklickt wird
        try:
            # Falls bereits ein bestehendes Dialogfenster vorhanden, wird dieses vorerst geschlossen
            self.dialog.close()
        except:
            pass
        
        # Initialisierung Widgets
        self.lb_status.clear()

        self.gb_edit_template.setHidden(True)
        self.gb_new_template.setHidden(True)
        self.gb_copy_template.setHidden(True)

        self.gb_home.setHidden(False)


        self.current_template = ""

        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Template zum Editieren wählen")
        self.dialog.setFixedSize(300, 300)
        
        self.lb_templates = QLabel("Bitte Template auswählen (Doppelklick)", self.dialog)
        self.lb_templates.setGeometry(QRect(10, 0, 300, 25))
        self.lw_templates = QListWidget(self.dialog)
        self.lw_templates.setGeometry(QRect(0, 30, 300, 270))

        for subject in self.db.get_templates_subjects():
            self.lw_templates.addItem(subject)
        
        self.lw_templates.itemDoubleClicked.connect(self.show_edit_template_UI)

        self.dialog.show()
    
    def delete_template_dialog(self):
        try:
            self.dialog.close()
        except:
            pass

        self.lb_status.clear()

        self.gb_edit_template.setHidden(True)
        self.gb_new_template.setHidden(True)
        self.gb_copy_template.setHidden(True)

        self.gb_home.setHidden(False)

        self.current_template = ""

        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Template zum Löschen wählen")
        self.dialog.setFixedSize(300, 300)

        self.lb_templates = QLabel("Template markieren und auf den Button 'Löschen' klicken", self.dialog)
        self.lb_templates.setGeometry(QRect(10, 0, 300, 25))
        self.lw_templates = QListWidget(self.dialog)
        self.lw_templates.setGeometry(QRect(0, 30, 300, 225))
        
        self.btn_delete_template = QPushButton("Löschen", self.dialog)
        self.btn_delete_template.setGeometry(QRect(100, 275, 100, 25))

        for subject in self.db.get_templates_subjects():
            self.lw_templates.addItem(subject)

        self.btn_delete_template.clicked.connect(self.delete_template)

        self.dialog.show()

    def copy_template_dialog(self):
        try:
            self.dialog.close()
        except:
            pass

        self.lb_status.clear()

        self.gb_edit_template.setHidden(True)
        self.gb_new_template.setHidden(True)
        self.gb_copy_template.setHidden(True)

        self.gb_home.setHidden(False)

        self.current_template = ""

        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Template zum Kopieren wählen")
        self.dialog.setFixedSize(300, 300)

        
        self.lb_templates = QLabel("Bitte Template auswählen (Doppelklick)", self.dialog)
        self.lb_templates.setGeometry(QRect(10, 0, 300, 25))
        self.lw_templates = QListWidget(self.dialog)
        self.lw_templates.setGeometry(QRect(0, 30, 300, 270))

        for subject in self.db.get_templates_subjects():
            self.lw_templates.addItem(subject)
        
        self.lw_templates.itemDoubleClicked.connect(self.show_copy_template_UI)

        self.dialog.show()

    def delete_template(self):
        self.lb_status.clear()

        self.current_template = self.lw_templates.currentItem().text()
        self.db.delete_template(self.current_template)

        self.dialog.close()
        self.lb_status.setStyleSheet("color: green")
        self.lb_status.setText(self.current_template + "-Template wurde gelöscht")

    def show_new_template_UI(self):
        try:
            self.dialog.close()
        except:
            pass

        self.lb_status.clear()

        self.gb_home.setHidden(True)
        self.gb_edit_template.setHidden(True)        
        self.gb_copy_template.setHidden(True)

        self.gb_new_template.setHidden(False)

        self.le_new_subject.clear()
        self.te_new_message.clear()

    def show_edit_template_UI(self):
        self.lb_status.clear()

        self.gb_home.setHidden(True)
        self.gb_new_template.setHidden(True)
        self.gb_copy_template.setHidden(True)

        self.gb_edit_template.setHidden(False)

        self.current_template = self.lw_templates.currentItem().text()
        self.dialog.close()

        attribute = self.db.get_attributes_from_subject(self.current_template)
        message = self.db.get_templates_message(self.current_template)

        self.le_edit_subject.setText(self.current_template)
        for attribut in attribute:
            self.findChild(QCheckBox, "checkbox_edit_{}".format(attribut)).setChecked(True)

        self.te_edit_message.setText(message)
    
    def show_copy_template_UI(self):
        self.lb_status.clear()

        self.gb_home.setHidden(True)
        self.gb_new_template.setHidden(True)
        self.gb_edit_template.setHidden(True)
        
        self.gb_copy_template.setHidden(False)

        self.current_template = self.lw_templates.currentItem().text()
        self.dialog.close()
        
        self.le_price.clear()
        self.de_date.setDateTime(QDateTime.currentDateTime())
        self.le_name.clear()
        self.rb_anrede_herr.setChecked(True)

        attributes = ("a", "d", "p")
        for a in attributes:
            self.findChild(QCheckBox, "checkbox_edit_{}".format(a)).setChecked(False)

        self.lb_chosen_template.setText(f"{self.current_template}")

        if "a" in self.db.get_attributes_from_subject(self.current_template):
            self.rb_anrede_frau.setDisabled(False)
            self.rb_anrede_herr.setDisabled(False)
            self.le_name.setDisabled(False)
        else:
            self.rb_anrede_frau.setDisabled(True)
            self.rb_anrede_herr.setDisabled(True)
            self.le_name.setDisabled(True)
        
        if "p" in self.db.get_attributes_from_subject(self.current_template):
            self.le_price.setDisabled(False)
        else:
            self.le_price.setDisabled(True)
        
        if "d" in self.db.get_attributes_from_subject(self.current_template):
            self.de_date.setDisabled(False)                
        else:
            self.de_date.setDisabled(True)
        
        self.sex = "geehrter " + self.rb_anrede_herr.text()
        self.name = ""
        self.anrede = self.sex + self.name
        self.datum = self.de_date.date().toPyDate().strftime("%d.%m.%Y")
        self.preis = ""
        
        self.show_current_text = self.db.get_templates_message(self.current_template).replace("{a}", self.anrede).replace("{d}", self.datum).replace("{p}", self.preis)

        self.te_current_text.setText(self.show_current_text)

        
        self.rb_anrede_frau.toggled.connect(self.rb_change)
        self.rb_anrede_herr.toggled.connect(self.rb_change)
        self.le_name.textChanged.connect(self.le_name_change)
        self.de_date.dateChanged.connect(self.de_date_change)
        self.le_price.textChanged.connect(self.le_preis_change)

    def rb_change(self):
        self.sex = ""
        

        if self.rb_anrede_frau.isChecked():
            self.sex += "geehrte Frau "
        elif self.rb_anrede_herr.isChecked():
            self.sex += "geehrter Herr "


        self.anrede = self.sex + self.name

        self.show_current_text = self.db.get_templates_message(self.current_template).replace("{a}", self.anrede).replace("{d}", self.datum).replace("{p}", self.preis)

        self.te_current_text.setText(self.show_current_text)
    
    def le_name_change(self):
        self.name = self.le_name.text()
        self.anrede = self.sex + self.name

        self.show_current_text = self.db.get_templates_message(self.current_template).replace("{a}", self.anrede).replace("{d}", self.datum).replace("{p}", self.preis)

        self.te_current_text.setText(self.show_current_text)

    def de_date_change(self):
        self.datum = self.de_date.date().toPyDate().strftime("%d.%m.%Y")

        self.show_current_text = self.db.get_templates_message(self.current_template).replace("{a}", self.anrede).replace("{d}", self.datum).replace("{p}", self.preis)

        self.te_current_text.setText(self.show_current_text)
    
    def le_preis_change(self):
        self.preis = self.le_price.text()

        self.show_current_text = self.db.get_templates_message(self.current_template).replace("{a}", self.anrede).replace("{d}", self.datum).replace("{p}", self.preis)

        self.te_current_text.setText(self.show_current_text)

    def copy(self):
        clipboard.copy(self.show_current_text)
        self.lb_status.setStyleSheet("color: green")
        self.lb_status.setText("Text kopiert")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = TemplateGUI()
    clock.show()
    sys.exit(app.exec_())
