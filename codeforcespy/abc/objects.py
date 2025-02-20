"""
Module for Codeforces API Data Structures

This module defines the data structures representing various entities returned by
the Codeforces API. These entities include users, blog entries, comments, contests,
submissions, hacks, and more. Each class is implemented as a subclass of
`msgspec.Struct` to ensure efficient serialization, strict type safety, and clear
adherence to Python Enhancement Proposals (PEP 8, PEP 257, and PEP 484).

Classes
-------
User
    Represents a Codeforces user.
Member
    Represents a member of a party.
BlogEntry
    Represents a Codeforces blog entry.
Comment
    Represents a comment.
RecentAction
    Represents a recent action.
RatingChange
    Represents a user's rating change after a contest.
Contest
    Represents a contest.
Party
    Represents a party participating in a contest.
Problem
    Represents a problem.
ProblemStatistics
    Represents statistics data for a problem.
Submission
    Represents a submission.
Hack
    Represents a hack attempt during a contest.
ProblemResult
    Represents a party's result for a specific problem.
RankListRow
    Represents a row in the contest ranklist.
"""

import msgspec
import typing as t


class User(msgspec.Struct):
    """
    Represents a Codeforces user.

    Attributes
    ----------
    handle : t.Optional[str]
        Codeforces user handle.
    vkId : t.Optional[str]
        User ID for the VK social network (if shared).
    openId : t.Optional[str]
        OpenID identifier (if shared).
    firstName : t.Optional[str]
        Localized first name of the user.
    lastName : t.Optional[str]
        Localized last name of the user.
    country : t.Optional[str]
        Localized country of the user.
    city : t.Optional[str]
        Localized city of the user.
    organization : t.Optional[str]
        Localized organization of the user.
    contribution : t.Optional[int]
        User's contribution to the Codeforces community.
    rank : t.Optional[str]
        Localized rank of the user.
    rating : t.Optional[int]
        User's rating in the Codeforces community.
    maxRank : t.Optional[str]
        Localized maximum rank achieved by the user.
    maxRating : t.Optional[int]
        Maximum rating achieved by the user.
    lastOnlineTimeSeconds : t.Optional[int]
        Unix timestamp indicating when the user was last online.
    registrationTimeSeconds : t.Optional[int]
        Unix timestamp of the user's registration.
    friendOfCount : t.Optional[int]
        Number of users who have this user in their friends list.
    avatar : t.Optional[str]
        URL of the user's avatar.
    titlePhoto : t.Optional[str]
        URL of the user's title photo.
    email : t.Optional[str]
        Email address (shared if permitted).
    """

    handle: t.Optional[str] = None
    vkId: t.Optional[str] = None
    openId: t.Optional[str] = None
    firstName: t.Optional[str] = None
    lastName: t.Optional[str] = None
    country: t.Optional[str] = None
    city: t.Optional[str] = None
    organization: t.Optional[str] = None
    contribution: t.Optional[int] = None
    rank: t.Optional[str] = None
    rating: t.Optional[int] = None
    maxRank: t.Optional[str] = None
    maxRating: t.Optional[int] = None
    lastOnlineTimeSeconds: t.Optional[int] = None
    registrationTimeSeconds: t.Optional[int] = None
    friendOfCount: t.Optional[int] = None
    avatar: t.Optional[str] = None
    titlePhoto: t.Optional[str] = None
    email: t.Optional[str] = None


class Member(msgspec.Struct):
    """
    Represents a member of a party.

    Attributes
    ----------
    handle : str
        Codeforces user handle.
    name : t.Optional[str]
        User's name (if available).
    """

    handle: str
    name: t.Optional[str] = None


class BlogEntry(msgspec.Struct):
    """
    Represents a Codeforces blog entry.

    Attributes
    ----------
    id : t.Optional[int]
        Unique identifier for the blog entry.
    originalLocale : t.Optional[str]
        Original locale of the blog entry.
    creationTimeSeconds : t.Optional[int]
        Unix timestamp when the blog entry was created.
    authorHandle : t.Optional[str]
        User handle of the blog entry author.
    title : t.Optional[str]
        Localized title of the blog entry.
    content : t.Optional[str]
        Localized content of the blog entry (omitted in the short version).
    locale : t.Optional[str]
        Locale of the blog entry.
    modificationTimeSeconds : t.Optional[int]
        Unix timestamp when the blog entry was last modified.
    allowViewHistory : t.Optional[bool]
        Indicates if viewing the history of the blog entry is permitted.
    tags : t.Optional[t.List[str]]
        List of tags associated with the blog entry.
    rating : t.Optional[int]
        Rating of the blog entry.
    """

    id: t.Optional[int] = None
    originalLocale: t.Optional[str] = None
    creationTimeSeconds: t.Optional[int] = None
    authorHandle: t.Optional[str] = None
    title: t.Optional[str] = None
    content: t.Optional[str] = None
    locale: t.Optional[str] = None
    modificationTimeSeconds: t.Optional[int] = None
    allowViewHistory: t.Optional[bool] = None
    tags: t.Optional[t.List[str]] = None
    rating: t.Optional[int] = None


class Comment(msgspec.Struct):
    """
    Represents a comment on Codeforces.

    Attributes
    ----------
    id : t.Optional[int]
        Unique identifier for the comment.
    creationTimeSeconds : t.Optional[int]
        Unix timestamp when the comment was created.
    commentatorHandle : t.Optional[str]
        Handle of the user who posted the comment.
    locale : t.Optional[str]
        Locale of the comment.
    text : t.Optional[str]
        Text content of the comment.
    parentCommentId : t.Optional[int]
        Identifier of the parent comment (if any).
    rating : t.Optional[int]
        Rating of the comment.
    """

    id: t.Optional[int] = None
    creationTimeSeconds: t.Optional[int] = None
    commentatorHandle: t.Optional[str] = None
    locale: t.Optional[str] = None
    text: t.Optional[str] = None
    parentCommentId: t.Optional[int] = None
    rating: t.Optional[int] = None


class RecentAction(msgspec.Struct):
    """
    Represents a recent action on Codeforces.

    Attributes
    ----------
    timeSeconds : t.Optional[int]
        Unix timestamp of the action.
    blogEntry : t.Optional[BlogEntry]
        Associated blog entry (short version), if applicable.
    comment : t.Optional[Comment]
        Associated comment, if applicable.
    """

    timeSeconds: t.Optional[int] = None
    blogEntry: t.Optional[BlogEntry] = None
    comment: t.Optional[Comment] = None


class RatingChange(msgspec.Struct):
    """
    Represents a user's rating change after participating in a contest.

    Attributes
    ----------
    contestId : t.Optional[int]
        Identifier of the contest.
    contestName : t.Optional[str]
        Localized name of the contest.
    handle : t.Optional[str]
        Codeforces user handle.
    rank : t.Optional[int]
        User's rank during the contest.
    ratingUpdateTimeSeconds : t.Optional[int]
        Unix timestamp when the rating was updated.
    oldRating : t.Optional[int]
        User's rating before the contest.
    newRating : t.Optional[int]
        User's rating after the contest.
    """

    contestId: t.Optional[int] = None
    contestName: t.Optional[str] = None
    handle: t.Optional[str] = None
    rank: t.Optional[int] = None
    ratingUpdateTimeSeconds: t.Optional[int] = None
    oldRating: t.Optional[int] = None
    newRating: t.Optional[int] = None


class Contest(msgspec.Struct):
    """
    Represents a contest on Codeforces.

    Attributes
    ----------
    id : t.Optional[int]
        Contest identifier.
    name : t.Optional[str]
        Localized name of the contest.
    type : t.Optional[str]
        Contest type (e.g., 'CF', 'IOI', 'ICPC').
    phase : t.Optional[str]
        Current contest phase (e.g., 'BEFORE', 'CODING', 'FINISHED').
    frozen : t.Optional[bool]
        Indicates if the contest ranklist is frozen.
    durationSeconds : t.Optional[int]
        Contest duration in seconds.
    startTimeSeconds : t.Optional[int]
        Unix timestamp of the contest start.
    relativeTimeSeconds : t.Optional[int]
        Seconds elapsed since the contest start (may be negative).
    preparedBy : t.Optional[str]
        Handle of the contest creator.
    websiteUrl : t.Optional[str]
        URL of the contest-related website.
    description : t.Optional[str]
        Localized description of the contest.
    difficulty : t.Optional[int]
        Difficulty rating (scale from 1 to 5).
    kind : t.Optional[str]
        Localized, human-readable contest type.
    icpcRegion : t.Optional[str]
        Localized region name for official ICPC contests.
    country : t.Optional[str]
        Localized country name.
    city : t.Optional[str]
        Localized city name.
    season : t.Optional[str]
        Contest season.
    """

    id: t.Optional[int] = None
    name: t.Optional[str] = None
    type: t.Optional[str] = None
    phase: t.Optional[str] = None
    frozen: t.Optional[bool] = None
    durationSeconds: t.Optional[int] = None
    startTimeSeconds: t.Optional[int] = None
    relativeTimeSeconds: t.Optional[int] = None
    preparedBy: t.Optional[str] = None
    websiteUrl: t.Optional[str] = None
    description: t.Optional[str] = None
    difficulty: t.Optional[int] = None
    kind: t.Optional[str] = None
    icpcRegion: t.Optional[str] = None
    country: t.Optional[str] = None
    city: t.Optional[str] = None
    season: t.Optional[str] = None


class Party(msgspec.Struct):
    """
    Represents a party participating in a contest.

    Attributes
    ----------
    contestId : t.Optional[int]
        Identifier of the contest (if applicable).
    members : t.Optional[t.List[Member]]
        List of party members.
    participantType : t.Optional[str]
        Participant type (e.g., 'CONTESTANT', 'PRACTICE', 'VIRTUAL').
    teamId : t.Optional[int]
        Unique team identifier (if the party is a team).
    teamName : t.Optional[str]
        Localized team name (if the party is a team or ghost).
    ghost : t.Optional[bool]
        Indicates if the party is a ghost (participated off Codeforces).
    room : t.Optional[int]
        Room number (if assigned).
    startTimeSeconds : t.Optional[int]
        Unix timestamp when the party started the contest.
    """

    contestId: t.Optional[int] = None
    members: t.Optional[t.List[Member]] = None
    participantType: t.Optional[str] = None
    teamId: t.Optional[int] = None
    teamName: t.Optional[str] = None
    ghost: t.Optional[bool] = None
    room: t.Optional[int] = None
    startTimeSeconds: t.Optional[int] = None


class Problem(msgspec.Struct):
    """
    Represents a problem on Codeforces.

    Attributes
    ----------
    contestId : t.Optional[int]
        Identifier of the contest containing the problem.
    problemsetName : t.Optional[str]
        Short name of the problemset to which the problem belongs.
    index : t.Optional[str]
        Problem index (typically a letter or letter-number combination).
    name : t.Optional[str]
        Localized name of the problem.
    type : t.Optional[str]
        Problem type (e.g., 'PROGRAMMING', 'QUESTION').
    points : t.Optional[float]
        Maximum points achievable for the problem.
    rating : t.Optional[int]
        Difficulty rating of the problem.
    tags : t.Optional[t.List[str]]
        List of tags associated with the problem.
    """

    contestId: t.Optional[int] = None
    problemsetName: t.Optional[str] = None
    index: t.Optional[str] = None
    name: t.Optional[str] = None
    type: t.Optional[str] = None
    points: t.Optional[float] = None
    rating: t.Optional[int] = None
    tags: t.Optional[t.List[str]] = None


class ProblemStatistics(msgspec.Struct):
    """
    Represents statistical data for a problem.

    Attributes
    ----------
    contestId : t.Optional[int]
        Identifier of the contest containing the problem.
    index : t.Optional[str]
        Problem index (typically a letter or letter-number combination).
    solvedCount : t.Optional[int]
        Number of users who solved the problem.
    """

    contestId: t.Optional[int] = None
    index: t.Optional[str] = None
    solvedCount: t.Optional[int] = None


class Submission(msgspec.Struct):
    """
    Represents a submission made on Codeforces.

    Attributes
    ----------
    id : int
        Unique identifier for the submission.
    contestId : t.Optional[int]
        Identifier of the contest (if applicable).
    creationTimeSeconds : t.Optional[int]
        Unix timestamp when the submission was created.
    relativeTimeSeconds : t.Optional[int]
        Seconds elapsed from contest start to the submission.
    problem : t.Optional[Problem]
        Problem associated with the submission.
    author : t.Optional[Party]
        Party that made the submission.
    programmingLanguage : t.Optional[str]
        Programming language used for the submission.
    verdict : t.Optional[str]
        Verdict of the submission (e.g., 'OK', 'WRONG_ANSWER').
    testset : t.Optional[str]
        Testset used for judging (e.g., 'SAMPLES', 'PRETESTS').
    passedTestCount : t.Optional[int]
        Number of tests passed.
    timeConsumedMillis : t.Optional[int]
        Time consumed (in milliseconds) for one test.
    memoryConsumedBytes : t.Optional[int]
        Memory consumed (in bytes) for one test.
    points : t.Optional[float]
        Points scored (for IOI-like contests).
    """

    id: int
    contestId: t.Optional[int] = None
    creationTimeSeconds: t.Optional[int] = None
    relativeTimeSeconds: t.Optional[int] = None
    problem: t.Optional[Problem] = None
    author: t.Optional[Party] = None
    programmingLanguage: t.Optional[str] = None
    verdict: t.Optional[str] = None
    testset: t.Optional[str] = None
    passedTestCount: t.Optional[int] = None
    timeConsumedMillis: t.Optional[int] = None
    memoryConsumedBytes: t.Optional[int] = None
    points: t.Optional[float] = None


class Hack(msgspec.Struct):
    """
    Represents a hack attempt during a Codeforces contest.

    Attributes
    ----------
    id : int
        Unique identifier for the hack.
    creationTimeSeconds : int
        Unix timestamp when the hack was created.
    hacker : t.Optional[Party]
        Party that initiated the hack.
    defender : t.Optional[Party]
        Party that was defended against.
    verdict : t.Optional[str]
        Hack verdict (e.g., 'HACK_SUCCESSFUL', 'HACK_UNSUCCESSFUL').
    problem : t.Optional[Problem]
        Problem that was hacked.
    test : t.Optional[str]
        Test case details (if available).
    judgeProtocol : t.Optional[t.Dict[str, str]]
        Judge protocol details including keys such as 'manual', 'protocol', and 'verdict'.
    """

    id: int
    creationTimeSeconds: int
    hacker: t.Optional[Party] = None
    defender: t.Optional[Party] = None
    verdict: t.Optional[str] = None
    problem: t.Optional[Problem] = None
    test: t.Optional[str] = None
    judgeProtocol: t.Optional[t.Dict[str, str]] = None


class ProblemResult(msgspec.Struct):
    """
    Represents a party's result for a specific problem.

    Attributes
    ----------
    points : t.Optional[float]
        Points scored for the problem.
    penalty : t.Optional[int]
        Penalty incurred (in ICPC style) for the problem.
    rejectedAttemptCount : t.Optional[int]
        Number of incorrect submission attempts.
    type : t.Optional[str]
        Result type (e.g., 'PRELIMINARY', 'FINAL').
    bestSubmissionTimeSeconds : t.Optional[int]
        Seconds elapsed from contest start for the best submission.
    """

    points: t.Optional[float] = None
    penalty: t.Optional[int] = None
    rejectedAttemptCount: t.Optional[int] = None
    type: t.Optional[str] = None
    bestSubmissionTimeSeconds: t.Optional[int] = None


class RankListRow(msgspec.Struct):
    """
    Represents a row in the contest ranklist.

    Attributes
    ----------
    party : t.Optional[Party]
        Party corresponding to this ranklist row.
    rank : t.Optional[int]
        Rank position of the party.
    points : t.Optional[float]
        Total points scored by the party.
    penalty : t.Optional[int]
        Total penalty incurred by the party.
    successfulHackCount : t.Optional[int]
        Number of successful hacks performed by the party.
    unsuccessfulHackCount : t.Optional[int]
        Number of unsuccessful hacks performed by the party.
    problemResults : t.Optional[t.List[ProblemResult]]
        List of results for each problem (order corresponds to the problems list).
    lastSubmissionTimeSeconds : t.Optional[int]
        Unix timestamp of the last submission contributing to the score (for IOI contests).
    """

    party: t.Optional[Party] = None
    rank: t.Optional[int] = None
    points: t.Optional[float] = None
    penalty: t.Optional[int] = None
    successfulHackCount: t.Optional[int] = None
    unsuccessfulHackCount: t.Optional[int] = None
    problemResults: t.Optional[t.List[ProblemResult]] = None
    lastSubmissionTimeSeconds: t.Optional[int] = None
