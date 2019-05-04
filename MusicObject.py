class MusicObject(object):
    def __init__(self, primitive, duration, box, pitch=-1):
        self.pitch = pitch
        self.duration = duration
        self.primitive = primitive
        self.box = box

    def set_pitch(self, pitch):
        self.pitch = pitch

    def set_duration(self, duration):
        self.duration = duration

    def get_objecu(self):
        return self.primitive

    def get_pitch(self):
        return self.pitch

    def get_duration(self):
        return self.duration

    def get_box(self):
        return self.box