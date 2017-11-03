import copy
from HighlyRatedCommentRule import HighlyRatedCommentRule
from LongCommentRule import LongCommentRule
from AskingForHelpTitlePostRule import AskingForHelpTitlePostRule
from CommentToIndicativeWordsInTitleRule import CommentToIndicativeWordsInTitleRule
from SpamContentInCommentRule import SpanContentInCommentRule

class CommentFilter:
    def __init__(self, subreddit):
        self.comments = subreddit.comments(limit=10)
        self.subreddit = subreddit;
        self.golden_comments = []

    def filter_golden_comments(self):
        self.filter_comments_to_indicative_words_post()

    def filter_long_comments(self):
        for reddit_comment in copy.copy(self.comments):
            golden_comment = LongCommentRule.execute_rule(reddit_comment)
            if golden_comment is not None:
                self.golden_comments.append(golden_comment)

    def filter_high_rated_comments(self):
        for reddit_comment in copy.copy(self.comments):
            golden_comment = HighlyRatedCommentRule.execute_rule(reddit_comment)
            if golden_comment is not None:
                self.golden_comments.append(golden_comment)

    def filter_comments_to_indicative_words_post(self):
        for reddit_post in copy.copy(self.subreddit.new(limit=500)):
            golden_post_with_indicative_words = AskingForHelpTitlePostRule.execute_rule(reddit_post)
            if golden_post_with_indicative_words is not None:
                for reddit_comment in golden_post_with_indicative_words.reddit_content.comments:
                    golden_comment = CommentToIndicativeWordsInTitleRule.execute_rule(reddit_comment)
                    if golden_comment is not None:
                        self.golden_comments.append(golden_comment)

    def remove_spam_messages(self):
        for comment in copy.copy(self.comments):
            comment = SpanContentInCommentRule.execute_rule(comment)
            if comment is not None:  # Tagged as spam
                self.comments.remove(comment)

    def print_golden_comments(self):
        for comment in self.golden_comments:
            print("http://reddit.com/" + comment.comment_link + " " + str(comment.votes))
