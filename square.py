
from CoordinateSystemTools import CoordinateSystemTools


class Square():
    def __init__(self, p1, p2, p3, p4, position):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.position = position

    def points(self):
        correctedpoints = CoordinateSystemTools(
            self.p1, self.p2, self.p3, self.p4)
        return correctedpoints.points


class ImageSquare():
    
    def __init__(self, img, position):
        self.img = img
        self.position = position

    def prediction(self, pred):
        return [self.position, pred]
