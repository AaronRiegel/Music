class MusicObject(object):
    def __init__(self, primitive, duration, box, pitch=-1):
        self.pitch = pitch
        self.duration = duration
        self.primitive = primitive
        self.box = box

    def set_Pitch(self, pitch):
        self.pitch = pitch

    def set_Duration(self, duration):
        self.duration = duration

    def get_Primitive(self):
        return self.primitive

    def get_Pitch(self):
        return self.pitch

    def get_Duration(self):
        return self.duration

    def get_Box(self):
        return self.box