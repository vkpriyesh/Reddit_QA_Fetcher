import praw
from typing import List, Dict
import config

# Initialize Reddit API client
reddit = praw.Reddit(
    client_id=config.REDDIT_CLIENT_ID,
    client_secret=config.REDDIT_CLIENT_SECRET,
    user_agent=config.REDDIT_USER_AGENT
)

def get_ama_responses(reddit_thread_url: str, user_ids: List[str]) -> List[Dict[str, str]]:
    """
    Fetches questions and answers from a Reddit AMA thread.
    
    Parameters:
    - reddit_thread_url: URL of the Reddit thread (AMA).
    - user_ids: List of Reddit user IDs responsible for the AMA.
    
    Returns:
    - A list of dictionaries with "Question" and "Answer" keys.
    """
    # Extract thread ID from URL and fetch the submission
    thread_id = reddit_thread_url.split('/comments/')[1].split('/')[0]
    submission = reddit.submission(id=thread_id)
    submission.comments.replace_more(limit=None)  # Fetch all comments
    
    qna_pairs = []

    # Iterate over all comments
    for comment in submission.comments.list():
        # Check if comment author is in the given user_ids
        if comment.author and comment.author.name in user_ids:
            # Retrieve the parent (question)
            parent_comment = comment.parent()
            if parent_comment != submission:  # Exclude the post itself
                qna_pairs.append({
                    "Question": parent_comment.body,
                    "Answer": comment.body
                })

    return qna_pairs

# Example usage:
reddit_thread_url = "https://www.reddit.com/r/ChatGPT/comments/1ggixzy/ama_with_openais_sam_altman_kevin_weil_srinivas/"
user_ids = ["samaltman"]
qna_pairs = get_ama_responses(reddit_thread_url, user_ids)

for pair in qna_pairs:
    print(f"Question: {pair['Question']}\nAnswer: {pair['Answer']}\n")
