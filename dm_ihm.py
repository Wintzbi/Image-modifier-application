import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QToolBar, QAction, QStatusBar, QVBoxLayout, QWidget, QFileDialog, QHBoxLayout, QSlider
from PyQt5.QtCore import Qt, QCoreApplication, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QKeySequence, QPixmap, QImage
from PIL import Image

class Fenetre(QMainWindow):
    color_values_signal = pyqtSignal(int, int, int)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Générateur de couleurs")
        self.setGeometry(100, 100, 500, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        self.label = QLabel()
        main_layout.addWidget(self.label)
        
        sliders_layout = QHBoxLayout()
        main_layout.addLayout(sliders_layout)
        
        self.slider_red = QSlider(Qt.Horizontal)
        self.slider_red.setMinimum(0)
        self.slider_red.setMaximum(255)
        self.slider_red.valueChanged.connect(self.update_color)
        sliders_layout.addWidget(self.slider_red)
        
        self.red_label = QLabel("Rouge")
        self.red_label.setStyleSheet("color: red;")
        sliders_layout.addWidget(self.red_label)
        
        self.slider_green = QSlider(Qt.Horizontal)
        self.slider_green.setMinimum(0)
        self.slider_green.setMaximum(255)
        self.slider_green.valueChanged.connect(self.update_color)
        sliders_layout.addWidget(self.slider_green)
        
        self.green_label = QLabel("Vert")
        self.green_label.setStyleSheet("color: green;")
        sliders_layout.addWidget(self.green_label)
        
        self.slider_blue = QSlider(Qt.Horizontal)
        self.slider_blue.setMinimum(0)
        self.slider_blue.setMaximum(255)
        self.slider_blue.valueChanged.connect(self.update_color)
        sliders_layout.addWidget(self.slider_blue)
        
        self.blue_label = QLabel("Bleu")
        self.blue_label.setStyleSheet("color: blue;")
        sliders_layout.addWidget(self.blue_label)
        
        self.update_color()

    def update_color(self):
        red = self.slider_red.value()
        green = self.slider_green.value()
        blue = self.slider_blue.value()
        color_hex = "#{:02x}{:02x}{:02x}".format(red, green, blue)
        self.label.setText(f"R: {red}, G: {green}, B: {blue}")
        self.label.setStyleSheet("background-color: " + color_hex)

        self.red_label.setText(str(red))
        self.green_label.setText(str(green))
        self.blue_label.setText(str(blue))

        self.color_values_signal.emit(red, green, blue)


class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Générateur d'image")
        self.setGeometry(100, 200, 700, 300)

        self.color_window = Fenetre()
        self.color_window.color_values_signal.connect(self.onColorValuesReceived)

        self.image_file = "singe.jpg"
        self.image = Image.open(self.image_file).convert(mode='RGB')
        self.image_width, self.image_height = self.image.size

        self.image_original = self.image.copy()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.textLabel = QLabel(f'{self.image_width} X {self.image_height}')
        layout.addWidget(self.textLabel)

        self.update_image()

        self.button_reset = QAction(QIcon("animal-penguin.png"),"Réinitialiser", self)
        self.button_reset.triggered.connect(self.onReset)
        self.button_reset.setShortcut(QKeySequence('Ctrl+D'))

        self.button_open = QAction(QIcon("folder-open-feed.png"),"Ouvrir", self)
        self.button_open.triggered.connect(self.onOpen)
        self.button_open.setShortcut(QKeySequence('Ctrl+O'))

        self.button_r = QAction(QIcon("android_rouge.png"),"Filtre rouge", self)
        self.button_r.triggered.connect(self.onFilterR)
        self.button_r.setShortcut(QKeySequence('Ctrl+R'))

        self.button_v = QAction(QIcon("android_vert.png"),"Filtre vert", self)
        self.button_v.triggered.connect(self.onFilterV)
        self.button_v.setShortcut(QKeySequence('Ctrl+V'))

        self.button_b = QAction(QIcon("android_bleu.png"),"Filtre bleu", self)
        self.button_b.triggered.connect(self.onFilterB)
        self.button_b.setShortcut(QKeySequence('Ctrl+B'))

        self.button_negatif = QAction(QIcon("android_noiretblanc.png"),"Négatif", self)
        self.button_negatif.triggered.connect(self.onNega)
        self.button_negatif.setShortcut(QKeySequence('Ctrl+N'))

        self.button_g = QAction(QIcon("android_gris.png"),"Filtre Gris", self)
        self.button_g.triggered.connect(self.onFilterG)
        self.button_g.setShortcut(QKeySequence('Ctrl+G'))

        self.button_p4 = QAction(QIcon("application-tile.png"),"Par 4", self)
        self.button_p4.triggered.connect(self.onPhoto4)
        self.button_p4.setShortcut(QKeySequence('Ctrl+P'))

        self.button_couleur = QAction(QIcon("android_blanc.png"),"Générateur de couleurs", self)
        self.button_couleur.triggered.connect(self.onGenerateur)
        self.button_couleur.setShortcut(QKeySequence('Ctrl+C'))

        self.button_quit = QAction(QIcon("bomb.png"),"Quitter",self)
        self.button_quit.triggered.connect(self.onQuit)
        self.button_quit.setShortcut(QKeySequence('Ctrl+Q'))

        self.setStatusBar(QStatusBar())
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)
        self.toolbar.setIconSize(QSize(16,16))

        menuBar = self.menuBar()
        self.image_fileMenu = menuBar.addMenu("&Image")
        self.image_fileMenu.addAction(self.button_reset)
        self.image_fileMenu.addAction(self.button_open)
        self.toolbar.addAction(self.button_reset)
        self.toolbar.addAction(self.button_open)

        self.filtre_fileMenu = menuBar.addMenu("&Filtre")
        self.filtre_fileMenu.addAction(self.button_r)
        self.filtre_fileMenu.addAction(self.button_v)
        self.filtre_fileMenu.addAction(self.button_b)
        self.filtre_fileMenu.addSeparator()
        self.filtre_fileMenu.addAction(self.button_negatif)
        self.filtre_fileMenu.addAction(self.button_g)
        self.toolbar.addAction(self.button_r)
        self.toolbar.addAction(self.button_v)
        self.toolbar.addAction(self.button_b)
        self.toolbar.addAction(self.button_negatif)
        self.toolbar.addAction(self.button_g)

        self.photomaton_fileMenu = menuBar.addMenu("&Photomaton")
        self.photomaton_fileMenu.addAction(self.button_p4)
        self.toolbar.addAction(self.button_p4)

        self.couleur_fileMenu = menuBar.addMenu("&Couleur")
        self.couleur_fileMenu.addAction(self.button_couleur)
        self.toolbar.addAction(self.button_couleur)

        self.quitter_fileMenu = menuBar.addMenu("&Quitter")
        self.quitter_fileMenu.addAction(self.button_quit)
        self.toolbar.addAction(self.button_quit)

    def onOpen(self):
        file_path,_ = QFileDialog.getOpenFileName(self, "", "", "Images (*.jpg *.jpeg *.png *.bmp *.gif)")
        if file_path:
            self.image = Image.open(file_path).convert("RGB")
            piximage = QPixmap(file_path)
            self.label.setPixmap(QPixmap(file_path))
            self.resize(piximage.width(), piximage.height())
            self.image_original = self.image.copy()
            self.image_width, self.image_height = self.image.size
            self.textLabel.setText(f'{self.image_width} X {self.image_height}')
            
    def onReset(self):
        self.image = self.image_original.copy()
        self.update_image()

    def onFilterR(self):
        self.image = self.image_original.copy()
        self.colorFilter("rouge")
        self.update_image()

    def onFilterV(self):
        self.image = self.image_original.copy()
        self.colorFilter("vert")
        self.update_image()

    def onFilterB(self):
        self.image = self.image_original.copy()
        self.colorFilter("bleu")
        self.update_image()

    def onNega(self):
        self.image = self.image_original.copy()
        self.colorFilter("negatif")
        self.update_image()

    def onFilterG(self):
        self.image = self.image_original.copy()
        self.colorFilter("gris")
        self.update_image()

    def onPhoto4(self):
        width = self.image_width // 2
        height = self.image_height // 2
        if self.image_width % 2 == 1:
            width += 1
        if self.image_height % 2 == 1:
            height += 1
        sections = []
        for _ in range(2):
            for _ in range(2):
                sections.append(self.image_original.copy().resize((width, height)))
        photomaton_image = Image.new('RGB', (width*2, height*2))
        for i, section in enumerate(sections):
            x = i % 2 * width
            y = i // 2 * height
            photomaton_image.paste(section, (x, y))
        photomaton_image = QImage(photomaton_image.tobytes(), 2 * width, 2 * height, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(photomaton_image))

    def onGenerateur(self):
        self.color_window.show()

    def onColorValuesReceived(self, red, green, blue):
        image_data = self.image.convert("RGB").tobytes()
        process = bytearray()
        for i in range(0, len(image_data), 3):
            r, g, b = image_data[i], image_data[i + 1], image_data[i + 2]
            n_r = (r * red) // 255
            n_g = (g * green) // 255
            n_b = (b * blue) // 255
            process.extend((n_r, n_g, n_b))
        self.label.setPixmap(QPixmap.fromImage(QImage(process, self.image_width, self.image_height, QImage.Format_RGB888)))

    def onQuit(self):
        self.close()

    def colorFilter(self, color):
        tab = self.image.load()
        for y in range(self.image_height):
            for x in range(self.image_width):
                r, g, b = tab[x, y]
                if color == "rouge":
                    tab[x, y] = (r, 0, 0)
                elif color == "vert":
                    tab[x, y] = (0, g, 0)
                elif color == "bleu":
                    tab[x, y] = (0, 0, b)
                elif color == "gris":
                    tab[x, y] = (r, r, r)
                elif color == 'negatif':
                    tab[x, y] = (255-r,255-g,255-b)

    def update_image(self):
        self.image = self.image.convert("RGB")
        image_updated = QImage(self.image.tobytes(), self.image_width, self.image_height, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(image_updated))
        self.textLabel.setText(f'{self.image_width} X {self.image_height}')

app = QCoreApplication.instance()
if app is None:
    app = QApplication(sys.argv)
    
window = FenetrePrincipale()
window.show()

app.exec_()
