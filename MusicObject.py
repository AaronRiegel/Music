class MusicObject(object):
    def __init__(self, obj, obj_type, duration, box, pitch=-1):
        self.pitch = pitch
        self.duration = duration
        self.obj = obj
        self.box = box
        self.obj_type = obj_type

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

    def get_type(self):
        return self.obj_type
