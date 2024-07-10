# ADD 8 TO ALL OF THE ID's
CATEGORIES = [
    ("General Knowledge", 1),
    ("Entertainment: Books", 2),
    ("Entertainment: Film", 3),
    ("Entertainment: Music", 4),
    ("Entertainment: Musicals & Theatres", 5),
    ("Entertainment: Television", 6),
    ("Entertainment: Video Games", 7),
    ("Entertainment: Board Games", 8),
    ("Science & Nature", 9),
    ("Science: Computers", 10),
    ("Science: Mathematics", 11),
    ("Mythology", 12),
    ("Sports", 13),
    ("Geography", 14),
    ("History", 15),
    ("Politics", 16),
    ("Art", 17),
    ("Celebrities", 18),
    ("Animals", 19),
    ("Vehicles", 20),
    ("Entertainment: Comics", 21),
    ("Science: Gadgets", 22),
    ("Entertainment: Japanese Anime & Manga", 23),
    ("Entertainment: Cartoon & Animations", 24)
]
ID_TO_CATEGORIES = {1: 'General Knowledge', 2: 'Entertainment: Books', 3: 'Entertainment: Film', 4: 'Entertainment: Music', 5: 'Entertainment: Musicals & Theatres', 6: 'Entertainment: Television', 7: 'Entertainment: Video Games', 8: 'Entertainment: Board Games', 9: 'Science & Nature', 10: 'Science: Computers', 11: 'Science: Mathematics', 12: 'Mythology', 13: 'Sports', 14: 'Geography', 15: 'History', 16: 'Politics', 17: 'Art', 18: 'Celebrities', 19: 'Animals', 20: 'Vehicles', 21: 'Entertainment: Comics', 22: 'Science: Gadgets', 23: 'Entertainment: Japanese Anime & Manga', 24: 'Entertainment: Cartoon & Animations'}
NUMS = [str(i) for i in range(1, 25)]

PROHIBITED = {'global_best', 'oj', 'OJ', 'Oj'}
PROTECTED = {"oJ"}

def fun():
    DIC = {}
    for name, ID in CATEGORIES:
        DIC[ID] = name
    print(DIC)
fun()