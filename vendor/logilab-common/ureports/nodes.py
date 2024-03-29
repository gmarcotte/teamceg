"""Micro reports objects.

A micro report is a tree of layout and content objects.

:copyright:
  2004-2008 `LOGILAB S.A. <http://www.logilab.fr>`_ (Paris, FRANCE),
  all rights reserved.

:contact:
  http://www.logilab.org/project/logilab-common --
  mailto:python-projects@logilab.org

:license:
  `General Public License version 2
  <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>`_
"""
__docformat__ = "restructuredtext en"

from logilab.common.tree import VNode

class BaseComponent(VNode):
    """base report component

    attributes
    * id : the component's optional id
    * klass : the component's optional klass
    """
    def __init__(self, id=None, klass=None):
        VNode.__init__(self, id)
        self.klass = klass

class BaseLayout(BaseComponent):
    """base container node

    attributes
    * BaseComponent attributes
    * children : components in this table (i.e. the table's cells)
    """
    def __init__(self, children=(), **kwargs):
        super(BaseLayout, self).__init__(**kwargs)
        for child in children:
            if isinstance(child, BaseComponent):
                self.append(child)
            else:
                self.add_text(child)

    def append(self, child):
        """overridden to detect problems easily"""
        assert child not in self.parents()
        VNode.append(self, child)
        
    def parents(self):
        """return the ancestor nodes"""
        assert self.parent is not self
        if self.parent is None:
            return []
        return [self.parent] + self.parent.parents()
    
    def add_text(self, text):
        """shortcut to add text data"""
        self.children.append(Text(text))


# non container nodes #########################################################

class Text(BaseComponent):
    """a text portion

    attributes :
    * BaseComponent attributes
    * data : the text value as an encoded or unicode string
    """
    def __init__(self, data, escaped=True, **kwargs):
        super(Text, self).__init__(**kwargs)
        #if isinstance(data, unicode):
        #    data = data.encode('ascii')
        assert isinstance(data, (str, unicode)), data.__class__
        self.escaped = escaped
        self.data = data

class VerbatimText(Text):
    """a verbatim text, display the raw data

    attributes :
    * BaseComponent attributes
    * data : the text value as an encoded or unicode string
    """
        
class Link(BaseComponent):
    """a labelled link

    attributes :
    * BaseComponent attributes
    * url : the link's target (REQUIRED)
    * label : the link's label as a string (use the url by default)
    """
    def __init__(self, url, label=None, **kwargs):
        super(Link, self).__init__(**kwargs)
        assert url
        self.url = url
        self.label = label or url

        
class Image(BaseComponent):
    """an embeded or a single image

    attributes :
    * BaseComponent attributes
    * filename : the image's filename (REQUIRED)
    * stream : the stream object containing the image data (REQUIRED)
    * title : the image's optional title
    """
    def __init__(self, filename, stream, title=None, **kwargs):
        super(Link, self).__init__(**kwargs)
        assert filename
        assert stream
        self.filename = filename
        self.stream = stream
        self.title = title

        
# container nodes #############################################################
        
class Section(BaseLayout):
    """a section

    attributes :
    * BaseLayout attributes
    
    a title may also be given to the constructor, it'll be added
    as a first element
    a description may also be given to the constructor, it'll be added
    as a first paragraph
    """
    def __init__(self, title=None, description=None, **kwargs):
        super(Section, self).__init__(**kwargs)
        if description:
            self.insert(0, Paragraph([Text(description)]))
        if title:
            self.insert(0, Title(children=(title,)))
        
class Title(BaseLayout):
    """a title
    
    attributes :
    * BaseLayout attributes

    A title must not contains a section nor a paragraph!
    """
    
class Span(BaseLayout):
    """a title
    
    attributes :
    * BaseLayout attributes

    A span should only contains Text and Link nodes (in-line elements)
    """
    
class Paragraph(BaseLayout):
    """a simple text paragraph
    
    attributes :
    * BaseLayout attributes

    A paragraph must not contains a section !
    """
    
class Table(BaseLayout):
    """some tabular data

    attributes :
    * BaseLayout attributes
    * cols : the number of columns of the table (REQUIRED)
    * rheaders : the first row's elements are table's header
    * cheaders : the first col's elements are table's header
    * title : the table's optional title
    """    
    def __init__(self, cols, title=None,
                 rheaders=0, cheaders=0, rrheaders=0, rcheaders=0,
                 **kwargs):
        super(Table, self).__init__(**kwargs)
        assert isinstance(cols, int)
        self.cols = cols
        self.title = title
        self.rheaders = rheaders
        self.cheaders = cheaders
        self.rrheaders = rrheaders
        self.rcheaders = rcheaders
        
class List(BaseLayout):
    """some list data

    attributes :
    * BaseLayout attributes
    """    
