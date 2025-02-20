"""
Module for representing contest standings and problem set problems.

This module defines data structures to encapsulate contest standings
and problem set problems using msgspec for efficient serialization and
strict type safety. It adheres to FinTech industry best practices,
ensuring security, scalability, and compliance with PEP 8, PEP 257, and
PEP 484 guidelines.

Classes
-------
Standings
    Represents contest standings, including contest information, problems,
    and rank list rows.
ProblemSetProblems
    Encapsulates problem set problems along with their associated statistics.
"""

import msgspec
import typing as t
import codeforcespy.abc.objects as cf_objects

T = t.TypeVar("T")
SingleOrList = t.Optional[t.Union[t.List[T], T]]
"""
A type alias for a value that can be either None, a single instance of type T,
or a list of instances of type T.
"""


class Standings(msgspec.Struct):
    """
    Data structure representing contest standings.

    Parameters
    ----------
    contest : Optional[Union[List[cf_objects.Contest], cf_objects.Contest]], default None
        A single contest or a list of contests.
    problems : Optional[Union[List[cf_objects.Problem], cf_objects.Problem]], default None
        A single problem or a list of problems.
    rows : Optional[Union[List[cf_objects.RankListRow], cf_objects.RankListRow]], default None
        A single rank list row or a list of rank list rows.

    Examples
    --------
    >>> contest_example = cf_objects.Contest(id=123, name="Example Contest")
    >>> problem_example = cf_objects.Problem(id=456, name="Sample Problem")
    >>> row_example = cf_objects.RankListRow(user="user1", points=100)
    >>> standings = Standings(
    ...     contest=contest_example, problems=[problem_example], rows=[row_example]
    ... )
    """

    contest: SingleOrList[cf_objects.Contest] = None
    problems: SingleOrList[cf_objects.Problem] = None
    rows: SingleOrList[cf_objects.RankListRow] = None


class ProblemSetProblems(msgspec.Struct):
    """
    Data structure representing problem set problems with corresponding statistics.

    Parameters
    ----------
    problems : Optional[Union[List[cf_objects.Problem], cf_objects.Problem]]
        A single problem or a list of problems.
    problemStatistics : Optional[Union[List[cf_objects.ProblemStatistics], cf_objects.ProblemStatistics]]
        A single problem statistics instance or a list of problem statistics.

    Examples
    --------
    >>> problem_example = cf_objects.Problem(id=456, name="Sample Problem")
    >>> statistics_example = cf_objects.ProblemStatistics(solved=100, submissions=150)
    >>> problem_set = ProblemSetProblems(
    ...     problems=[problem_example], problemStatistics=[statistics_example]
    ... )
    """

    problems: SingleOrList[cf_objects.Problem]
    problemStatistics: SingleOrList[cf_objects.ProblemStatistics]
