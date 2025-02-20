"""
Module for synchronous and asynchronous Codeforces API clients.

This module provides two classes, SyncMethod and AsyncMethod, which allow for making
synchronous and asynchronous requests respectively to the Codeforces API. Both classes
feature optional authentication, strict type annotations, and comprehensive NumPy‐style
docstrings in adherence to FinTech industry best practices and Python Enhancement Proposals
(PEP 8, PEP 257, and PEP 484).

Classes
-------
SyncMethod
    Synchronous client for executing Codeforces API requests.
AsyncMethod
    Asynchronous client for executing Codeforces API requests.
"""

import time
import random
import typing as t
import hashlib
import collections
import urllib.parse
import msgspec

import codeforcespy.clients
import codeforcespy.abc.endpoints
import codeforcespy.abc.objects
import codeforcespy.abc.interactions
import codeforcespy.abc.cobjects


class SyncMethod:
    """
    Synchronous Codeforces API client for executing requests with optional authentication.

    Parameters
    ----------
    enable_auth : t.Optional[bool], optional
        Flag indicating whether authentication is enabled (default is False).
    auth_key : t.Optional[str], optional
        API authentication key to be used when authentication is enabled.
    unix_time : t.Optional[int], optional
        Unix timestamp to be used for request signing; if not provided, the current time is used.
    secret : t.Optional[str], optional
        API secret for signing requests when authentication is enabled.

    Attributes
    ----------
    _url_generator : pycodeforces.abc.endpoints.CodeForcesAPI
        Instance for generating API endpoint URLs.
    _client : pycodeforces.clients.SyncClient
        Synchronous HTTP client for making API requests.
    _auth_key : t.Optional[str]
        Authentication key for API requests.
    _secret : t.Optional[str]
        Secret key for request signing.
    _time : t.Optional[int]
        Unix timestamp used for request signing.
    _auth_enabled : bool
        Indicates if authentication is enabled.
    """

    def __init__(
        self,
        enable_auth: t.Optional[bool] = False,
        auth_key: t.Optional[str] = None,
        unix_time: t.Optional[int] = None,
        secret: t.Optional[str] = None,
    ) -> None:
        """
        Initialize the synchronous client.

        Parameters
        ----------
        enable_auth : t.Optional[bool], optional
            Whether to enable authentication (default is False).
        auth_key : t.Optional[str], optional
            API authentication key (default is None).
        unix_time : t.Optional[int], optional
            Unix timestamp for signing requests (default is None).
        secret : t.Optional[str], optional
            API secret for signing requests (default is None).
        """
        self._url_generator: codeforcespy.abc.endpoints.CodeForcesAPI = (
            codeforcespy.abc.endpoints.CodeForcesAPI()
        )
        self._client: codeforcespy.clients.SyncClient = (
            codeforcespy.clients.SyncClient()
        )
        self._auth_key: t.Optional[str] = auth_key
        self._secret: t.Optional[str] = secret
        self._time: t.Optional[int] = unix_time
        self._auth_enabled: bool = bool(enable_auth)

    def _generate_authorisation(
        self,
        end_point_url: str,
        method_name: t.Literal[
            "blogEntry.comments",
            "blogEntry.view",
            "contest.hacks",
            "contest.list",
            "contest.ratingChanges",
            "contest.standings",
            "contest.status",
            "problemset.problems",
            "problemset.recentStatus",
            "recentActions",
            "user.blogEntries",
            "user.friends",
            "user.info",
            "user.ratedList",
            "user.rating",
            "user.status",
        ],
    ) -> str:
        """
        Generate an authorised URL for a given API endpoint.

        Parameters
        ----------
        end_point_url : str
            The raw endpoint URL.
        method_name : Literal[...]
            The API method name.

        Returns
        -------
        str
            The authorised URL if authentication is enabled; otherwise, the original endpoint URL.
        """
        if self._auth_enabled:
            if self._time is None:
                self._time = int(time.time())
            random_six_digit: int = random.randint(111111, 999999)
            prefix: str = f"https://codeforces.com/api/{method_name}?"
            head: str = end_point_url.removeprefix(prefix)
            params: t.Dict[str, str] = {
                x.split("=")[0]: x.split("=")[1]
                for x in head.split("&")
                if x and "=" in x
            }
            sorted_params: "collections.OrderedDict[str, str]" = (
                collections.OrderedDict(sorted(params.items()))
            )
            encoded_params: str = urllib.parse.urlencode(sorted_params, safe=";")
            to_hash: str = (
                f"{random_six_digit}/{method_name}?apiKey={self._auth_key}&"
                f"{encoded_params}&time={self._time}#{self._secret}"
            )
            hashed_string: str = hashlib.sha512(to_hash.encode("utf8")).hexdigest()
            final_url: str = (
                f"https://codeforces.com/api/{method_name}?"
                f"{encoded_params}&apiKey={self._auth_key}&time={self._time}"
                f"&apiSig={random_six_digit}{hashed_string}"
            )
            return final_url
        return end_point_url

    def _generate_response(self, url: str) -> bytes:
        """
        Execute an HTTP GET request and return the response content.

        Parameters
        ----------
        url : str
            The URL to request.

        Returns
        -------
        bytes
            The raw response content.
        """
        with self._client as socket:
            response = socket.get(url=url)
            return response.content

    @staticmethod
    def _ensure_list(
        result: t.Optional[t.Union[t.List[t.Any], t.Any]],
    ) -> t.List[t.Any]:
        """
        Ensure that the API result is returned as a list.

        Parameters
        ----------
        result : t.Optional[t.Union[t.List[t.Any], t.Any]]
            The API result.

        Returns
        -------
        t.List[t.Any]
            The result as a list.
        """
        if result is None:
            return []
        if isinstance(result, list):
            return result
        return [result]

    def _execute_request(
        self,
        method_name: t.Literal[
            "blogEntry.comments",
            "blogEntry.view",
            "contest.hacks",
            "contest.list",
            "contest.ratingChanges",
            "contest.standings",
            "contest.status",
            "problemset.problems",
            "problemset.recentStatus",
            "recentActions",
            "user.blogEntries",
            "user.friends",
            "user.info",
            "user.ratedList",
            "user.rating",
            "user.status",
        ],
        endpoint_url: str,
        response_cls: t.Type,
    ) -> t.List[t.Any]:
        """
        Execute an API request synchronously and decode the response.

        Parameters
        ----------
        method_name : Literal[...]
            The API method name.
        endpoint_url : str
            The raw endpoint URL.
        response_cls : t.Type
            The class used to decode the JSON response.

        Returns
        -------
        t.List[t.Any]
            The decoded result wrapped as a list.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        final_url: str = self._generate_authorisation(
            method_name=method_name, end_point_url=endpoint_url
        )
        response_bytes: bytes = self._generate_response(url=final_url)
        base = msgspec.json.decode(response_bytes, strict=False, type=response_cls)
        if base.status != "FAILED":
            return self._ensure_list(base.result)
        else:
            raise Exception(base.comment)

    def get_user(
        self, handles: str, check_historic_handles: t.Optional[bool] = True
    ) -> t.List[codeforcespy.abc.objects.User]:
        """
        Retrieve user information for given handles.

        Parameters
        ----------
        handles : str
            Semicolon-separated list of user handles.
        check_historic_handles : t.Optional[bool], optional
            Whether to check historic handles (default is True).

        Returns
        -------
        t.List[pycodeforces.abc.objects.User]
            A list of user objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.user_info(
            handles=handles, check_historic_handles=check_historic_handles
        )
        result = self._execute_request(
            "user.info",
            endpoint_url,
            codeforcespy.abc.interactions.UserInteractionResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.User], result)

    def get_blog_entry_comments(
        self, blog_entry_id: int
    ) -> t.List[codeforcespy.abc.objects.Comment]:
        """
        Retrieve comments for a specific blog entry.

        Parameters
        ----------
        blog_entry_id : int
            The blog entry ID.

        Returns
        -------
        t.List[pycodeforces.abc.objects.Comment]
            A list of comment objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.blog_entry_comments(
            blog_entry_id=blog_entry_id
        )
        result = self._execute_request(
            "blogEntry.comments",
            endpoint_url,
            codeforcespy.abc.interactions.BlogEntryCommentResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.Comment], result)

    def get_blog_entry_view(
        self, blog_entry_id: int
    ) -> t.List[codeforcespy.abc.objects.BlogEntry]:
        """
        Retrieve a blog entry view.

        Parameters
        ----------
        blog_entry_id : int
            The blog entry ID.

        Returns
        -------
        t.List[pycodeforces.abc.objects.BlogEntry]
            A list of blog entry objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.blog_entry_view(
            blog_entry_id=blog_entry_id
        )
        result = self._execute_request(
            "blogEntry.view",
            endpoint_url,
            codeforcespy.abc.interactions.BlogEntryViewResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.BlogEntry], result)

    def get_contest_hacks(
        self, contest_id: int, as_manager: t.Optional[bool] = False
    ) -> t.List[codeforcespy.abc.objects.Hack]:
        """
        Retrieve contest hacks for a specific contest.

        Parameters
        ----------
        contest_id : int
            The contest ID.
        as_manager : t.Optional[bool], optional
            Whether to retrieve hacks as a contest manager (default is False).

        Returns
        -------
        t.List[pycodeforces.abc.objects.Hack]
            A list of hack objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.contest_hacks(
            contest_id=contest_id, as_manager=as_manager
        )
        result = self._execute_request(
            "contest.hacks",
            endpoint_url,
            codeforcespy.abc.interactions.ContestHacksResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.Hack], result)

    def get_contest_list(
        self, of_gym: t.Optional[bool] = False
    ) -> t.List[codeforcespy.abc.objects.Contest]:
        """
        Retrieve a list of contests.

        Parameters
        ----------
        of_gym : t.Optional[bool], optional
            Whether to include gym contests (default is False).

        Returns
        -------
        t.List[pycodeforces.abc.objects.Contest]
            A list of contest objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.contest_list(gym=of_gym)
        result = self._execute_request(
            "contest.list",
            endpoint_url,
            codeforcespy.abc.interactions.ContestListResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.Contest], result)

    def get_contest_rating_changes(
        self, contest_id: int
    ) -> t.List[codeforcespy.abc.objects.RatingChange]:
        """
        Retrieve rating changes for a specific contest.

        Parameters
        ----------
        contest_id : int
            The contest ID.

        Returns
        -------
        t.List[pycodeforces.abc.objects.RatingChange]
            A list of rating change objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.contest_rating_changes(
            contest_id=contest_id
        )
        result = self._execute_request(
            "contest.ratingChanges",
            endpoint_url,
            codeforcespy.abc.interactions.ContestRatingChangeResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.RatingChange], result)

    def get_contest_standings(
        self,
        contest_id: int,
        as_manager: t.Optional[bool] = False,
        from_index: int = 1,
        count: int = 5,
        show_unofficial: t.Optional[bool] = True,
    ) -> t.List[codeforcespy.abc.cobjects.Standings]:
        """
        Retrieve contest standings.

        Parameters
        ----------
        contest_id : int
            The contest ID.
        as_manager : t.Optional[bool], optional
            Whether to retrieve standings as a contest manager (default is False).
        from_index : int, optional
            The starting index for standings (default is 1).
        count : int, optional
            The number of standings rows to retrieve (default is 5).
        show_unofficial : t.Optional[bool], optional
            Whether to show unofficial standings (default is True).

        Returns
        -------
        t.List[pycodeforces.abc.cobjects.Standings]
            A list of standings objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.contest_standings(
            contest_id=contest_id,
            as_manager=as_manager,
            from_index=from_index,
            count=count,
            show_unofficial=show_unofficial,
        )
        result = self._execute_request(
            "contest.standings",
            endpoint_url,
            codeforcespy.abc.interactions.ContestStandingResponse,
        )
        return t.cast(t.List[codeforcespy.abc.cobjects.Standings], result)

    def get_contest_status(
        self,
        contest_id: int,
        as_manager: t.Optional[bool] = False,
        handle: t.Optional[str] = None,
        from_index: int = 1,
        count: int = 10,
    ) -> t.List[codeforcespy.abc.objects.Submission]:
        """
        Retrieve contest submissions.

        Parameters
        ----------
        contest_id : int
            The contest ID.
        as_manager : t.Optional[bool], optional
            Whether to retrieve status as a contest manager (default is False).
        handle : t.Optional[str], optional
            The user handle to filter submissions (default is None).
        from_index : int, optional
            The starting index for submissions (default is 1).
        count : int, optional
            The number of submissions to retrieve (default is 10).

        Returns
        -------
        t.List[pycodeforces.abc.objects.Submission]
            A list of submission objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.contest_status(
            contest_id=contest_id,
            as_manager=as_manager,
            handle=handle,
            from_index=from_index,
            count=count,
        )
        result = self._execute_request(
            "contest.status",
            endpoint_url,
            codeforcespy.abc.interactions.ContestStatusResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.Submission], result)

    def get_problemset_problems(
        self, tags: t.Optional[str] = None, problemset_name: t.Optional[str] = None
    ) -> t.List[codeforcespy.abc.cobjects.ProblemSetProblems]:
        """
        Retrieve problems from the problem set.

        Parameters
        ----------
        tags : t.Optional[str], optional
            Semicolon-separated list of tags (default is None).
        problemset_name : t.Optional[str], optional
            Custom problem set name (default is None).

        Returns
        -------
        t.List[pycodeforces.abc.cobjects.ProblemSetProblems]
            A list of problem set problems objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.problemset_problems(
            tags=tags, problemset_name=problemset_name
        )
        result = self._execute_request(
            "problemset.problems",
            endpoint_url,
            codeforcespy.abc.interactions.ProblemSetProblemsResponse,
        )
        return t.cast(t.List[codeforcespy.abc.cobjects.ProblemSetProblems], result)

    def get_problemset_recent_status(
        self, count: int, problemset_name: t.Optional[str] = None
    ) -> t.List[codeforcespy.abc.objects.Submission]:
        """
        Retrieve recent submissions for the problem set.

        Parameters
        ----------
        count : int
            The number of submissions to retrieve.
        problemset_name : t.Optional[str], optional
            Custom problem set name (default is None).

        Returns
        -------
        t.List[pycodeforces.abc.objects.Submission]
            A list of submission objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.problemset_recent_status(
            count=count, problemset_name=problemset_name
        )
        result = self._execute_request(
            "problemset.recentStatus",
            endpoint_url,
            codeforcespy.abc.interactions.ProblemSetRecentStatusResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.Submission], result)

    def get_recent_actions(
        self, max_count: int
    ) -> t.List[codeforcespy.abc.objects.RecentAction]:
        """
        Retrieve recent actions.

        Parameters
        ----------
        max_count : int
            The maximum number of recent actions to retrieve.

        Returns
        -------
        t.List[pycodeforces.abc.objects.RecentAction]
            A list of recent action objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.recent_actions(max_count=max_count)
        result = self._execute_request(
            "recentActions",
            endpoint_url,
            codeforcespy.abc.interactions.RecentActionsResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.RecentAction], result)

    def get_user_blog_entries(
        self, handle: str
    ) -> t.List[codeforcespy.abc.objects.BlogEntry]:
        """
        Retrieve blog entries for a specific user.

        Parameters
        ----------
        handle : str
            The Codeforces user handle.

        Returns
        -------
        t.List[pycodeforces.abc.objects.BlogEntry]
            A list of blog entry objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.user_blog_entries(handle=handle)
        result = self._execute_request(
            "user.blogEntries",
            endpoint_url,
            codeforcespy.abc.interactions.UserBlogEntryResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.BlogEntry], result)

    def get_user_friends(self, only_online: bool = True) -> t.List[str]:
        """
        Retrieve the friends list for the authenticated user.

        Parameters
        ----------
        only_online : bool, optional
            Whether to retrieve only online friends (default is True).

        Returns
        -------
        t.List[str]
            A list of friend handles.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.user_friends(only_online=only_online)
        result = self._execute_request(
            "user.friends",
            endpoint_url,
            codeforcespy.abc.interactions.UserFriendResponse,
        )
        return t.cast(t.List[str], result)

    def get_user_rated_list(
        self,
        active_only: t.Optional[bool] = True,
        include_retired: t.Optional[bool] = False,
        contest_id: t.Optional[int] = None,
    ) -> t.List[codeforcespy.abc.objects.User]:
        """
        Retrieve the rated list of users.

        Parameters
        ----------
        active_only : t.Optional[bool], optional
            Whether to include only active users (default is True).
        include_retired : t.Optional[bool], optional
            Whether to include retired users (default is False).
        contest_id : t.Optional[int], optional
            Contest ID to filter the rated list (default is None).

        Returns
        -------
        t.List[pycodeforces.abc.objects.User]
            A list of user objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.user_rated_list(
            active_only=active_only,
            include_retired=include_retired,
            contest_id=contest_id,
        )
        result = self._execute_request(
            "user.ratedList",
            endpoint_url,
            codeforcespy.abc.interactions.UserRatedListResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.User], result)

    def get_user_rating(
        self, handle: str
    ) -> t.List[codeforcespy.abc.objects.RatingChange]:
        """
        Retrieve the rating history for a specific user.

        Parameters
        ----------
        handle : str
            The Codeforces user handle.

        Returns
        -------
        t.List[pycodeforces.abc.objects.RatingChange]
            A list of rating change objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.user_rating(handle=handle)
        result = self._execute_request(
            "user.rating",
            endpoint_url,
            codeforcespy.abc.interactions.UserRatingResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.RatingChange], result)

    def get_user_status(
        self, handle: str, from_index: int = 1, count: int = 10
    ) -> t.List[codeforcespy.abc.objects.Submission]:
        """
        Retrieve submission status for a specific user.

        Parameters
        ----------
        handle : str
            The Codeforces user handle.
        from_index : int, optional
            The starting index for submissions (default is 1).
        count : int, optional
            The number of submissions to retrieve (default is 10).

        Returns
        -------
        t.List[pycodeforces.abc.objects.Submission]
            A list of submission objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.user_status(
            handle=handle, from_index=from_index, count=count
        )
        result = self._execute_request(
            "user.status",
            endpoint_url,
            codeforcespy.abc.interactions.UserStatusResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.Submission], result)

    def close(self) -> None:
        """
        Close the underlying synchronous HTTP client.
        """
        self._client.close()


class AsyncMethod:
    """
    Asynchronous Codeforces API client for executing requests with optional authentication.

    Parameters
    ----------
    enable_auth : t.Optional[bool], optional
        Flag indicating whether authentication is enabled (default is False).
    auth_key : t.Optional[str], optional
        API authentication key to be used when authentication is enabled.
    unix_time : t.Optional[int], optional
        Unix timestamp to be used for request signing; if not provided, the current time is used.
    secret : t.Optional[str], optional
        API secret for signing requests when authentication is enabled.

    Attributes
    ----------
    _url_generator : pycodeforces.abc.endpoints.CodeForcesAPI
        Instance for generating API endpoint URLs.
    _client : pycodeforces.clients.AsyncClient
        Asynchronous HTTP client for making API requests.
    _auth_key : t.Optional[str]
        Authentication key for API requests.
    _secret : t.Optional[str]
        Secret key for request signing.
    _time : t.Optional[int]
        Unix timestamp used for request signing.
    _auth_enabled : bool
        Indicates if authentication is enabled.
    """

    def __init__(
        self,
        enable_auth: t.Optional[bool] = False,
        auth_key: t.Optional[str] = None,
        unix_time: t.Optional[int] = None,
        secret: t.Optional[str] = None,
    ) -> None:
        """
        Initialize the asynchronous client.

        Parameters
        ----------
        enable_auth : t.Optional[bool], optional
            Whether to enable authentication (default is False).
        auth_key : t.Optional[str], optional
            API authentication key (default is None).
        unix_time : t.Optional[int], optional
            Unix timestamp for signing requests (default is None).
        secret : t.Optional[str], optional
            API secret for signing requests (default is None).
        """
        self._url_generator: codeforcespy.abc.endpoints.CodeForcesAPI = (
            codeforcespy.abc.endpoints.CodeForcesAPI()
        )
        self._client: codeforcespy.clients.AsyncClient = (
            codeforcespy.clients.AsyncClient()
        )
        self._auth_key: t.Optional[str] = auth_key
        self._secret: t.Optional[str] = secret
        self._time: t.Optional[int] = unix_time
        self._auth_enabled: bool = bool(enable_auth)

    def _generate_authorisation(
        self,
        end_point_url: str,
        method_name: t.Literal[
            "blogEntry.comments",
            "blogEntry.view",
            "contest.hacks",
            "contest.list",
            "contest.ratingChanges",
            "contest.standings",
            "contest.status",
            "problemset.problems",
            "problemset.recentStatus",
            "recentActions",
            "user.blogEntries",
            "user.friends",
            "user.info",
            "user.ratedList",
            "user.rating",
            "user.status",
        ],
    ) -> str:
        """
        Generate an authorised URL for a given API endpoint.

        Parameters
        ----------
        end_point_url : str
            The raw endpoint URL.
        method_name : Literal[...]
            The API method name.

        Returns
        -------
        str
            The authorised URL if authentication is enabled; otherwise, the original endpoint URL.
        """
        if self._auth_enabled:
            if self._time is None:
                self._time = int(time.time())
            random_six_digit: int = random.randint(111111, 999999)
            prefix: str = f"https://codeforces.com/api/{method_name}?"
            head: str = end_point_url.removeprefix(prefix)
            params: t.Dict[str, str] = {
                x.split("=")[0]: x.split("=")[1]
                for x in head.split("&")
                if x and "=" in x
            }
            sorted_params: "collections.OrderedDict[str, str]" = (
                collections.OrderedDict(sorted(params.items()))
            )
            encoded_params: str = urllib.parse.urlencode(sorted_params, safe=";")
            to_hash: str = (
                f"{random_six_digit}/{method_name}?apiKey={self._auth_key}&"
                f"{encoded_params}&time={self._time}#{self._secret}"
            )
            hashed_string: str = hashlib.sha512(to_hash.encode("utf8")).hexdigest()
            final_url: str = (
                f"https://codeforces.com/api/{method_name}?"
                f"{encoded_params}&apiKey={self._auth_key}&time={self._time}"
                f"&apiSig={random_six_digit}{hashed_string}"
            )
            return final_url
        return end_point_url

    async def _generate_response(self, url: str) -> bytes:
        """
        Execute an asynchronous HTTP GET request and return the response content.

        Parameters
        ----------
        url : str
            The URL to request.

        Returns
        -------
        bytes
            The raw response content.
        """
        async with self._client as socket:
            response = await socket.get(url=url)
            return response.read()

    @staticmethod
    def _ensure_list(
        result: t.Optional[t.Union[t.List[t.Any], t.Any]],
    ) -> t.List[t.Any]:
        """
        Ensure that the API result is returned as a list.

        Parameters
        ----------
        result : t.Optional[t.Union[t.List[t.Any], t.Any]]
            The API result.

        Returns
        -------
        t.List[t.Any]
            The result as a list.
        """
        if result is None:
            return []
        if isinstance(result, list):
            return result
        return [result]

    async def _execute_request(
        self,
        method_name: t.Literal[
            "blogEntry.comments",
            "blogEntry.view",
            "contest.hacks",
            "contest.list",
            "contest.ratingChanges",
            "contest.standings",
            "contest.status",
            "problemset.problems",
            "problemset.recentStatus",
            "recentActions",
            "user.blogEntries",
            "user.friends",
            "user.info",
            "user.ratedList",
            "user.rating",
            "user.status",
        ],
        endpoint_url: str,
        response_cls: t.Type,
    ) -> t.List[t.Any]:
        """
        Execute an asynchronous API request and decode the response.

        Parameters
        ----------
        method_name : Literal[...]
            The API method name.
        endpoint_url : str
            The raw endpoint URL.
        response_cls : t.Type
            The class used to decode the JSON response.

        Returns
        -------
        t.List[t.Any]
            The decoded result wrapped as a list.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        final_url: str = self._generate_authorisation(
            method_name=method_name, end_point_url=endpoint_url
        )
        response_bytes: bytes = await self._generate_response(url=final_url)
        base = msgspec.json.decode(response_bytes, strict=False, type=response_cls)
        if base.status != "FAILED":
            return self._ensure_list(base.result)
        else:
            raise Exception(base.comment)

    async def get_user(
        self, handles: str, check_historic_handles: t.Optional[bool] = True
    ) -> t.List[codeforcespy.abc.objects.User]:
        """
        Asynchronously retrieve user information for given handles.

        Parameters
        ----------
        handles : str
            Semicolon-separated list of user handles.
        check_historic_handles : t.Optional[bool], optional
            Whether to check historic handles (default is True).

        Returns
        -------
        t.List[pycodeforces.abc.objects.User]
            A list of user objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.user_info(
            handles=handles, check_historic_handles=check_historic_handles
        )
        result = await self._execute_request(
            "user.info",
            endpoint_url,
            codeforcespy.abc.interactions.UserInteractionResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.User], result)

    async def get_blog_entry_comments(
        self, blog_entry_id: int
    ) -> t.List[codeforcespy.abc.objects.Comment]:
        """
        Asynchronously retrieve comments for a specific blog entry.

        Parameters
        ----------
        blog_entry_id : int
            The blog entry ID.

        Returns
        -------
        t.List[pycodeforces.abc.objects.Comment]
            A list of comment objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.blog_entry_comments(
            blog_entry_id=blog_entry_id
        )
        result = await self._execute_request(
            "blogEntry.comments",
            endpoint_url,
            codeforcespy.abc.interactions.BlogEntryCommentResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.Comment], result)

    async def get_blog_entry_view(
        self, blog_entry_id: int
    ) -> t.List[codeforcespy.abc.objects.BlogEntry]:
        """
        Asynchronously retrieve a blog entry view.

        Parameters
        ----------
        blog_entry_id : int
            The blog entry ID.

        Returns
        -------
        t.List[pycodeforces.abc.objects.BlogEntry]
            A list of blog entry objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.blog_entry_view(
            blog_entry_id=blog_entry_id
        )
        result = await self._execute_request(
            "blogEntry.view",
            endpoint_url,
            codeforcespy.abc.interactions.BlogEntryViewResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.BlogEntry], result)

    async def get_contest_hacks(
        self, contest_id: int, as_manager: t.Optional[bool] = False
    ) -> t.List[codeforcespy.abc.objects.Hack]:
        """
        Asynchronously retrieve contest hacks for a specific contest.

        Parameters
        ----------
        contest_id : int
            The contest ID.
        as_manager : t.Optional[bool], optional
            Whether to retrieve hacks as a contest manager (default is False).

        Returns
        -------
        t.List[pycodeforces.abc.objects.Hack]
            A list of hack objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.contest_hacks(
            contest_id=contest_id, as_manager=as_manager
        )
        result = await self._execute_request(
            "contest.hacks",
            endpoint_url,
            codeforcespy.abc.interactions.ContestHacksResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.Hack], result)

    async def get_contest_list(
        self, of_gym: t.Optional[bool] = False
    ) -> t.List[codeforcespy.abc.objects.Contest]:
        """
        Asynchronously retrieve a list of contests.

        Parameters
        ----------
        of_gym : t.Optional[bool], optional
            Whether to include gym contests (default is False).

        Returns
        -------
        t.List[pycodeforces.abc.objects.Contest]
            A list of contest objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.contest_list(gym=of_gym)
        result = await self._execute_request(
            "contest.list",
            endpoint_url,
            codeforcespy.abc.interactions.ContestListResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.Contest], result)

    async def get_contest_rating_changes(
        self, contest_id: int
    ) -> t.List[codeforcespy.abc.objects.RatingChange]:
        """
        Asynchronously retrieve rating changes for a specific contest.

        Parameters
        ----------
        contest_id : int
            The contest ID.

        Returns
        -------
        t.List[pycodeforces.abc.objects.RatingChange]
            A list of rating change objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.contest_rating_changes(
            contest_id=contest_id
        )
        result = await self._execute_request(
            "contest.ratingChanges",
            endpoint_url,
            codeforcespy.abc.interactions.ContestRatingChangeResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.RatingChange], result)

    async def get_contest_standings(
        self,
        contest_id: int,
        as_manager: t.Optional[bool] = False,
        from_index: int = 1,
        count: int = 5,
        show_unofficial: t.Optional[bool] = True,
    ) -> t.List[codeforcespy.abc.cobjects.Standings]:
        """
        Asynchronously retrieve contest standings.

        Parameters
        ----------
        contest_id : int
            The contest ID.
        as_manager : t.Optional[bool], optional
            Whether to retrieve standings as a contest manager (default is False).
        from_index : int, optional
            The starting index for standings (default is 1).
        count : int, optional
            The number of standings rows to retrieve (default is 5).
        show_unofficial : t.Optional[bool], optional
            Whether to show unofficial standings (default is True).

        Returns
        -------
        t.List[pycodeforces.abc.cobjects.Standings]
            A list of standings objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.contest_standings(
            contest_id=contest_id,
            as_manager=as_manager,
            from_index=from_index,
            count=count,
            show_unofficial=show_unofficial,
        )
        result = await self._execute_request(
            "contest.standings",
            endpoint_url,
            codeforcespy.abc.interactions.ContestStandingResponse,
        )
        return t.cast(t.List[codeforcespy.abc.cobjects.Standings], result)

    async def get_contest_status(
        self,
        contest_id: int,
        as_manager: t.Optional[bool] = False,
        handle: t.Optional[str] = None,
        from_index: int = 1,
        count: int = 10,
    ) -> t.List[codeforcespy.abc.objects.Submission]:
        """
        Asynchronously retrieve contest submission status.

        Parameters
        ----------
        contest_id : int
            The contest ID.
        as_manager : t.Optional[bool], optional
            Whether to retrieve status as a contest manager (default is False).
        handle : t.Optional[str], optional
            The user handle to filter submissions (default is None).
        from_index : int, optional
            The starting index for submissions (default is 1).
        count : int, optional
            The number of submissions to retrieve (default is 10).

        Returns
        -------
        t.List[pycodeforces.abc.objects.Submission]
            A list of submission objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.contest_status(
            contest_id=contest_id,
            as_manager=as_manager,
            handle=handle,
            from_index=from_index,
            count=count,
        )
        result = await self._execute_request(
            "contest.status",
            endpoint_url,
            codeforcespy.abc.interactions.ContestStatusResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.Submission], result)

    async def get_problemset_problems(
        self, tags: t.Optional[str] = None, problemset_name: t.Optional[str] = None
    ) -> t.List[codeforcespy.abc.cobjects.ProblemSetProblems]:
        """
        Asynchronously retrieve problems from the problem set.

        Parameters
        ----------
        tags : t.Optional[str], optional
            Semicolon-separated list of tags (default is None).
        problemset_name : t.Optional[str], optional
            Custom problem set name (default is None).

        Returns
        -------
        t.List[pycodeforces.abc.cobjects.ProblemSetProblems]
            A list of problem set problems objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.problemset_problems(
            tags=tags, problemset_name=problemset_name
        )
        result = await self._execute_request(
            "problemset.problems",
            endpoint_url,
            codeforcespy.abc.interactions.ProblemSetProblemsResponse,
        )
        return t.cast(t.List[codeforcespy.abc.cobjects.ProblemSetProblems], result)

    async def get_problemset_recent_status(
        self, count: int, problemset_name: t.Optional[str] = None
    ) -> t.List[codeforcespy.abc.objects.Submission]:
        """
        Asynchronously retrieve recent submissions for the problem set.

        Parameters
        ----------
        count : int
            The number of submissions to retrieve.
        problemset_name : t.Optional[str], optional
            Custom problem set name (default is None).

        Returns
        -------
        t.List[pycodeforces.abc.objects.Submission]
            A list of submission objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.problemset_recent_status(
            count=count, problemset_name=problemset_name
        )
        result = await self._execute_request(
            "problemset.recentStatus",
            endpoint_url,
            codeforcespy.abc.interactions.ProblemSetRecentStatusResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.Submission], result)

    async def get_recent_actions(
        self, max_count: int
    ) -> t.List[codeforcespy.abc.objects.RecentAction]:
        """
        Asynchronously retrieve recent actions.

        Parameters
        ----------
        max_count : int
            The maximum number of recent actions to retrieve.

        Returns
        -------
        t.List[pycodeforces.abc.objects.RecentAction]
            A list of recent action objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.recent_actions(max_count=max_count)
        result = await self._execute_request(
            "recentActions",
            endpoint_url,
            codeforcespy.abc.interactions.RecentActionsResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.RecentAction], result)

    async def get_user_blog_entries(
        self, handle: str
    ) -> t.List[codeforcespy.abc.objects.BlogEntry]:
        """
        Asynchronously retrieve blog entries for a specific user.

        Parameters
        ----------
        handle : str
            The Codeforces user handle.

        Returns
        -------
        t.List[pycodeforces.abc.objects.BlogEntry]
            A list of blog entry objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.user_blog_entries(handle=handle)
        result = await self._execute_request(
            "user.blogEntries",
            endpoint_url,
            codeforcespy.abc.interactions.UserBlogEntryResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.BlogEntry], result)

    async def get_user_friends(self, only_online: bool = True) -> t.List[str]:
        """
        Asynchronously retrieve the friends list for the authenticated user.

        Parameters
        ----------
        only_online : bool, optional
            Whether to retrieve only online friends (default is True).

        Returns
        -------
        t.List[str]
            A list of friend handles.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.user_friends(only_online=only_online)
        result = await self._execute_request(
            "user.friends",
            endpoint_url,
            codeforcespy.abc.interactions.UserFriendResponse,
        )
        return t.cast(t.List[str], result)

    async def get_user_rated_list(
        self,
        active_only: t.Optional[bool] = True,
        include_retired: t.Optional[bool] = False,
        contest_id: t.Optional[int] = None,
    ) -> t.List[codeforcespy.abc.objects.User]:
        """
        Asynchronously retrieve the rated list of users.

        Parameters
        ----------
        active_only : t.Optional[bool], optional
            Whether to include only active users (default is True).
        include_retired : t.Optional[bool], optional
            Whether to include retired users (default is False).
        contest_id : t.Optional[int], optional
            Contest ID to filter the rated list (default is None).

        Returns
        -------
        t.List[pycodeforces.abc.objects.User]
            A list of user objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.user_rated_list(
            active_only=active_only,
            include_retired=include_retired,
            contest_id=contest_id,
        )
        result = await self._execute_request(
            "user.ratedList",
            endpoint_url,
            codeforcespy.abc.interactions.UserRatedListResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.User], result)

    async def get_user_rating(
        self, handle: str
    ) -> t.List[codeforcespy.abc.objects.RatingChange]:
        """
        Asynchronously retrieve the rating history for a specific user.

        Parameters
        ----------
        handle : str
            The Codeforces user handle.

        Returns
        -------
        t.List[pycodeforces.abc.objects.RatingChange]
            A list of rating change objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.user_rating(handle=handle)
        result = await self._execute_request(
            "user.rating",
            endpoint_url,
            codeforcespy.abc.interactions.UserRatingResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.RatingChange], result)

    async def get_user_status(
        self, handle: str, from_index: int = 1, count: int = 10
    ) -> t.List[codeforcespy.abc.objects.Submission]:
        """
        Asynchronously retrieve submission status for a specific user.

        Parameters
        ----------
        handle : str
            The Codeforces user handle.
        from_index : int, optional
            The starting index for submissions (default is 1).
        count : int, optional
            The number of submissions to retrieve (default is 10).

        Returns
        -------
        t.List[pycodeforces.abc.objects.Submission]
            A list of submission objects.

        Raises
        ------
        Exception
            If the API response indicates a failure.
        """
        endpoint_url: str = self._url_generator.user_status(
            handle=handle, from_index=from_index, count=count
        )
        result = await self._execute_request(
            "user.status",
            endpoint_url,
            codeforcespy.abc.interactions.UserStatusResponse,
        )
        return t.cast(t.List[codeforcespy.abc.objects.Submission], result)

    async def close(self) -> None:
        """
        Asynchronously close the underlying HTTP client.
        """
        await self._client.aclose()
