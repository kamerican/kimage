from kimage import constant
from kimage.models import Base, Face, Picture, Identity, Group

session = constant.session_factory()

def create_db():
    """
    Initialize SQLITE db if not created yet.
    """
    if not constant.DATABASE_PATH.is_file():
        print("Creating database...")
        Base.metadata.create_all(constant.engine)
def refresh_idols():
    """
    Clears tables and adds idols.
    """
    # Clear tables
    clear_table(Face)
    clear_table(Picture)
    clear_table(Identity)
    clear_table(Group)

    # Add idols
    add_idols(constant.IDOL_DICT)
def add_idols(idol_dict):
    """
    Add idols to db from a list of strings.
    """
    groups = idol_dict.keys()
    for group_name in groups:
        # Add group
        group = Group()
        group.name = group_name
        print("Adding:", group)
        session.add(group)

        # Add members of the group
        members = idol_dict[group_name]
        for member in members:
            identity = Identity()
            identity.group = group
            identity.name = member
            print("Adding:", identity)
            session.add(identity)
def clear_table(table_class):
    """
    Clears the db table parameter.
    """
    query_list = session.query(table_class).all()
    if query_list:
        for query in query_list:
            print("Removing:", query)
            session.delete(query)
def save():
    """
    Commit changes and close the session connection.
    """
    session.commit()
    session.close()
def revert():
    """
    Rollback changes and close the session connection.
    """
    session.rollback()
    session.close()
