class QueryBuilder:
    """
    A simple QueryBuilder class to generate SQL queries.
    """

    def __init__(self):
        self._table = ""
        self._columns = []
        self._conditions = []
        self._limit = 0

    def __repr__(self):
        return self.build()

    def __str__(self):
        return self.build()

    def table(self, name):
        self._table = name
        return self

    """
	Manupilators
	-----
	1. select(*columns) -> select one or more columns
	2. insert(data) -> one or more records
	3. update(data) -> with corresponding eq for primary key
	4. upsert(data) -> create if not there else update previous
	5. delete(data) -> with corresponding eq for primary key
	"""

    def select(self, *args):
        """
        Returns columns from the table
        1. select() = SELECT *
        2. select(*cols) = SELECT col1, col2, ... coln
        """
        if len(args) == 0:
            self._columns.append("*")
        else:
            self._columns.extend(args)
        return self

    """
	Conditionals
	-----

	1.  eq(column, value) -> for equality
	2.  neq(column, value) -> negative equality (not equal to)
	3.  gt(column, value) -> greater than
	4.  lt(column, value) -> less than
	5.  gte(column, value) -> greater than or equal to
	6.  lte(column, value) -> less than or equal to
	7.  like(column, pattern, case_sensitive = true) -> matches a pattern
	8.  iS(column, value) -> column is a value
	9.  iN(column, values) -> if column if one of the values 
	10. nullable(column) -> if a column IS NULL
	11. nonNullable(column) -> if a column IS NOT NULL
	"""

    def filter(self, **filters):
        """Filter records on the basis of keywords arguements"""
        for column, value in filters.items():
            # Check if column is to searched ina list of values
            if isinstance(value, list):
                self.iN(column, value)
            # Check if the column should be checked for NULL value
            elif value is None:
                self.nullable(column)
            # Check if the column is equal to the given value
            else:
                self.eq(column, value)
        return self

    def eq(self, column, value):
        """Equate values to columns"""
        self._conditions.append(f"{column} = {value}")
        return self

    def neq(self, column, value):
        self._conditions.append(f"{column} <> {value}")
        return self

    def gt(self, column, value):
        self._conditions.append(f"{column} > {value}")
        return self

    def gte(self, column, value):
        self._conditions.append(f"{column} >= {value}")
        return self

    def lt(self, column, value):
        self._conditions.append(f"{column} < {value}")
        return self

    def lte(self, column, value):
        self._conditions.append(f"{column} <= {value}")
        return self

    def iS(self, column, value):
        self._conditions.append(f"{column} IS {value}")
        return self

    def iN(self, column, values):
        refinedValues = map(lambda x: str(x), values)
        self._conditions.append(f"{column} IN ({", ".join(refinedValues)})")
        return self

    def nullable(self, column):
        self._conditions.append(f"{column} IS NULL")
        return self

    def nonNullable(self, column):
        self._conditions.append(f"{column} IS NOT NULL")
        return self

    """
	Modifiers
	-----

	1. order(column, ascending = true) -> orders the given column
	2. limit(count) -> limit the output by count
	3. single() -> returns an dict instead of array of records
	4. maybeSingle() -> retrieves zero or one record
	"""

    def limit(self, count_of_rows):
        self._limit = count_of_rows
        return self

    def build(self):
        select_clause = ""
        from_clause = ""
        where_clause = ""
        limit_clause = ""

        if self._columns:
            select_clause = "SELECT " + ", ".join(self._columns)

        if self._conditions:
            where_clause = "WHERE " + " AND ".join(self._conditions)

        if self._limit > 0:
            limit_clause = f"LIMIT {self._limit}"

        if self._table:
            from_clause = f"FROM {self._table}"

        return " ".join(
            filter(
                lambda x: len(x) > 0,
                [select_clause, from_clause, where_clause, limit_clause],
            )
        )
