"""
Module for representing Codeforces API response structures.

This module defines data classes that encapsulate the responses received from the Codeforces API.
Each response type is defined as a subclass of InteractionResponse, incorporating the API's response
status, an optional comment, and a result payload that can either be a single object or a list of objects.

Classes
-------
InteractionResponse
    Base response structure containing status and an optional comment.
UserInteractionResponse
    Response for user-related interactions.
BlogEntryCommentResponse
    Response for blog entry comments.
BlogEntryViewResponse
    Response for viewing a blog entry.
ContestHacksResponse
    Response for contest hacks.
ContestListResponse
    Response for contest lists.
ContestRatingChangeResponse
    Response for contest rating changes.
ContestStandingResponse
    Response for contest standings.
ContestStatusResponse
    Response for contest submissions.
ProblemSetProblemsResponse
    Response for problem set problems.
ProblemSetRecentStatusResponse
    Response for recent problem set submissions.
RecentActionsResponse
    Response for recent actions.
UserBlogEntryResponse
    Response for user blog entries.
UserFriendResponse
    Response for user friends.
UserRatedListResponse
    Response for user rated list.
UserRatingResponse
    Response for user rating history.
UserStatusResponse
    Response for user submissions.
"""

import msgspec
import typing as t
import codeforcespy.abc.objects as cf_objects
import codeforcespy.abc.cobjects as cf_cobjects


class InteractionResponse(msgspec.Struct):
    """
    Base response structure for Codeforces API interactions.

    Attributes
    ----------
    status : str
        The status of the API interaction.
    comment : Optional[str]
        An optional comment associated with the response.
    """

    status: str
    comment: t.Optional[str] = None


class UserInteractionResponse(InteractionResponse):
    """
    Response structure for user-related interactions.

    Attributes
    ----------
    result : Optional[Union[List[cf_objects.User], cf_objects.User]]
        A single user or a list of users returned by the API.
    """

    result: t.Optional[t.Union[t.List[cf_objects.User], cf_objects.User]] = None


class BlogEntryCommentResponse(InteractionResponse):
    """
    Response structure for blog entry comments.

    Attributes
    ----------
    result : Optional[Union[List[cf_objects.Comment], cf_objects.Comment]]
        A single comment or a list of comments returned by the API.
    """

    result: t.Optional[t.Union[t.List[cf_objects.Comment], cf_objects.Comment]] = None


class BlogEntryViewResponse(InteractionResponse):
    """
    Response structure for viewing a blog entry.

    Attributes
    ----------
    result : Optional[Union[List[cf_objects.BlogEntry], cf_objects.BlogEntry]]
        A single blog entry or a list of blog entries returned by the API.
    """

    result: t.Optional[t.Union[t.List[cf_objects.BlogEntry], cf_objects.BlogEntry]] = (
        None
    )


class ContestHacksResponse(InteractionResponse):
    """
    Response structure for contest hacks.

    Attributes
    ----------
    result : Optional[Union[List[cf_objects.Hack], cf_objects.Hack]]
        A single hack or a list of hacks returned by the API.
    """

    result: t.Optional[t.Union[t.List[cf_objects.Hack], cf_objects.Hack]] = None


class ContestListResponse(InteractionResponse):
    """
    Response structure for contest lists.

    Attributes
    ----------
    result : Optional[Union[List[cf_objects.Contest], cf_objects.Contest]]
        A single contest or a list of contests returned by the API.
    """

    result: t.Optional[t.Union[t.List[cf_objects.Contest], cf_objects.Contest]] = None


class ContestRatingChangeResponse(InteractionResponse):
    """
    Response structure for contest rating changes.

    Attributes
    ----------
    result : Optional[Union[List[cf_objects.RatingChange], cf_objects.RatingChange]]
        A single rating change or a list of rating changes returned by the API.
    """

    result: t.Optional[
        t.Union[t.List[cf_objects.RatingChange], cf_objects.RatingChange]
    ] = None


class ContestStandingResponse(InteractionResponse):
    """
    Response structure for contest standings.

    Attributes
    ----------
    result : Optional[Union[List[cf_cobjects.Standings], cf_cobjects.Standings]]
        A single standings object or a list of standings objects returned by the API.
    """

    result: t.Optional[
        t.Union[t.List[cf_cobjects.Standings], cf_cobjects.Standings]
    ] = None


class ContestStatusResponse(InteractionResponse):
    """
    Response structure for contest submissions.

    Attributes
    ----------
    result : Optional[Union[List[cf_objects.Submission], cf_objects.Submission]]
        A single submission or a list of submissions returned by the API.
    """

    result: t.Optional[
        t.Union[t.List[cf_objects.Submission], cf_objects.Submission]
    ] = None


class ProblemSetProblemsResponse(InteractionResponse):
    """
    Response structure for problem set problems.

    Attributes
    ----------
    result : Optional[Union[List[cf_cobjects.ProblemSetProblems], cf_cobjects.ProblemSetProblems]]
        A single problem set problems object or a list of such objects returned by the API.
    """

    result: t.Optional[
        t.Union[t.List[cf_cobjects.ProblemSetProblems], cf_cobjects.ProblemSetProblems]
    ] = None


class ProblemSetRecentStatusResponse(InteractionResponse):
    """
    Response structure for recent problem set submissions.

    Attributes
    ----------
    result : Optional[Union[List[cf_objects.Submission], cf_objects.Submission]]
        A single submission or a list of submissions returned by the API.
    """

    result: t.Optional[
        t.Union[t.List[cf_objects.Submission], cf_objects.Submission]
    ] = None


class RecentActionsResponse(InteractionResponse):
    """
    Response structure for recent actions.

    Attributes
    ----------
    result : Optional[Union[List[cf_objects.RecentAction], cf_objects.RecentAction]]
        A single recent action or a list of recent actions returned by the API.
    """

    result: t.Optional[
        t.Union[t.List[cf_objects.RecentAction], cf_objects.RecentAction]
    ] = None


class UserBlogEntryResponse(InteractionResponse):
    """
    Response structure for user blog entries.

    Attributes
    ----------
    result : Optional[Union[List[cf_objects.BlogEntry], cf_objects.BlogEntry]]
        A single blog entry or a list of blog entries returned by the API.
    """

    result: t.Optional[t.Union[t.List[cf_objects.BlogEntry], cf_objects.BlogEntry]] = (
        None
    )


class UserFriendResponse(InteractionResponse):
    """
    Response structure for user friends.

    Attributes
    ----------
    result : Optional[Union[List[str], str]]
        A single friend (user handle) or a list of user handles returned by the API.
    """

    result: t.Optional[t.Union[t.List[str], str]] = None


class UserRatedListResponse(InteractionResponse):
    """
    Response structure for the user rated list.

    Attributes
    ----------
    result : Optional[Union[List[cf_objects.User], cf_objects.User]]
        A single user or a list of users in the rated list returned by the API.
    """

    result: t.Optional[t.Union[t.List[cf_objects.User], cf_objects.User]] = None


class UserRatingResponse(InteractionResponse):
    """
    Response structure for user rating history.

    Attributes
    ----------
    result : Optional[Union[List[cf_objects.RatingChange], cf_objects.RatingChange]]
        A single rating change or a list of rating changes returned by the API.
    """

    result: t.Optional[
        t.Union[t.List[cf_objects.RatingChange], cf_objects.RatingChange]
    ] = None


class UserStatusResponse(InteractionResponse):
    """
    Response structure for user submissions.

    Attributes
    ----------
    result : Optional[Union[List[cf_objects.Submission], cf_objects.Submission]]
        A single submission or a list of submissions returned by the API.
    """

    result: t.Optional[
        t.Union[t.List[cf_objects.Submission], cf_objects.Submission]
    ] = None
