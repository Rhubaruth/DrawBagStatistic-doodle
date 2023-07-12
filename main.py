import random
from typing import Literal

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtGui, uic

BASE = {
    "STR": 2,
    "DEX": 2,
    "WIS": 2,
    "TT": 0,
    "MISS": 5
}
KEYS = list(BASE.keys())


ATTEMPTS = 1000

qtCreatorFile = "gui.ui"  # Enter file # here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class MyApp(QMainWindow, Ui_MainWindow):
    STATS = {
        "STR": 3,
        "DEX": 1,
        "WIS": 1,
        "TT": 0,
        "MISS": 0
    }

    bag = []

    DRAW = 5
    ABILITY = "STR"
    SUCCESS_LEVEL = 2
    MISS_LEVEL = 3

    SEED = 45685

    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.buttonBuild.clicked.connect(self.create_bag)
        self.buttonPercentage.clicked.connect(self.get_percentages)
        self.SEED = random.randbytes(3)

        self.create_bag()

    def create_bag(self):
        if not self._get_stats():
            return

        self.bag = []
        for key in self.STATS.keys():
            self.bag += [key] * (self.STATS[key] + BASE[key])

    def get_percentages(self):
        if len(self.bag) < 1:
            print("Bag was not created")
            return
        if not self._get_draw_info():
            return

        draw = min(self.DRAW, len(self.bag))

        outputs = []
        for offset in range(-2, 3):
            curr_draw = draw + offset
            if curr_draw < 1 or curr_draw > len(self.bag):
                continue

            percentage = self._percentage(self.bag, curr_draw, self.SEED)
            outputs.append((curr_draw, percentage))

        print("\n-----------------------------------------------------------")
        print('; '.join([f"{key}: {self.bag.count(key)}" for key in self.STATS.keys()]))
        for out in outputs:
            print(f"Percentage drawing {out[0]} tokens: {100 * out[1]:.2f} %")

    def _percentage(self, bag=None, draw: int = 5,
                    rand_seed: random = 123):
        if bag is None:
            return 0
        random.seed(rand_seed)

        # exe = random.sample(bag, draw)
        successes = 0
        for _ in range(ATTEMPTS):
            sample = random.sample(bag, draw)
            hits = sample.count(self.ABILITY)
            misses = sample.count("MISS")

            if hits >= self.SUCCESS_LEVEL and misses < self.MISS_LEVEL:
                successes += 1
                # exe = sample
        # print(sorted(exe, key=lambda item: KEYS.index(item)))
        return successes / ATTEMPTS


    def _get_draw_info(self):
        try:
            draw = int(self.lineEditKeyDraw.text())
            success_level = int(self.lineEditKeyDiff.text())
            ability = self.lineEditKeyAbility.text()

        except TypeError:
            print("ERROR")
            return False
        if draw < 1:
            return False
        if success_level > 7 or success_level < 1:
            return False
        if ability not in self.STATS.keys():
            return False

        self.DRAW = draw
        self.SUCCESS_LEVEL = success_level
        self.ABILITY = ability

        return True

    def _get_stats(self):
        try:
            STR = int(self.lineEditKeySTR.text())
            DEX = int(self.lineEditKeyDEX.text())
            WIS = int(self.lineEditKeyWIS.text())

            TOX = int(self.lineEditKeyTOX.text())
            MISS = int(self.lineEditKeyMIS.text())
        except TypeError:
            print("ERROR")
            return False

        self.STATS["STR"] = STR
        self.STATS["DEX"] = DEX
        self.STATS["WIS"] = WIS

        self.STATS["TT"] = TOX
        self.STATS["MISS"] = MISS
        # print(self.STATS)
        return True


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
