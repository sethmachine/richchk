"""

"""

import abc
import inspect
import re

# module level imports go here
# BEGIN imports


class Statement(abc.ABC):
    _trigedit_name = 'statement'
    _quoted_fields = frozenset()

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

# actions and conditions go here
# BEGIN ACTIONS


if __name__ == '__main__':
    pass
