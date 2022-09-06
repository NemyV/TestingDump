class skills(object):
    def __init__(self, hotkey, skill_type, priority=None, cooldown=None):
        self.hotkey = hotkey
        self.skill_type = skill_type
        self.priority = priority or {}
        self.cooldown = cooldown or {}

    def setGrade(self, hotkey, cooldown):
        self.grades[hotkey] = cooldown

    def getGrade(self, hotkey):
        return self.grades[hotkey]

    def getGPA(self):
        return list(self.cooldown.keys())[0]


# Define some students
skill_1 = skills("q", "holding", "high", {"q":4})

print(skill_1.getGPA())

