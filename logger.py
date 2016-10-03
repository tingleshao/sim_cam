#  the goal of this is to print debug messages when the debug option is up

class logger:

    @staticmethod
    def debug_print(tag, message):
        if tag == 'debug':
            print message
