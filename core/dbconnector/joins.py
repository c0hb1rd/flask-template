from core.dbconnector.conditions import BaseCondiction


class ConditionJoin:
    def __init__(self, symbol, conditions: list):
        self.conditions = []
        self.symbol = " {symbol} ".format(symbol=symbol.strip())
        self.is_join = False

        if not isinstance(conditions, list):
            conditions = [conditions]

        if len(conditions) == 1 and (
                    isinstance(conditions[0], ConditionJoin) or isinstance(conditions[0], BaseCondiction)):
            self.is_join = True
            self.conditions = conditions[0].format()
        else:
            for condition in conditions:
                if isinstance(condition, BaseCondiction) or isinstance(condition, ConditionJoin):
                    self.conditions.append(condition.format())
                else:
                    raise TypeError('must a condiction class')

    def format(self):
        if self.is_join:
            return self.conditions
        return "(%s)" % self.symbol.join(self.conditions)

    def add(self, condition):
        self.conditions.append(condition)


class AndJoin(ConditionJoin):
    def __init__(self, conditions):
        super().__init__(symbol='AND', conditions=conditions)


class OrJoin(ConditionJoin):
    def __init__(self, conditions):
        super().__init__(symbol='OR', conditions=conditions)


class Join:
    def __init__(self, table, alias, symbol, conditions: BaseCondiction):
        self.conditions = conditions
        self.symbol = symbol
        self.table = table
        self.alias = alias

    def format(self):
        base_statement = ' {symbol} JOIN {table} AS {alias}'.format(symbol=self.symbol,
                                                                    table=self.table,
                                                                    alias=self.alias)

        if self.conditions:
            base_statement += ' ON ' + self.conditions.format()

        return base_statement


class LeftJoin(Join):
    def __init__(self, table, alias, conditions: BaseCondiction):
        super().__init__(table=table, alias=alias, conditions=conditions, symbol='LEFT')


class RightJoin(Join):
    def __init__(self, table, alias, conditions: BaseCondiction):
        super().__init__(table=table, alias=alias, conditions=conditions, symbol='RIGHT')


class InnerJoin(Join):
    def __init__(self, table, alias, conditions: BaseCondiction):
        super().__init__(table=table, alias=alias, conditions=conditions, symbol='INNER')
