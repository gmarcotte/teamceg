""" docstring for file clientmodule.py """
from data2.suppliermodule_test import Interface as IFace, DoNothing

class Toto: pass

class Ancestor:
    """ Ancestor method """
    __implements__ = (IFace,)
    
    def __init__(self, value):
        local_variable = 0
        self.attr = 'this method shouldn\'t have a docstring'
        self.__value = value

    def get_value(self):
        """ nice docstring ;-) """
        return self.__value

    def set_value(self, value):
        self.__value = value
        return 'this method shouldn\'t have a docstring'    

class Specialization(Ancestor):
    TYPE = 'final class'
    top = 'class'
    
    def __init__(self, value, _id):
        Ancestor.__init__(self, value)
        self._id = _id
        self.relation = DoNothing()
        self.toto = Toto()
        
