"""
Asynchronous Client Example.

This example demonstrates how to use the asynchronous Codeforces API client
for high-concurrency applications and async frameworks.
"""

import asyncio

import codeforcespy.errors
import codeforcespy.processors


async def fetch_user_info(client: codeforcespy.processors.AsyncMethod) -> None:
    """Fetch and display user information."""
    users = await client.get_user(handles="tourist;Petr;jiangly")
    print("Top Competitive Programmers:")
    print("-" * 40)
    for user in users:
        print(f"  {user.handle}: {user.rating} ({user.rank})")
    print()


async def fetch_contest_standings(
    client: codeforcespy.processors.AsyncMethod,
    contest_id: int,
) -> None:
    """Fetch and display contest standings."""
    standings = await client.get_contest_standings(
        contest_id=contest_id,
        from_index=1,
        count=5,
        show_unofficial=False,
    )
    if standings:
        standing = standings[0]
        if standing.contest:
            contest = (
                standing.contest[0]
                if isinstance(standing.contest, list)
                else standing.contest
            )
            print(f"Contest: {contest.name}")
            print("-" * 40)

        if standing.rows:
            rows = (
                standing.rows
                if isinstance(standing.rows, list)
                else [standing.rows]
            )
            for row in rows:
                if row.party and row.party.members:
                    handle = row.party.members[0].handle
                    print(f"  Rank {row.rank}: {handle} ({row.points} pts)")
    print()


async def fetch_problems_by_tag(
    client: codeforcespy.processors.AsyncMethod,
    tag: str,
) -> None:
    """Fetch problems filtered by tag."""
    result = await client.get_problemset_problems(tags=tag)
    if result:
        problems_data = result[0]
        problems = problems_data.problems
        if problems:
            problem_list = problems if isinstance(problems, list) else [problems]
            print(f"Problems with tag '{tag}' (first 5):")
            print("-" * 40)
            for problem in problem_list[:5]:
                rating = problem.rating if problem.rating else "unrated"
                print(f"  {problem.contestId}{problem.index}: {problem.name} [{rating}]")
    print()


async def main() -> None:
    """Run all async examples concurrently."""
    client = codeforcespy.processors.AsyncMethod()

    try:
        # Run multiple requests concurrently for better performance
        _ = await asyncio.gather(
            fetch_user_info(client),
            fetch_contest_standings(client, contest_id=1992),
            fetch_problems_by_tag(client, tag="dp"),
        )

    except codeforcespy.errors.APIError as e:
        print(f"API Error: {e.message}")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
