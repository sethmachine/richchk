"""

"""

import abc
import inspect
import re

from scunit import SCUnit


class Statement(abc.ABC):
    _trigedit_name = 'Statement'
    _quoted_fields = set()

    def __init__(self):
        pass

    def _is_quoted(self, value):
        return True if re.search(r'^".+?"$', value) is not None else False

    def _quote_value(self, value):
        return '"{}"'.format(value)

    def compile(self, pretty=False) -> str:
        """Compiles the action/condition into format usable by SCMDraft TrigEdit.

        :param pretty: whether to include name of each argument (cannot be used in TrigEdit); use for debugging
        :type pretty: bool
        :return: a string representing the TrigEdit format for the trigger action or condition
        :rtype: str
        """
        values = []
        for arg in inspect.getfullargspec(self.__init__).args:
            if arg != 'self':
                value = getattr(self, arg)
                if arg in self.__class__._quoted_fields:
                    if not self._is_quoted(value):
                        value = self._quote_value(value)
                if pretty:
                    values.append('{}={}'.format(arg, value if type(value) == str else str(value)))
                else:
                    values.append(value if type(value) == str else str(value))
        return '{}({});'.format(self.__class__._trigedit_name, ', '.join(values))

    def __repr__(self):
        return self.compile()


class Condition(Statement):
    _trigedit_name = 'condition'

    def __init__(self):
        super().__init__()
        self.type = self.__class__.__name__

class Action(Statement):
    _trigedit_name = 'action'

    def __init__(self):
        super().__init__()
        self.type = self.__class__.__name__


class Bring(Action):
    _trigedit_name = 'Bring'
    _quoted_fields = {'player', 'unit', 'location'}

    def __init__(self, player: str, unit: SCUnit, location: str, quantifier: str, count: int):
        """Bring action.

        :param player:
        :param unit:
        :param location:
        :param quantifier:
        :param count:
        """
        super().__init__()
        self.player = player
        self.unit = unit
        self.location = location
        self.quantifier = quantifier
        self.count = count


if __name__ == '__main__':
    b = Bring("Player 1", "foof", "bar", "car", 1)
    print(b.compile())
    print(b.compile(pretty=True))
