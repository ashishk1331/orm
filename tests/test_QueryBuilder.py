import unittest
import sqlite3
from orm import QueryBuilder
import json


class TestQueryBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Read movies from data.json"""
        with open("./tests/data.json", encoding="utf-8") as file:
            cls.data = json.loads(file.read())
            cls.data = list(map(lambda x: tuple(x.values()), cls.data))

        """Establish connection with DB"""
        cls.connection = sqlite3.connect("sample.db")
        cls.cursor = cls.connection.cursor()

        cls.cursor.execute("CREATE TABLE IF NOT EXISTS movie(title, year, rating)")
        cls.cursor.executemany("INSERT INTO movie VALUES(?, ?, ?)", cls.data)

    @classmethod
    def tearDownClass(cls):
        cls.cursor.execute("DROP TABLE movie")
        cls.connection.close()

    def test_select_all(self):
        """Test for equality"""
        query = QueryBuilder().table("movie").select()
        titles = self.cursor.execute(str(query)).fetchall()

        # assert equal length
        self.assertEqual(len(titles), len(self.data))

        # assert all fields are found in the two sets
        for i in range(len(titles)):
            self.assertTupleEqual(titles[0], self.data[0])

    def test_select_title(self):
        """Test for equality"""
        query = QueryBuilder().table("movie").select("title")
        titles = self.cursor.execute(str(query)).fetchall()
        titles = list(map(lambda x: x[0], titles))

        stone = list(map(lambda x: x[0], self.data))

        self.assertListEqual(titles, stone)

    def test_where_in(self):
        """Test for in keyword in where clause"""
        years = [1982, 1983]

        # using .filter() method
        query_one = QueryBuilder().table("movie").select().filter(year=years)
        titles_one = self.cursor.execute(str(query_one)).fetchall()
        titles_one = list(map(lambda x: x[0], titles_one))

        # using .iN() method
        query_two = QueryBuilder().table("movie").select().iN("year", years)
        titles_two = self.cursor.execute(str(query_two)).fetchall()
        titles_two = list(map(lambda x: x[0], titles_two))

        stone = list(map(lambda x: x[0], filter(lambda x: x[1] in years, self.data)))

        # assert for equal titles
        self.assertListEqual(titles_one, stone)
        self.assertListEqual(titles_two, stone)

    def test_where_nullable(self):
        """Test for in keyword in where clause"""

        # using .filter() method
        query_one = QueryBuilder().table("movie").select().filter(year=None)
        titles_one = self.cursor.execute(str(query_one)).fetchall()
        titles_one = list(map(lambda x: x[0], titles_one))

        # using .iN() method
        query_two = QueryBuilder().table("movie").select().nullable("year")
        titles_two = self.cursor.execute(str(query_two)).fetchall()
        titles_two = list(map(lambda x: x[0], titles_two))

        stone = list(map(lambda x: x[0], filter(lambda x: x[1] is None, self.data)))

        # assert for equal titles
        self.assertListEqual(titles_one, stone)
        self.assertListEqual(titles_two, stone)
