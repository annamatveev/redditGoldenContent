from Config.IndicativeWordsDictionary import IndicativeWordsDictionary
from Config.QualityThersholds import QualityThresholds
from Decorators.UsersDecorator import UsersDecorator
from Models.RuleMatch import RuleMatch
from Models.Activity import Activity
from Models.Lead import Lead


class AskingForHelpTitlePostRule:
    description = "Posted a post with indicative words in title"

    @staticmethod
    def execute_rule(reddit_post):
        title = reddit_post.title.lower()

        flair = ''
        if reddit_post.link_flair_text is not None:
            flair = reddit_post.link_flair_text.lower()

        guide_words_found = [word for word in IndicativeWordsDictionary.GUIDE_CONTENT
                             if (word in title or word in flair)]
        asking_help_words_found = [word for word in IndicativeWordsDictionary.ASKING_FOR_HELP
                                   if (word in title or word in flair)]

        if len(guide_words_found) > 0 and len(asking_help_words_found) > 0:
            match = RuleMatch(AskingForHelpTitlePostRule.description + ': ' + ', '.join(guide_words_found),
                              QualityThresholds.content_quality_score(reddit_post.selftext, reddit_post.ups))
            golden_post = Activity(reddit_post.id,
                                   reddit_post.selftext,
                                   reddit_post.title,
                                   reddit_post.ups,
                                   reddit_post.shortlink,
                                   reddit_post.author.name,
                                   reddit_post.created,
                                   match,
                                   reddit_post)

            user = UsersDecorator.amend_user_details(reddit_post.author)
            lead = Lead(golden_post, user)
            return lead
