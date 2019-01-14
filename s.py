from datetime import datetime
from kimage import constant


def func1(picture):
    return picture.stat().st_ctime
def func2(picture):
    return datetime.fromtimestamp(picture.stat().st_ctime)
count = 0
old_dt = datetime.now()
picture_dir = constant.BASE_DIR / 'database' / 'rename'
picture_list = list(picture_dir.glob('*'))
l1 = sorted(picture_list, key=func1)
l2 = sorted(picture_list, key=func2)
for item in l1:
    print(func2(item))
# for index, value in enumerate(l1):
#     if l1[index] != picture_list[index]:
#         print(l1[index])
#         print(l2[index])


# for picture in picture_list:
#     dt = 
#     dt
    # filename = "{}{}{}_{}"
    # if dt.hour == old_dt.hour and dt.minute == old_dt.minute and dt.second == old_dt.second:
    #     count += 1
    # elif count != 0:
    #     if count > 100:
    #         print(count)
    #     count = 0
    # old_dt = dt
    # flag += 1
    # if flag > 1000:
    #     break


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
