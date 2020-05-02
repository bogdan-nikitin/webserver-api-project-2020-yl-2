class Anything:
    def __eq__(self, other):
        return True

    def __hash__(self):
        return 0


anything = Anything()