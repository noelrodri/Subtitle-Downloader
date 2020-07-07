
import re
x = ["Version TLA, 269.00 MBs",
     "Version DVDRip.x264 - TASTETV, 0.00 MBs ",
     "Version TLA, 269.00 MBs",
     "Version DVDRip.x264 - TASTETV, 0.00 MBs",
     ]


# for i in x:
#   print(i.split('Version '))

# print(re.split("Version TLA, 269.00 MBs" , "Version"))


strs = "Version TLA, 269.00 MBs"

# print(re.findall(r"Version  , MBs", strs))

# for strs in x:
#     subteams = re.findall(r'Version (.*),', strs)
#     print(subteams[0].split(" _ "))


strs = 'DVDRip.x264 - TASTETV'

# print(strs.split("-"))

{'tla'}
{'x264-tastetv', 'dvdrip'}


'''
tla
dvdrip .x264-tastetv
tla
dvdrip .x264-tastetv
'''

# links = [ < a class = "buttonDownload" href = "/original/105576/1" > <strong > Download < /strong > </a > ]
