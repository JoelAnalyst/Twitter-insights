import pandas as pd
import string
import operator
def load_tweets(tweet_file):

    """ Load and process a Twitter analytics data file """

    # Read tweet data (obtained from Twitter Analytics)
    tweet_df = pd.read_csv("tweet_file.csv")

    # Drop irrelevant columns
    tweet_df = tweet_df.drop(tweet_df.columns[[13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39]], axis=1)

    return tweet_df
tweet_df = load_tweets('tweets.csv')
tweet_df.head()
# Total tweets
print 'Total tweets this period:', len(tweet_df.index), '\n'

# Retweets
tweet_df = tweet_df.sort_values(by='Retweets', ascending=False)
tweet_df = tweet_df.reset_index(drop=True)
print 'Mean retweets:', round(tweet_df['Retweets'].mean(),2), '\n'
print 'Top 5 RTed tweets:'
print '------------------'
for i in range(5):
    print tweet_df['Texte du Tweet'].ix[i], '-', tweet_df['Retweets'].ix[i]
print '\n'
    
# Likes
tweet_df = tweet_df.sort_values(by="J'aime", ascending=False)
tweet_df = tweet_df.reset_index(drop=True)
print 'Mean likes:', round(tweet_df["J'aime"].mean(),2), '\n'
print 'Top 5 liked tweets:'
print '-------------------'
for i in range(5):
    print tweet_df['Texte du Tweet'].ix[i], '-', tweet_df["J'aime"].ix[i]
print '\n'

# Impressions
tweet_df = tweet_df.sort_values(by='impressions', ascending=False)
tweet_df = tweet_df.reset_index(drop=True)
print 'Mean impressions:', round(tweet_df['impressions'].mean(),2), '\n'
print 'Top 5 tweets with most impressions:'
print '-----------------------------------'
for i in range(5):
    print tweet_df['Texte du Tweet'].ix[i], '-', tweet_df['impressions'].ix[i]

# Hashtags & mentions
tag_dict = {}
mention_dict = {}

for i in tweet_df.index:
    tweet_text = tweet_df.ix[i]['Texte du Tweet']
    tweet = tweet_text.lower()
    tweet_tokenized = tweet.split()

    for word in tweet_tokenized:
        # Hashtags - tokenize and build dict of tag counts
        if (word[0:1] == '#' and len(word) > 1):
            key = word.translate(string.maketrans("",""), string.punctuation)
            if key in tag_dict:
                tag_dict[key] += 1
            else:
                tag_dict[key] = 1

        # Mentions - tokenize and build dict of mention counts
        if (word[0:1] == '@' and len(word) > 1):
            key = word.translate(string.maketrans("",""), string.punctuation)
            if key in mention_dict:
                mention_dict[key] += 1
            else:
                mention_dict[key] = 1

# The 10 most popular tags and counts
top_tags = dict(sorted(tag_dict.iteritems(), key=operator.itemgetter(1), reverse=True)[:10])
top_tags_sorted = sorted(top_tags.items(), key=lambda x: x[1])[::-1]
print 'Top 10 hashtags:'
print '----------------'
for tag in top_tags_sorted:
    print tag[0], '-', str(tag[1])
    
# The 10 most popular mentions and counts
top_mentions = dict(sorted(mention_dict.iteritems(), key=operator.itemgetter(1), reverse=True)[:10])
top_mentions_sorted = sorted(top_mentions.items(), key=lambda x: x[1])[::-1]
print '\nTop 10 mentions:'
print '----------------'
for mention in top_mentions_sorted:
    print mention[0], '-', str(mention[1])

# Time-series impressions (DOW, HOD, etc) (0 = Sunday... 6 = Saturday)
gmt_offset = -4

# Create proper datetime column, apply local GMT offset
tweet_df['ts'] = pd.to_datetime(tweet_df['heure'])
tweet_df['ts'] = tweet_df.ts + pd.to_timedelta(gmt_offset, unit='h')

# Add hour of day and day of week columns
tweet_df['hod'] = [t.hour for t in tweet_df.ts]
tweet_df['dow'] = [t.dayofweek for t in tweet_df.ts]

hod_dict = {}
hod_count = {}
dow_dict = {}
dow_count = {}
weekday_dict = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}

# Process tweets, collect stats
for i in tweet_df.index:
    hod = tweet_df.ix[i]['hod']
    dow = tweet_df.ix[i]['dow']
    imp = tweet_df.ix[i]['impressions']

    if hod in hod_dict:
        hod_dict[hod] += int(imp)
        hod_count[hod] += 1
    else:
        hod_dict[hod] = int(imp)
        hod_count[hod] = 1

    if dow in dow_dict:
        dow_dict[dow] += int(imp)
        dow_count[dow] += 1
    else:
        dow_dict[dow] = int(imp)
        dow_count[dow] = 1

print 'Average impressions per tweet by hour tweeted:'
print '----------------------------------------------'
for hod in hod_dict:
    print hod, '-', hod+1, ':', hod_dict[hod]/hod_count[hod], '=>', hod_count[hod], 'tweets'

print '\nAverage impressions per tweet by day of week tweeted:'
print '-----------------------------------------------------'
for dow in dow_dict:
    print weekday_dict[dow], ':', dow_dict[dow]/dow_count[dow], '=>', dow_count[dow], ' tweets'
