"""
Feuilles de style QSS pour l'application.
Thème moderne et professionnel.
"""

MAIN_STYLE = """
/* === Palette de couleurs === */
QMainWindow {
    background-color: #f0f2f5;
}

/* === Barre latérale === */
#sidebar {
    background-color: #1e293b;
    min-width: 220px;
    max-width: 220px;
}

#sidebar QPushButton {
    background-color: transparent;
    color: #94a3b8;
    border: none;
    text-align: left;
    padding: 14px 20px;
    font-size: 14px;
    font-weight: 500;
    border-left: 3px solid transparent;
}

#sidebar QPushButton:hover {
    background-color: #334155;
    color: #e2e8f0;
}

#sidebar QPushButton:checked,
#sidebar QPushButton[active="true"] {
    background-color: #334155;
    color: #ffffff;
    border-left: 3px solid #3b82f6;
    font-weight: 600;
}

#sidebar_title {
    color: #ffffff;
    font-size: 18px;
    font-weight: 700;
    padding: 20px;
}

/* === En-tête de page === */
#page_header {
    font-size: 22px;
    font-weight: 700;
    color: #1e293b;
    padding: 10px 0;
}

/* === Cartes statistiques === */
.stat-card {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 20px;
    border: 1px solid #e2e8f0;
}

/* === Tableau === */
QTableWidget {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    gridline-color: #f1f5f9;
    font-size: 13px;
    selection-background-color: #dbeafe;
    selection-color: #1e293b;
}

QTableWidget::item {
    padding: 8px 12px;
}

QHeaderView::section {
    background-color: #f8fafc;
    color: #475569;
    font-weight: 600;
    font-size: 12px;
    text-transform: uppercase;
    padding: 10px 12px;
    border: none;
    border-bottom: 2px solid #e2e8f0;
}

/* === Boutons === */
QPushButton {
    background-color: #3b82f6;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #2563eb;
}

QPushButton:pressed {
    background-color: #1d4ed8;
}

QPushButton#btn_danger {
    background-color: #ef4444;
}

QPushButton#btn_danger:hover {
    background-color: #dc2626;
}

QPushButton#btn_secondary {
    background-color: #64748b;
}

QPushButton#btn_secondary:hover {
    background-color: #475569;
}

QPushButton#btn_success {
    background-color: #22c55e;
}

/* === Champs de saisie === */
QLineEdit, QComboBox, QDateEdit, QTextEdit {
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 13px;
    background-color: #ffffff;
    color: #1e293b;
}

QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTextEdit:focus {
    border: 2px solid #3b82f6;
    outline: none;
}

QComboBox::drop-down {
    border: none;
    width: 30px;
}

/* === Labels === */
QLabel {
    color: #334155;
    font-size: 13px;
}

/* === GroupBox === */
QGroupBox {
    font-weight: 600;
    font-size: 14px;
    color: #1e293b;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 16px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    padding: 0 8px;
}

/* === Barre de recherche === */
#search_bar {
    border: 1px solid #cbd5e1;
    border-radius: 20px;
    padding: 10px 18px;
    font-size: 13px;
    min-width: 300px;
}

/* === Dialog === */
QDialog {
    background-color: #ffffff;
}

/* === Scrollbar === */
QScrollBar:vertical {
    width: 8px;
    background: #f1f5f9;
}

QScrollBar::handle:vertical {
    background: #94a3b8;
    border-radius: 4px;
    min-height: 40px;
}

/* === Statut badges === */
QLabel#status_actif { color: #16a34a; font-weight: 600; }
QLabel#status_maintenance { color: #ea580c; font-weight: 600; }
QLabel#status_en_panne { color: #dc2626; font-weight: 600; }
"""

DARK_STYLE = """
QMainWindow { background-color: #0f172a; }
#sidebar { background-color: #020617; }
QTableWidget { background-color: #1e293b; color: #e2e8f0; border-color: #334155; gridline-color: #334155; }
QHeaderView::section { background-color: #0f172a; color: #94a3b8; border-bottom-color: #334155; }
QLineEdit, QComboBox, QDateEdit, QTextEdit { background-color: #1e293b; color: #e2e8f0; border-color: #475569; }
QLabel { color: #e2e8f0; }
QDialog { background-color: #1e293b; }
QGroupBox { color: #e2e8f0; border-color: #334155; }
"""
