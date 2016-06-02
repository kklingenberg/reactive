from . import ao

class Component(object):

    STATE_ATTRIBUTE = "_component_state"

    @property
    def state(self):
        if not hasattr(self, self.STATE_ATTRIBUTE):
            setattr(self, self.STATE_ATTRIBUTE, AO())
        return getattr(self, self.STATE_ATTRIBUTE)

    def get_state(self):
        raise NotImplementedError("get_state() method not implemented")

    def set_state(self, s):
        if not isinstance(s, ao.AO):
            raise TypeError("state value must be an AO instance")
        past = self.get_state()
        if not isinstance(past, ao.AO):
            raise TypeError("get_state() didn't return AO instance: {0}".\
                            format(type(past)))
        self.derender(ao.diffkeys(s, past))
        self.render(ao.diff(past, s))
        setattr(self, self.STATE_ATTRIBUTE, s)

    def derender(self, diff):
        raise NotImplementedError("derender(diff) method not implemented")

    def render(self, diff):
        raise NotImplementedError("render(diff) method not implemented")
