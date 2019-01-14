from kimage import constant

class Table():
    """
    Base table for inheritance.
    """
    def __init__(self):
        self.table = []
        self.item_class = None
    def add(self, item):
        if isinstance(item, self.item_class):
            self.table.append(item)
        else:
            raise TypeError("Tried to save {0} in {1}!".format(
                type(item),
                self.item_class,
            ))
class Gallery(Table):
    """
    Table of pictures.
    """
    def __init__(self):
        super().__init__()
        self.item_class = Picture
class Picture():
    """
    A picture.
    """
    picture_dir = constant.BASE_DIR / 'database' / 'picture'
    def __init__(self, filename):
        self.filename = filename
        self.filepath = self.picture_dir / self.filename
        self.height = 0
        self.width = 0
        self.faces_extracted = False
        self.is_resized = False

    # @property
    # def filepath(self):
    #     pass

    def __repr__(self):
        return '<Picture: {0}>'.format(self.filename)



"""
group attribute between members are equal, but are not equal
to the group in organization
"""
class Organization(Table):
    """
    Table of groups.
    """
    def __init__(self):
        super().__init__()
        self.item_class = Group
    def get_members_of_a_group(self, group):
        pass
class Group():
    """
    A group.
    """
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return '<Group: {0}>'.format(self.name)
class Roster(Table):
    """
    Table of identities.
    """
    def __init__(self):
        super().__init__()
        self.item_class = Identity
class Identity():
    """
    An identity.
    """
    def __init__(self, name, group):
        self.name = name
        self.group = group
    def __repr__(self):
        return '<Name: {0} ({1})>'.format(
            self.name,
            self.group.name,
        )

# class Face():
#     """
#     Table of faces.
#     """
#     # Attributes
#     __tablename__ = 'face'
#     face_dir = constant.BASE_DIR / 'database' / 'face'

#     # Descriptors
#     id = Column(Integer, primary_key=True)
#     embedding = Column(PickleType)
#     filename = Column(String)
#     identity_id = Column(Integer, ForeignKey('identity.id'))
#     identity = relationship('Identity', back_populates='faces')
#     picture_id = Column(Integer, ForeignKey('picture.id'))
#     picture = relationship('Picture', back_populates='faces')

#     # add training/predicted stuff here

#     # Properties
#     @property
#     def filepath(self):
#         if self.filename is None:
#             return None
#         return self.face_dir / self.filename

#     # Public
#     def __repr__(self):
#         return '<Face: {0}>'.format(self.identity)
