"""
Properties mock setter.
Use this module to mock/stub any property of New Style Class
(if you need to leave it as a property - not as an attribute,
with old style class there are no problems with doing that =)).
"""
import sys
import logging


logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)


class ValueWrapper(object):
    def __init__(self, value):
        self.value = value


class HackProp(object):
    def __init__(self, originalProp):
        self._prop = originalProp

    def __get__(self, instance, owner):
        if hasattr(instance, '_hacked_props') and self._prop in instance._hacked_props:
            return instance._hacked_props[self._prop]
        else:
            return self._prop.__get__(instance, owner)

    def __set__(self, instance, value):
        """
        Using special value wrapper to prevent unexpected
        property setting by some code
        """
        if isinstance(value, ValueWrapper):
            if not hasattr(instance, '_hacked_props'):
                instance._hacked_props = {}
            logger.info('hacking property: %s %s', instance, value)
            instance._hacked_props[self._prop] = value.value
        else:
            return self._prop.__set__(instance, value)


def hackable_properties(cls):
    for attr in dir(cls):
        item = getattr(cls, attr)
        if isinstance(item, property) and not item.fset:
            setattr(cls, attr, HackProp(item))
    return cls


if __name__ == '__main__':
    class NewStyleCls(object):
        @property
        def prop_2_mock(self):
            raise RuntimeError("Unmocked property!")


    @hackable_properties
    class NewStyleClsMocked(NewStyleCls):
        def __init__(self, *args, **kwargs):
            super(NewStyleClsMocked, self).__init__(*args, **kwargs)
            self.prop_2_mock = ValueWrapper("MOCKING_PROP_VALUE")

    mockable_cls = NewStyleClsMocked()
    assert mockable_cls.prop_2_mock == "MOCKING_PROP_VALUE"
