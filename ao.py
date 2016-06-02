class AO(object):
    "Anonymous object"

    def __init__(self, **kwargs):
        if any(k.startswith("_") for k in kwargs):
            raise RuntimeError("AO field can't start with '_'")
        super(AO, self).__setattr__('_keys', set(kwargs))
        for k in self._keys:
            super(AO, self).__setattr__(k, kwargs[k])

    def __getitem__(self, k):
        return getattr(self, k)

    def __setattr__(self, k, v):
        if k.startswith("_"):
            raise RuntimeError("AO field can't start with '_'")
        self._keys.add(k)
        super(AO, self).__setattr__(k, v)
    __setitem__ = __setattr__

    def __delattr__(self, k):
        if k in self._keys:
            self._keys.remove(k)
        super(AO, self).__delattr__(k)
    __delitem__ = __delattr__

    def __iter__(self):
        return ((k, getattr(self, k)) for k in self._keys)

    def __contains__(self, k):
        return k in self._keys

    def __nonzero__(self):
        return bool(self._keys)

    def _deepcopy(self):
        return AO(**dict(
            dict(self),
            **dict((k, v._deepcopy()) for k, v in self if isinstance(v, AO))))

    def __repr__(self):
        return u"AO({0})".format(
            u", ".join(u"{0}={1}".format(k, repr(v)) for k, v in self))
    __str__ = __repr__
    __unicode__ = __repr__


def diff(from_, to):
    "Returns an AO with the fields in *to* that are different in *from_*."
    if not isinstance(from_, AO) or not isinstance(to, AO):
        raise TypeError("expected AO instance")
    d = dict((k, v) for k, v in to
             if not isinstance(v, AO)
             if k not in from_ or from_[k] != v)
    d.update(dict((k, v) for k, v in to
                  if isinstance(v, AO)
                  if k not in from_ or not isinstance(from_[k], AO)))
    d.update(dict((k, diff(from_[k], v))
                  for k, v in to
                  if isinstance(v, AO)
                  if k in from_
                  if isinstance(from_[k], AO)
                  if diff(from_[k], v)))
    return AO(**d)


def diffkeys(from_, to):
    "Returns an AO with the fields in *to* that are not in *from_*."
    if not isinstance(from_, AO) or not isinstance(to, AO):
        raise TypeError("expected AO instance")
    d = dict((k, v) for k, v in to
             if k not in from_)
    d.update(dict((k, diffkeys(from_[k], v))
                  for k, v in to
                  if isinstance(v, AO)
                  if k in from_
                  if isinstance(from_[k], AO)))
    for empty in [k for k, v in d.iteritems() if isinstance(v, AO) and not v]:
        del d[empty]
    return AO(**d)
