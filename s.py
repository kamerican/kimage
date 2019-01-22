from datetime import datetime
from kimage import constant


def sort_function(picture):
    return picture.stat().st_ctime

picture_number = 0
count = 0
previous_datetime_string = ""
picture_dir = constant.BASE_DIR / 'database' / 'rename'
picture_list = list(picture_dir.glob('*'))
sorted_list = sorted(picture_list, key=sort_function)
for picture_path in sorted_list:
    created_datetime = datetime.fromtimestamp(picture_path.stat().st_ctime)
    created_datetime_string = created_datetime.strftime("%y%m%d_%H%M%S")

    if created_datetime_string == previous_datetime_string:
        count += 1
        if count > 999:
            previous_datetime_string = created_datetime_string
            raise Exception("Error: count exceeded 999 for {}".format(picture_path))
    else:
        # if count != 0:
        #     print(count)
        count = 0
    rename_string = "{0}_{1}{2}".format(
        created_datetime_string,
        str(count).zfill(3),
        picture_path.suffix,
    )
    previous_datetime_string = created_datetime_string
    rename_path = picture_dir / rename_string
    picture_number += 1
    # if picture_number % 500 == 0:
    #     print(picture_number)
    #     print(rename_path)
    if not rename_path.is_file():
        print("{0} -> {1}".format(
            picture_path.name,
            rename_path.name,
        ))
        picture_path.rename(rename_path)


# import shelve
# from kimage.models import Organization, Group, Roster, Identity

# def init():
#     """
#     Initialize shelve with groups and identities from a list of strings.
#     """
#     organization = Organization()
#     roster = Roster()
#     idol_dict = constant.IDOL_DICT
#     groups = idol_dict.keys()
#     for group_name in groups:
#         # Add group
#         group = Group(group_name)
#         print("Adding:", group)
#         organization.add(group)
#         # Add members of the group
#         members = idol_dict[group_name]
#         for member in members:
#             identity = Identity(member, group)
#             print("Adding:", identity)
#             roster.add(identity)
#     with shelve.open(constant.DATABASE) as db:
#         db['organization'] = organization
#         db['roster'] = roster
