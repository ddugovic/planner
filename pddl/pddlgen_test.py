#!/usr/bin/python2

from pddlgen import proc_text, produce_problem

easy = """# # # # # # # # #
# @ #   # E H   #
#   #   # # #   #
#   #   #       #
#         #     #
# # # #   #   # #
#         #     #
#   # #       # #
# # # # # # # # #
"""

chips_x = """# # # # # # # # #
# E # $ #   $   #
# H #   #   #   #
# @             #
#   # # # #     #
#   # $         #
#   # # # #     #
#               #
# # # # # # # # #
"""

pie="""# # # # # # # # #
# @       $ # $ #
#   # # # # # # #
#   #   H E     #
#   #   # # #   #
#   #           #
# $     #   # # #
# $     # $ # $ #
# # # # # # # # #
"""

chips = """# # # # # # # # #
# E # $ #   $   #
# H #   #   #   #
# @             #
#   # # # #     #
#   # $         #
#   # # # #     #
#               #
# # # # # # # # #
"""

hazard="""# # # # # # # # #
# @         , $ #
#   , , ,       #
#   & E H   ,   #
#   & & &   ,   #
#               #
#   &   & & &   #
# $ &     $ & $ #
# # # # # # # # #
"""

hints="""# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # @ # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # ? # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# #   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # $ # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# #   # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # H # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # E # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""

#A	blue key
#B	red key
#C	yellow key
#D	blue door
#F	red door
#G	green door
#I	yellow door
#J	green key

keys="""# # # # # # # # #
# # $ # $ # A $ #
# # B # C #     #
# # D # F #     #
# @             #
# # G # I # G # #
# #   # J #   H #
# # $ # $ # H E #
# # # # # # # # #
"""

#produce_problem( proc_text(easy), 0 )
#produce_problem( proc_text(chips), 3 )
#produce_problem( proc_text(pie), 5 )
#produce_problem( proc_text(hints), 0 )
#produce_problem( proc_text(keys), 5 )


def test_produce_problem():
    assert produce_problem( proc_text(hazard), 4 ) is None

