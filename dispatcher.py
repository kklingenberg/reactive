import inspect
import weakref
import itertools


class Dispatcher(object):

    DEFAULT_PRIORITY = 1

    def __repr__(self):
        return u"Dispatcher({0})".format(u"name={0}".format(repr(name)) \
                                         if self.name is not None else u"")
    __str__ = __repr__
    __unicode__ = __repr__

    def __init__(self, name=None):
        self._stores = weakref.WeakValueDictionary()
        self._types = dict()
        self._ids = itertools.count()
        self.name = name

    def register(self, t, fn, priority=DEFAULT_PRIORITY):
        "Registers a function for the given type *t*."
        if not inspect.isroutine(fn):
            raise TypeError("register must be applied to a routine object")
        id_ = next(self._ids)
        self._stores[id_] = fn
        self._types[id_] = (t, priority)
        return id_

    def dispatch(self, t, action):
        """Dispatches an action for all registered functions that match the
        type *t*.

        """
        matching_ids = list(
            (id_, p) for id_, (type_, p) in self._types.iteritems() if t == type_)
        matching_ids.sort(key=lambda (_, p): p)
        for id_, _ in matching_ids:
            store = self._stores.get(id_)
            if store is None:
                del self._types[id_]
            store(action)
