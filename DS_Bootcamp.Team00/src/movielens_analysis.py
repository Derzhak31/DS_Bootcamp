import os
from collections import Counter, defaultdict
from datetime import datetime
from contextlib import nullcontext

import pytest
import requests
from bs4 import BeautifulSoup


class Basic:
    def __init__(self, path_to_the_file: str, lines: int):
        self.path_to_the_file = path_to_the_file
        self.lines = lines

    def read_csv(self) -> list[dict[str:str]]:
        if not isinstance(self.path_to_the_file, str):
            raise ValueError(f"Ошибка: {self.path_to_the_file} не строка!")
        if not os.path.isfile(self.path_to_the_file):
            raise FileNotFoundError(f"Файл {self.path_to_the_file} не найден!")
        if not isinstance(self.lines, int) or self.lines < 1:
            raise ValueError(f"Ошибка: '{self.lines}' не является числом >= 0.")
        with open(self.path_to_the_file, "r", encoding="utf-8") as f:
            fields = f.readline()[:-1].split(",")
            if "" in fields:
                raise ValueError(
                    f"Пустое значение заголовка в файле {self.path_to_the_file}!"
                )
            rows = [f.readline()[:-1].split(",") for _ in range(self.lines)]
        data = []
        for row in rows:
            while len(fields) < len(row):
                row[1] += row.pop(2)
                if row[1][-1] == '"':
                    row[1] = row[1][1:-1]
            data.append(dict(zip(fields, row)))
        return data


class Links(Basic):
    def __init__(self, path_to_the_file: str = "links.csv", lines: int = 9742):
        super().__init__(path_to_the_file, lines)
        self.data = super().read_csv()
        self.lines = lines
        self.imdb_info = self.get_imdb(
            self.data,
            [
                "Director",
                "Budget",
                "Gross worldwide",
                "Runtime",
                "RATING",
                "Popularity",
            ],
        )

    def get_imdb(
        self, list_of_movies: list, list_of_fields: list
    ) -> list[list[str | list[str]]]:
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 YaBrowser/25.2.0.0 Safari/537.36"
        }
        imdb_info = []
        for elem in list_of_movies:
            try:
                url = f"https://www.imdb.com/title/tt{elem['imdbId']}/"
                response = requests.get(url=url, headers=headers, timeout=5)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                line = [int(elem["movieId"])]
                for field in list_of_fields:
                    if field == "Director":
                        direc = soup.find("div", class_="sc-70a366cc-3 iwmAOx")
                        if direc.find("span") != None:
                            line.append([direc.find("a").text])
                        else:
                            data = (
                                direc.find("div")
                                .find_next()
                                .find("ul", {"role": "presentation"})
                                .find_all("a")
                            )
                            dir_all = []
                            for i in data:
                                dir_all.append(i.text)
                            line.append(dir_all)
                    elif field == "Budget":
                        budget = soup.find(
                            "div", {"data-testid": "title-boxoffice-section"}
                        )
                        if budget != None:
                            line.append(
                                int(
                                    soup.find(
                                        "div",
                                        {"data-testid": "title-boxoffice-section"},
                                    )
                                    .find("div")
                                    .text.split(" ")[0][1:]
                                    .replace(",", "")
                                )
                            )
                            line.append(
                                int(
                                    soup.find(
                                        "div",
                                        {"data-testid": "title-boxoffice-section"},
                                    )
                                    .find(
                                        "li",
                                        {
                                            "data-testid": "title-boxoffice-cumulativeworldwidegross"
                                        },
                                    )
                                    .find("div")
                                    .text[1:]
                                    .replace(",", "")
                                )
                            )
                        else:
                            line.append("n/a")
                            line.append("n/a")
                    elif (
                        field
                        == soup.find("li", {"data-testid": "title-techspec_runtime"})
                        .find("span")
                        .text
                    ):
                        m = (
                            soup.find("li", {"data-testid": "title-techspec_runtime"})
                            .find("div")
                            .text.split()
                        )
                        line.append(int(m[0]) * 60 + int(m[2]))

                    elif (
                        field
                        == soup.find(
                            "div", class_="sc-3a4309f8-0 jJkxPn sc-70a366cc-1 kUfGfN"
                        )
                        .find("div", class_="sc-acdbf0f3-1 ioCFan")
                        .text.split()[1]
                    ):
                        line.append(
                            float(soup.find("span", class_="sc-d541859f-1 imUuxf").text)
                        )

                    elif field == "Popularity":
                        if (
                            soup.find("div", class_="sc-3a4309f8-1 dOjKRs").find(
                                "div", {"data-testid": "hero-rating-bar__popularity"}
                            )
                            != None
                        ):
                            line.append(
                                int(
                                    soup.find(
                                        "div",
                                        {
                                            "data-testid": "hero-rating-bar__popularity__score"
                                        },
                                    ).text.replace(",", "")
                                )
                            )
                        else:
                            line.append("n/a")
                line.append(soup.find("h1").text)
                imdb_info.append(line)
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при запросе к IMDb для фильма {elem["movieId"]}: {e}")
        return imdb_info

    def top_directors(self, n: int) -> dict[str:int]:
        if not isinstance(n, int) or n < 1:
            raise ValueError(f"Ошибка: '{n}' не является числом >= 0.")
        data = []
        for item in self.imdb_info:
            if len(item[1]) == 1:
                data.append(item[1][0])
            else:
                for i in item[1]:
                    data.append(i)
        directors = dict(Counter(elem for elem in data).most_common(n))
        return directors

    def most_expensive(self, n: int) -> dict[str:int]:
        if not isinstance(n, int) or n < 1:
            raise ValueError(f"Ошибка: '{n}' не является числом >= 0.")
        sort_data = sorted(
            [x for x in self.imdb_info if x[2] != "n/a"],
            key=lambda i: -int(i[2]),
        )[:n]
        budgets = {}
        for i in sort_data:
            budgets[i[7]] = int(i[2])
        return budgets

    def most_total_collection(self, n: int) -> dict[str:int]:
        if not isinstance(n, int) or n < 1:
            raise ValueError(f"Ошибка: '{n}' не является числом >= 0.")
        sort_data = sorted(
            [x for x in self.imdb_info if x[3] != "n/a"],
            key=lambda i: -int(i[3]),
        )[:n]
        result = {}
        for i in sort_data:
            result[i[7]] = int(i[3])
        return result

    def most_profitable(self, n: int) -> dict[str:int]:
        if not isinstance(n, int) or n < 1:
            raise ValueError(f"Ошибка: '{n}' не является числом >= 0.")
        data = {}
        for i in self.imdb_info:
            if i[2] != "n/a":
                data[i[7]] = int(i[3]) - int(i[2])
        profits = dict(sorted(data.items(), key=lambda item: -item[1])[:n])
        return profits

    def longest(self, n: int) -> dict[str:int]:
        if not isinstance(n, int) or n < 1:
            raise ValueError(f"Ошибка: '{n}' не является числом >= 0.")
        sort_data = sorted(
            [x for x in self.imdb_info],
            key=lambda i: -int(i[4]),
        )[:n]
        runtimes = {}
        for i in sort_data:
            runtimes[i[7]] = int(i[4])
        return runtimes

    def top_cost_per_minute(self, n: int) -> dict[str:int]:
        if not isinstance(n, int) or n < 1:
            raise ValueError(f"Ошибка: '{n}' не является числом >= 0.")
        data = {}
        for i in self.imdb_info:
            if i[2] != "n/a":
                data[i[7]] = round(float(float(i[2]) / float(i[4])), 2)
        costs = dict(sorted(data.items(), key=lambda item: -item[1])[:n])
        return costs

    def most_ratings(self, n: int) -> dict[str:int]:
        if not isinstance(n, int) or n < 1:
            raise ValueError(f"Ошибка: '{n}' не является числом >= 0.")
        sort_data = sorted(self.imdb_info, key=lambda i: -float(i[5]))[:n]
        result = {}
        for i in sort_data:
            result[i[7]] = float(i[5])
        return result

    def most_popularity(self, n: int) -> dict[str:int]:
        if not isinstance(n, int) or n < 1:
            raise ValueError(f"Ошибка: '{n}' не является числом >= 0.")
        sort_data = sorted(
            [x for x in self.imdb_info if x[6] != "n/a"],
            key=lambda i: int(i[6]),
        )[:n]
        result = {}
        for i in sort_data:
            result[i[7]] = int(i[6])
        return result


class Movies(Basic):
    def __init__(self, path_to_the_file: str = "movies.csv", lines: int = 9742):
        super().__init__(path_to_the_file, lines)
        self.data = super().read_csv()
        self.lines = lines
        self.all_genres = [
            "Action",
            "Adventure",
            "Animation",
            "Children",
            "Comedy",
            "Crime",
            "Documentary",
            "Drama",
            "Fantasy",
            "Film-Noir",
            "Horror",
            "Musical",
            "Mystery",
            "Romance",
            "Sci-Fi",
            "Thriller",
            "War",
            "Western",
            "(no genres listed)",
        ]

    def dist_by_release(self) -> dict[int:int]:
        all_years = []
        for row in self.data:
            year = int(row["title"][-5:-1])
            all_years.append(year)
        release_years = dict(Counter(all_years).most_common())
        return release_years

    def dist_by_genres(self) -> dict[str:int]:
        list_genres = []
        for row in self.data:
            elems = row["genres"].split("|")
            for elem in elems:
                if elem in self.all_genres:
                    list_genres.append(elem)
                else:
                    list_genres.append("(no genres listed)")
        genres = dict(Counter(list_genres).most_common())
        return genres

    def most_genres(self, n):
        if not isinstance(n, int) or n < 1:
            raise ValueError(f"Ошибка: '{n}' не является числом >= 0.")
        movies = dict(Counter(self.dist_by_genres()).most_common(n))
        return movies


class Ratings(Basic):
    def __init__(self, filename="ratings.csv", lines=100836):
        super().__init__(filename, lines)
        self.data = super().read_csv()
        self.lines = lines

    class Movies:
        def __init__(self, data_ratings, data_movies):
            self.data_ratings = data_ratings
            self.data_movies = data_movies

        def dist_by_year(self) -> dict[int:int]:
            year = Counter(
                [
                    datetime.fromtimestamp(int(row["timestamp"])).year
                    for row in self.data_ratings
                ]
            )
            ratings_by_year = dict(sorted(year.items(), key=lambda item: -item[0]))
            return ratings_by_year

        def dist_by_rating(self) -> dict[float:int]:
            rating = Counter([float(row["rating"]) for row in self.data_ratings])
            ratings_distribution = dict(
                sorted(rating.items(), key=lambda item: item[0])
            )
            return ratings_distribution

        def top_by_num_of_ratings(self, n: int) -> dict[str:int]:
            if not isinstance(n, int) or n < 1:
                raise ValueError(f"Ошибка: '{n}' не является числом >= 0.")
            rating = Counter(
                [
                    line["title"][:-7]
                    for row in self.data_ratings
                    for line in self.data_movies
                    if row["movieId"] == line["movieId"]
                ]
            )
            top_movies = dict(sorted(rating.items(), key=lambda item: -item[1])[:n])
            return top_movies

        def top_by_ratings(self, n: int, metric: str = "average") -> dict[str:float]:
            if not isinstance(n, int) or n < 1:
                raise ValueError("Ошибка: n не является числом >= 0.")
            if not isinstance(metric, str) or metric not in ["average", "median"]:
                raise ValueError("Ошибка: metric не со значением average или median.")
            if metric == "average":
                metric_func = lambda ratings: sum(ratings) / len(ratings)
            else:
                metric_func = lambda ratings: sorted(ratings)[len(ratings) // 2]
            movie_ratings = defaultdict(list)
            for row in self.data_ratings:
                movie_ratings[row["movieId"]].append(float(row["rating"]))
            movie_metrics = {
                film["title"][:-7]: round(metric_func(ratings), 2)
                for movie, ratings in movie_ratings.items()
                for film in self.data_movies
                if film["movieId"] == movie
            }
            top_movies = dict(
                sorted(movie_metrics.items(), key=lambda item: -item[1])[:n]
            )
            return top_movies

        def top_controversial(self, n: int) -> dict[str:float]:
            if not isinstance(n, int) or n < 1:
                raise ValueError(f"Ошибка: '{n}' не является числом >= 0.")
            movie_ratings = defaultdict(list)
            for row in self.data_ratings:
                for film in self.data_movies:
                    if film["movieId"] == row["movieId"]:
                        movie_ratings[film["title"][:-7]].append(float(row["rating"]))
            movie_variances = {}
            for movie, ratings in movie_ratings.items():
                if len(ratings) < 2:
                    movie_variances[movie] = 0
                    continue
                mean = sum(ratings) / len(ratings)
                variance = sum([(x - mean) ** 2 for x in ratings]) / (len(ratings) - 1)
                movie_variances[movie] = round(variance, 2)
            top_movies = dict(
                sorted(movie_variances.items(), key=lambda item: -item[1])[:n]
            )
            return top_movies

    class Users(Movies):
        def user_by_num_of_ratings(self, n: int) -> dict[str:int]:
            if not isinstance(n, int) or n < 1:
                raise ValueError(f"Ошибка: '{n}' не является числом >= 0.")
            data = {}
            for row in self.data_ratings:
                if row["userId"] in data:
                    data[row["userId"]] += 1
                else:
                    data[row["userId"]] = 1
            sort_data = dict(sorted(data.items(), key=lambda item: -item[1])[:n])
            return sort_data

        def user_by_ratings(self, n: int, metric: str = "average") -> dict[str:float]:
            if not isinstance(n, int) or n < 1:
                raise ValueError("Ошибка: n не является числом >= 0.")
            if not isinstance(metric, str) or metric not in ["average", "median"]:
                raise ValueError("Ошибка: metric не со значением average или median.")
            if metric == "average":
                metric_func = lambda ratings: (sum(ratings) / len(ratings))
            else:
                metric_func = lambda ratings: (sorted(ratings)[len(ratings) // 2])
            user_ratings = defaultdict(list)
            for row in self.data_ratings:
                user_ratings[row["userId"]].append(float(row["movieId"]))
            user_metrics = {
                user: round(metric_func(ratings), 2)
                for user, ratings in user_ratings.items()
            }
            result = dict(sorted(user_metrics.items(), key=lambda item: -item[1])[:n])
            return result

        def user_controversial(self, n: int) -> dict[str:float]:
            if not isinstance(n, int) or n < 1:
                raise ValueError(f"Ошибка: '{n}' не является числом >= 0.")
            user_ratings = defaultdict(list)
            for row in self.data_ratings:
                user_ratings[row["userId"]].append(float(row["rating"]))

            user_variances = {}
            for user, ratings in user_ratings.items():
                if len(ratings) < 2:
                    user_variances[user] = 0
                    continue

                mean = sum(ratings) / len(ratings)
                variance = sum([(x - mean) ** 2 for x in ratings]) / (len(ratings) - 1)
                user_variances[user] = round(variance, 2)

            top_user = dict(
                sorted(user_variances.items(), key=lambda item: -item[1])[:n]
            )
            return top_user


class Tags(Basic):
    def __init__(self, path_to_the_file: str = "tags.csv", lines: int = 3683):
        super().__init__(path_to_the_file, lines)
        self.data = super().read_csv()
        self.tags = [x["tag"] for x in self.data]
        self.unique_tags = set(self.tags)

    def most_words(self, n: int) -> dict[str:int]:
        if not isinstance(n, int) or n < 1:
            raise ValueError(f"Ошибка: '{n}' не является числом >= 0.")
        count = {x: len(x.split()) for x in self.unique_tags}
        big_tags = dict(sorted(count.items(), key=lambda item: -item[1])[:n])
        return big_tags

    def longest(self, n: int) -> list[str]:
        if not isinstance(n, int) or n < 1:
            raise ValueError(f"Ошибка: '{n}' не является числом >= 0.")
        big_tags = sorted(self.unique_tags, key=len, reverse=True)[:n]
        return big_tags

    def most_words_and_longest(self, n: int) -> list[str]:
        if not isinstance(n, int) or n < 1:
            raise ValueError(f"Ошибка: '{n}' не является числом >= 0.")
        most_words = self.most_words(n)
        longest = self.longest(n)
        big_tags = []
        for i in most_words:
            if i in longest:
                big_tags.append(i)
        return big_tags

    def most_popular(self, n: int) -> dict[str:int]:
        if not isinstance(n, int) or n < 1:
            raise ValueError(f"Ошибка: '{n}' не является числом >= 0.")
        popular_tags = dict(
            sorted(Counter(self.tags).items(), key=lambda item: -item[1])[:n]
        )
        return popular_tags

    def tags_with(self, word: str) -> list[str]:
        if not isinstance(word, str):
            raise ValueError(f"Ошибка: '{word}' не является строкой")
        tags_with_word = sorted(
            (tag for tag in self.unique_tags if word.lower() in tag.lower()),
            key=str.lower,
        )
        return tags_with_word


class Tests:
    @pytest.mark.parametrize(
        "filename, line, res, expectation",
        [
            (
                "tags.csv",
                2,
                [
                    {
                        "userId": "2",
                        "movieId": "60756",
                        "tag": "funny",
                        "timestamp": "1445714994",
                    },
                    {
                        "userId": "2",
                        "movieId": "60756",
                        "tag": "Highly quotable",
                        "timestamp": "1445714996",
                    },
                ],
                nullcontext(),
            ),
            (21, 2, None, pytest.raises(ValueError)),
            ("123.txt", 2, None, pytest.raises(FileNotFoundError)),
            ("tags.csv", 0, None, pytest.raises(ValueError)),
            ("tags.csv", "sber", None, pytest.raises(ValueError)),
        ],
    )
    def test_read_csv(self, filename, line, res, expectation):
        with expectation:
            assert Basic(filename, line).read_csv() == res

    class TestLinks:
        @pytest.fixture
        def links(self):
            return Links(lines=5).read_csv()

        def test_read_csv(self, links):
            assert type(links).__name__ == "list"
            for line in links:
                assert type(line).__name__ == "dict"

        def test_data_title(self, links):
            title = ["movieId", "imdbId", "tmdbId"]
            for line in links:
                assert list(line.keys()) == title
                assert line["movieId"].isdigit() == True
                assert line["imdbId"].isdigit() == True
                assert line["tmdbId"].isdigit() == True
                assert ("" in list(line.values())) == False

        def test_data_imdb(self):
            assert Links(lines=2).imdb_info == [
                [
                    1,
                    ["John Lasseter"],
                    30000000,
                    394436586,
                    81,
                    8.3,
                    723,
                    "История игрушек",
                ],
                [
                    2,
                    ["Joe Johnston"],
                    65000000,
                    262821940,
                    104,
                    7.1,
                    960,
                    "Джуманджи",
                ],
            ]

        @pytest.mark.parametrize(
            "line, n, res1, res2, res3, res4, res5, res6, res7, res8, expectation",
            [
                (
                    5,
                    2,
                    {"John Lasseter": 1, "Joe Johnston": 1},
                    {"Джуманджи": 65000000, "История игрушек": 30000000},
                    {"История игрушек": 394436586, "Джуманджи": 262821940},
                    {"История игрушек": 364436586, "Джуманджи": 197821940},
                    {"В ожидании выдоха": 124, "Отец невесты 2": 106},
                    {"Джуманджи": 625000.0, "История игрушек": 370370.37},
                    {"История игрушек": 8.3, "Джуманджи": 7.1},
                    {"История игрушек": 723, "Джуманджи": 960},
                    nullcontext(),
                ),
                (
                    2,
                    0,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    pytest.raises(ValueError),
                ),
                (
                    2,
                    "sber",
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    pytest.raises(ValueError),
                ),
            ],
        )
        def test_func(
            self, line, n, res1, res2, res3, res4, res5, res6, res7, res8, expectation
        ):
            with expectation:
                assert Links(lines=line).top_directors(n) == res1
                assert Links(lines=line).most_expensive(n) == res2
                assert Links(lines=line).most_total_collection(n) == res3
                assert Links(lines=line).most_profitable(n) == res4
                assert Links(lines=line).longest(n) == res5
                assert Links(lines=line).top_cost_per_minute(n) == res6
                assert Links(lines=line).most_ratings(n) == res7
                assert Links(lines=line).most_popularity(n) == res8

    class TestMovies:
        @pytest.fixture
        def movies(self):
            return Movies(lines=10).read_csv()

        def test_read_csv(self, movies):
            assert type(movies).__name__ == "list"
            for line in movies:
                assert type(line).__name__ == "dict"

        def test_data(self, movies):
            title = ["movieId", "title", "genres"]
            for line in movies:
                assert list(line.keys()) == title
                assert line["movieId"].isdigit() == True
                assert isinstance(line["title"], str) == True
                assert isinstance(line["genres"], str) == True
                assert ("" in list(line.values())) == False

        @pytest.mark.parametrize(
            "line1, line2, line3, n, res1, res2, res3, expectation",
            [
                (
                    100,
                    10,
                    50,
                    3,
                    {1995: 74, 1996: 22, 1994: 3, 1976: 1},
                    {
                        "Comedy": 5,
                        "Adventure": 4,
                        "Children": 3,
                        "Romance": 3,
                        "Action": 3,
                        "Fantasy": 2,
                        "Thriller": 2,
                        "Animation": 1,
                        "Drama": 1,
                        "Crime": 1,
                    },
                    {"Drama": 27, "Comedy": 16, "Romance": 13},
                    nullcontext(),
                ),
                (
                    10,
                    5,
                    50,
                    0,
                    {1995: 10},
                    {
                        "Comedy": 4,
                        "Adventure": 2,
                        "Children": 2,
                        "Fantasy": 2,
                        "Romance": 2,
                        "Animation": 1,
                        "Drama": 1,
                    },
                    None,
                    pytest.raises(ValueError),
                ),
            ],
        )
        def test_func(self, line1, line2, line3, n, res1, res2, res3, expectation):
            with expectation:
                assert Movies(lines=line1).dist_by_release() == res1
                assert Movies(lines=line2).dist_by_genres() == res2
                assert Movies(lines=line3).most_genres(n) == res3

    class TestRatings:
        @pytest.fixture
        def ratings(self):
            return Ratings(lines=500).read_csv()

        @pytest.fixture
        def movies(self):
            return Movies(lines=1000).read_csv()

        def test_read_csv(self, ratings):
            assert type(ratings).__name__ == "list"
            for line in ratings:
                assert type(line).__name__ == "dict"

        def test_data(self, ratings):
            title = ["userId", "movieId", "rating", "timestamp"]
            for line in ratings:
                assert list(line.keys()) == title
                assert line["userId"].isdigit() == True
                assert line["movieId"].isdigit() == True
                assert (
                    len(line["rating"].split(".")) == 2
                    and line["rating"].split(".")[0].isdigit() == True
                    and line["rating"].split(".")[1].isdigit() == True
                )
                assert line["timestamp"].isdigit() == True
                assert ("" in list(line.values())) == False

        def test_dist_movies(self, ratings, movies):
            assert Ratings(lines=500).Movies(ratings, movies).dist_by_year() == {
                2015: 29,
                2011: 39,
                2001: 54,
                2000: 296,
                1999: 82,
            }
            assert Ratings(lines=500).Movies(ratings, movies).dist_by_rating() == {
                0.5: 20,
                1.0: 22,
                2.0: 31,
                2.5: 1,
                3.0: 66,
                3.5: 5,
                4.0: 145,
                4.5: 9,
                5.0: 201,
            }

        @pytest.mark.parametrize(
            "n, metric, res1, res2, res3, expectation",
            [
                (
                    3,
                    "average",
                    {
                        "Seven (a.k.a. Se7en)": 2,
                        "Ed Wood": 2,
                        "Star Wars: Episode IV - A New Hope": 2,
                    },
                    {"Usual Suspects The": 5.0, "Bottle Rocket": 5.0, "Rob Roy": 5.0},
                    {
                        "Schindler's List": 10.12,
                        "My Fair Lady": 10.12,
                        "Seven (a.k.a. Se7en)": 4.5,
                    },
                    nullcontext(),
                ),
                (0, "median", None, None, None, pytest.raises(ValueError)),
                (
                    3,
                    21,
                    {
                        "Seven (a.k.a. Se7en)": 2,
                        "Ed Wood": 2,
                        "Star Wars: Episode IV - A New Hope": 2,
                    },
                    None,
                    None,
                    pytest.raises(ValueError),
                ),
            ],
        )
        def test_top_movies(
            self, ratings, movies, n, metric, res1, res2, res3, expectation
        ):
            with expectation:
                assert (
                    Ratings(lines=500).Movies(ratings, movies).top_by_num_of_ratings(n)
                    == res1
                )
                assert (
                    Ratings(lines=500).Movies(ratings, movies).top_by_ratings(n, metric)
                    == res2
                )
                assert (
                    Ratings(lines=500).Movies(ratings, movies).top_controversial(n)
                    == res3
                )

        @pytest.mark.parametrize(
            "n, metric, res1, res2, res3, expectation",
            [
                (
                    3,
                    "median",
                    {"1": 232, "4": 200, "3": 39},
                    {"2": 79132.0, "3": 2288.0, "1": 1967.0},
                    {"3": 4.37, "4": 1.73, "2": 0.65},
                    nullcontext(),
                ),
                (
                    0,
                    "median",
                    None,
                    None,
                    None,
                    pytest.raises(ValueError),
                ),
                (
                    3,
                    "sber",
                    {"1": 232, "4": 200, "3": 39},
                    None,
                    None,
                    pytest.raises(ValueError),
                ),
            ],
        )
        def test_top_user(
            self, ratings, movies, n, metric, res1, res2, res3, expectation
        ):
            with expectation:
                assert (
                    Ratings(lines=1000).Users(ratings, movies).user_by_num_of_ratings(n)
                    == res1
                )
                assert (
                    Ratings(lines=1000)
                    .Users(ratings, movies)
                    .user_by_ratings(n, metric)
                    == res2
                )
                assert (
                    Ratings(lines=1000).Users(ratings, movies).user_controversial(n)
                    == res3
                )

    class TestTags:
        @pytest.fixture
        def tags(self):
            return Tags(lines=15).read_csv()

        def test_read_csv(self, tags):
            assert type(tags).__name__ == "list"
            for line in tags:
                assert type(line).__name__ == "dict"

        def test_data(self, tags):
            title = ["userId", "movieId", "tag", "timestamp"]
            for line in tags:
                assert list(line.keys()) == title
                assert line["userId"].isdigit() == True
                assert line["movieId"].isdigit() == True
                assert isinstance(line["tag"], str) == True
                assert line["timestamp"].isdigit() == True
                assert ("" in list(line.values())) == False

        @pytest.mark.parametrize(
            "line, n, word, res1, res2, res3, res4, res5, expectation",
            [
                (
                    30,
                    2,
                    "leo",
                    {"indie record label": 3, "way too long": 3},
                    ["indie record label", "Leonardo DiCaprio"],
                    ["indie record label"],
                    {"Al Pacino": 2, "twist ending": 2},
                    ["Leonardo DiCaprio"],
                    nullcontext(),
                ),
                (
                    30,
                    0,
                    "leo",
                    None,
                    None,
                    None,
                    None,
                    ["Leonardo DiCaprio"],
                    pytest.raises(ValueError),
                ),
                (
                    30,
                    2,
                    21,
                    {"indie record label": 3, "way too long": 3},
                    ["indie record label", "Leonardo DiCaprio"],
                    ["indie record label"],
                    {"Al Pacino": 2, "twist ending": 2},
                    None,
                    pytest.raises(ValueError),
                ),
            ],
        )
        def test_func(self, line, n, word, res1, res2, res3, res4, res5, expectation):
            with expectation:
                assert Tags(lines=line).most_words(n) == res1
                assert Tags(lines=line).longest(n) == res2
                assert Tags(lines=line).most_words_and_longest(n) == res3
                assert Tags(lines=line).most_popular(n) == res4
                assert Tags(lines=line).tags_with(word) == res5


if __name__ == '__main__':
    print(Links(lines=3).imdb_info)