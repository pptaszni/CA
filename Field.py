import logging

class Field:
    def __init__(self, field):
        self.background = None
        self.obj = None
        self.building = None
        self.unit = None
        self.movable = True
        self.transferable = True # TODO!
        self.border = False
        elements = field.getchildren()
        if len(elements) == 0:
            self.border = True
        for elem in elements:
            if elem.tag == 'background':
                self.background = {}
                self.background['type'] = elem.text
                if elem.text in ['stone','black']:
                    self.movable = False
            elif elem.tag == 'object':
                self.obj = {}
                self.obj['type'] = elem.text
                if elem.text in ['stone','diamond']:
                    self.movable = False
            elif elem.tag == 'building':
                self.building = {}
                self.building['type'] = elem.text
                self.building['player'] = elem.attrib['player']
                self.movable = False
            elif elem.tag == 'unit':
                self.unit = {}
                self.unit['type'] = elem.text
                self.unit['player'] = elem.attrib['player']
                self.unit['hp'] = elem.attrib['hp']
                self.movable = False
            else:
                logging.error('Unknown type of element on the field: '+elem.tag)
        if self.background == None:
            self.movable = False
    def __repr__(self):
        rep = 'Field: '
        rep = ( rep if self.background == None else 
                rep + '{Background: '+self.background['type']+'} ' )
        rep = ( rep if self.obj==None else
                rep + '{Object: '+self.obj['type']+'} ' )
        rep = ( rep if self.building==None else
                rep + '{Building: ('+self.building['type']+
                ', '+self.building['player']+')} ' )
        rep = ( rep if self.unit==None else 
                rep + '{Unit: ('+self.unit['type']+
                ', '+self.unit['player'] + ', '+self.unit['hp']+')}' )
        return rep
    def __eq__(self,other):
        if not hasattr(other,'__dict__'):
            return False
        return self.__dict__ == other.__dict__
    def __ne__(self,other):
        if not hasattr(other,'__dict__'):
            return True
        return self.__dict__ != other.__dict__

