class MusicObject(object):
    def __init__(self, obj, duration, box, pitch=-1):
        self.pitch = pitch
        self.duration = duration
        self.obj = obj
        self.box = box

    def set_pitch(self, pitch):
        self.pitch = pitch

    def set_duration(self, duration):
        self.duration = duration

    def get_object(self):
        return self.obj

    def get_pitch(self):
        return self.pitch

    def get_duration(self):
        return self.duration

    def get_box(self):
        return self.box