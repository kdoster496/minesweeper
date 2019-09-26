class Square:
    def __init__(self, mine):
        self.isMine = mine
        self.numDisplay = 0
        self.numAround = 0
        self.flagged = False
    def setNumber(self, around):
        self.numDisplay = around
        self.numAround = around
        return self.numDisplay
    def flagMine(self):
        self.flagged = True