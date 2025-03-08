from direct.showbase.ShowBase import ShowBase
from mapmanager import Mapmanager
from direct.gui.DirectGui import DirectButton, DirectLabel, DirectFrame
from panda3d.core import TransparencyAttrib
from hero import Hero

pos = (0, 0, 1)

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.land = Mapmanager(self)  # Передаємо об'єкт ShowBase до Mapmanager
        self.camLens.setFov(90)  # Встановлюємо поле огляду камери
        self.land.addBlock((0, 0, 0))
        self.land.loadLand("land.txt")
        self.hero = Hero(pos, self.land)

        self.bg_frame = DirectFrame(image = "pack.png", scale = (1.5, 1, 1), sortOrder = 0)
        self.bg_frame.setTransparency(TransparencyAttrib.MAlpha)

        self.label = DirectLabel(text = "NOT game", scale = 0.1, pos = (0, 0, 0.8), text_fg = (1, 1, 1, 1), sortOrder = 1)

        self.button = DirectButton(text = "PLAY", scale = 0.1, pos = (0, 0, 0.6), command = self.toggle_ui, sortOrder = 2)

        self.ui_visible = False

    def toggle_ui(self):
        if not self.ui_visible:
            self.bg_frame.hide()
            self.label.hide()
            self.button.hide()
        else:
            self.bg_frame.show()
            self.label.show()

game = Game()
game.run()