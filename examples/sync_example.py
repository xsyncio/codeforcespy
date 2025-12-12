"""
Synchronous Client Example.

This example demonstrates how to use the synchronous Codeforces API client
for simple scripts and CLI tools.
"""

import codeforcespy.errors
import codeforcespy.processors


def main() -> None:
    """Demonstrate synchronous API usage."""
    # Initialize the synchronous client
    client = codeforcespy.processors.SyncMethod()

    try:
        # Fetch user information
        users = client.get_user(handles="tourist")
        for user in users:
            print(f"Handle: {user.handle}")
            print(f"Rating: {user.rating}")
            print(f"Rank: {user.rank}")
            print(f"Max Rating: {user.maxRating}")
            print()

        # Get user rating history
        rating_history = client.get_user_rating(handle="tourist")
        print(f"Total contests: {len(rating_history)}")
        if rating_history:
            latest = rating_history[-1]
            print(f"Latest contest: {latest.contestName}")
            print(f"Rating change: {latest.oldRating} -> {latest.newRating}")
            print()

        # Get recent submissions
        submissions = client.get_user_status(handle="tourist", count=5)
        print("Recent submissions:")
        for sub in submissions:
            problem_name = sub.problem.name if sub.problem else "Unknown"
            print(f"  - {problem_name}: {sub.verdict}")
        print()

        # List upcoming/recent contests
        contests = client.get_contest_list(of_gym=False)
        upcoming = [c for c in contests if c.phase == "BEFORE"][:3]
        print(f"Upcoming contests ({len(upcoming)}):")
        for contest in upcoming:
            print(f"  - {contest.name}")

    except codeforcespy.errors.APIError as e:
        print(f"API Error: {e.message}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
