from abc import ABC

class RestService(ABC):
    
    #Given a choice, and options (a set of choices), returns true if choice is included in options
    def valid_choice(self, choice, options):
        valid_choice = False
        for choices in options:
            if choice in choices:
                valid_choice = True
                break

        return valid_choice