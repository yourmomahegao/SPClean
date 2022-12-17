from PyQt5 import QtGui


# --- INIT CODE (USING IN INTERFACE MANUALLY) --- #
# from font_init import init_fonts
# init_fonts()
# ----------------------------------------------- #

# Initing fonts from resources
def init_fonts():
    QtGui.QFontDatabase.addApplicationFont(":/fonts/fonts/Ermilov-bold.otf")
