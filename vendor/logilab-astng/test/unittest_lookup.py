# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""tests for the astng variable lookup capabilities
"""
import sys
from os.path import join, abspath
from logilab.common.testlib import TestCase, unittest_main

from logilab.astng import builder, nodes, scoped_nodes, \
     InferenceError, NotFoundError

from unittest_inference import get_name_node

builder = builder.ASTNGBuilder()
MODULE = builder.file_build('data/module.py', 'data.module')
MODULE2 = builder.file_build('data/module2.py', 'data.module2')
NONREGR = builder.file_build('data/nonregr.py', 'data.nonregr')

class LookupTC(TestCase):

    def test_limit(self):
        data = '''
l = [a
     for a,b in list]

a = 1
b = a
a = None

def func():
    c = 1
        '''
        astng = builder.string_build(data, __name__, __file__)
        names = astng.nodes_of_class(nodes.Name)
        a = names.next()
        stmts = a.lookup('a')[1]
        self.failUnlessEqual(len(stmts), 1)
        b = astng.locals['b'][1]
        #self.failUnlessEqual(len(b.lookup('b')[1]), 1)
        self.failUnlessEqual(len(astng.lookup('b')[1]), 2)
        b_infer = b.infer()
        b_value = b_infer.next()
        self.failUnlessEqual(b_value.value, 1)
        self.failUnlessRaises(StopIteration, b_infer.next)
        func = astng.locals['func'][0]
        self.failUnlessEqual(len(func.lookup('c')[1]), 1)

    def test_module(self):
        astng = builder.string_build('pass', __name__, __file__)
        # built-in objects
        none = astng.ilookup('None').next()
        self.assertEquals(none.value, None)
        obj = astng.ilookup('object').next()
        self.assertIsInstance(obj, nodes.Class)
        self.assertEquals(obj.name, 'object')
        self.assertRaises(InferenceError, astng.ilookup('YOAA').next)

        # XXX
        self.assertEquals(len(list(NONREGR.ilookup('enumerate'))), 2)

    def test_class_ancestor_name(self):
        data = '''
class A:
    pass

class A(A):
    pass
        '''
        astng = builder.string_build(data, __name__, __file__)
        cls1 = astng.locals['A'][0]
        cls2 = astng.locals['A'][1]
        name = cls2.nodes_of_class(nodes.Name).next()
        self.assertEquals(name.infer().next(), cls1)
        
    ### backport those test to inline code
    def test_method(self):
        method = MODULE['YOUPI']['method']
        my_dict = method.ilookup('MY_DICT').next()
        self.assert_(isinstance(my_dict, nodes.Dict), my_dict)
        none = method.ilookup('None').next()
        self.assertEquals(none.value, None)
        self.assertRaises(InferenceError, method.ilookup('YOAA').next)
        
    def test_function_argument_with_default(self):
        make_class = MODULE2['make_class']
        base = make_class.ilookup('base').next()
        self.assert_(isinstance(base, nodes.Class), base.__class__)
        self.assertEquals(base.name, 'YO')
        self.assertEquals(base.root().name, 'data.module')

    def test_class(self):
        klass = MODULE['YOUPI']
        #print klass.getattr('MY_DICT')
        my_dict = klass.ilookup('MY_DICT').next()
        self.assertIsInstance(my_dict, nodes.Dict)
        none = klass.ilookup('None').next()
        self.assertEquals(none.value, None)
        obj = klass.ilookup('object').next()
        self.assertIsInstance(obj, nodes.Class)
        self.assertEquals(obj.name, 'object')
        self.assertRaises(InferenceError, klass.ilookup('YOAA').next)

    def test_inner_classes(self):
        ccc = NONREGR['Ccc']
        self.assertEquals(ccc.ilookup('Ddd').next().name, 'Ddd')

    def test_loopvar_hiding(self):
        astng = builder.string_build("""
x = 10
for x in range(5):
    print x
   
if x > 0:
    print '#' * x        
        """, __name__, __file__)
        xnames = [n for n in astng.nodes_of_class(nodes.Name) if n.name == 'x']
        # inside the loop, only one possible assigment
        self.assertEquals(len(xnames[0].lookup('x')[1]), 1)
        # outside the loop, two possible assigments
        self.assertEquals(len(xnames[1].lookup('x')[1]), 2)
        self.assertEquals(len(xnames[2].lookup('x')[1]), 2)

    def test_list_comps(self):
        if sys.version_info < (2, 4):
            self.skip('this test require python >= 2.4')
        astng = builder.string_build("""
print [ i for i in range(10) ]
print [ i for i in range(10) ]
print list( i for i in range(10) )
        """, __name__, __file__)
        xnames = [n for n in astng.nodes_of_class(nodes.Name) if n.name == 'i']
        self.assertEquals(len(xnames[0].lookup('i')[1]), 1)
        self.assertEquals(xnames[0].lookup('i')[1][0].lineno, 2)
        self.assertEquals(len(xnames[1].lookup('i')[1]), 1)
        self.assertEquals(xnames[1].lookup('i')[1][0].lineno, 3)
        self.assertEquals(len(xnames[2].lookup('i')[1]), 1)
        self.assertEquals(xnames[2].lookup('i')[1][0].lineno, 4)


    def test_nonregr_method_lookup(self):
        if sys.version_info < (2, 4):
            self.skip('this test require python >= 2.4')
        data = '''
class FileA:
    @staticmethod
    def funcA():
        return 4


class Test:
    FileA = [1,2,3]
    
    def __init__(self):
        print FileA.funcA()
        '''
        astng = builder.string_build(data, __name__, __file__)
        it = astng['Test']['__init__'].ilookup('FileA')
        obj = it.next()
        self.assertIsInstance(obj, nodes.Class)
        self.assertRaises(StopIteration, it.next)

    def test_decorator_arguments_lookup(self):
        if sys.version_info < (2, 4):
            self.skip('this test require python >= 2.4')
        data = '''
def decorator(value):
   def wrapper(function):
        return function
   return wrapper

class foo:
  member = 10

  @decorator(member) #This will cause pylint to complain
  def test(self):
       pass
        ''' 
        astng = builder.string_build(data, __name__, __file__)
        member = get_name_node(astng['foo'], 'member')
        print 'oop', member.lineno
        it = member.infer()
        obj = it.next()
        self.assertIsInstance(obj, nodes.Const)
        self.assertEquals(obj.value, 10)
        self.assertRaises(StopIteration, it.next)
       
    def test_nonregr_decorator_member_lookup(self):
        if sys.version_info < (2, 4):
            self.skip('this test require python >= 2.4')
        data = '''
class FileA:
    def decorator(bla):
        return bla
    
    @decorator
    def funcA():
        return 4
        '''
        astng = builder.string_build(data, __name__, __file__)
        decname = get_name_node(astng['FileA'], 'decorator')
        it = decname.infer()
        obj = it.next()
        self.assertIsInstance(obj, nodes.Function)
        self.assertRaises(StopIteration, it.next)
        
        
if __name__ == '__main__':
    unittest_main()
