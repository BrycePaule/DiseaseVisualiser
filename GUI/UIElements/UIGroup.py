
class UIGroup:

    def __init__(self, name, *members, single_selection=False):
        self.name = name
        self.members = [member for member in members]
        self.single_selection = single_selection


    def add(self, member):
        self.members.append(member)
        member.ui_group = self