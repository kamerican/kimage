from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

# from pathlib import Path
from kimage import constant

Base = declarative_base()

class Group(Base):
    """
    Table of groups.
    """
    # Attributes
    __tablename__ = 'group'

    # Descriptors
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # One group to many identities
    identities = relationship('Identity', back_populates='group')

    # Public
    def __repr__(self):
        return '<Group: {0}>'.format(self.name)
class Identity(Base):
    """
    Table of identities.
    """
    # Attributes
    __tablename__ = 'identity'

    # Descriptors
    id = Column(Integer, primary_key=True)
    name = Column(String)
    # One identity to many faces
    faces = relationship('Face', back_populates='identity')
    # Each identity has a group
    group_id = Column(Integer, ForeignKey('group.id'))
    group = relationship('Group', back_populates='identities')

    # Public
    def __repr__(self):
        return '<Name: {0} ({1})>'.format(
            self.name,
            self.group.name,
        )
class Picture(Base):
    """
    Table of pictures.
    """
    # Attributes
    __tablename__ = 'picture'
    picture_dir = constant.BASE_DIR / 'database' / 'picture'

    # Descriptors
    id = Column(Integer, primary_key=True)
    _filename = Column(String)
    faces_extracted = Column(Boolean, default=False, nullable=False)
    faces = relationship('Face', back_populates='picture')

    # Properties
    @hybrid_property
    def filepath(self):
        if self._filename is None:
            return None
        return self.picture_dir / self._filename
    @filepath.setter
    def filepath(self, path):
        self._filename = path.name
    @filepath.expression
    def filepath(self):
        return self._filename

    # Public
    def __repr__(self):
        return '<Picture: {0}>'.format(self._filename)
class Face(Base):
    """
    Table of faces.
    """
    # Attributes
    __tablename__ = 'face'
    face_dir = constant.BASE_DIR / 'database' / 'face'

    # Descriptors
    id = Column(Integer, primary_key=True)
    embedding = Column(PickleType)
    _filename = Column(String)
    identity_id = Column(Integer, ForeignKey('identity.id'))
    identity = relationship('Identity', back_populates='faces')
    picture_id = Column(Integer, ForeignKey('picture.id'))
    picture = relationship('Picture', back_populates='faces')

    # add training/predicted stuff here

    # Properties
    @hybrid_property
    def filepath(self):
        if self._filename is None:
            return None
        return self.face_dir / self._filename

    @filepath.setter
    def filepath(self, path):
        self._filename = path.name

    # Public
    def __repr__(self):
        return '<Face: {0}>'.format(self.identity)
