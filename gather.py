import datetime
import dateutil.relativedelta
import praw
import requests
import sys
'''
Usage:
./gather.py [id of reddit post from URL] [outfile]

Format of printed comments:
[minutes after post] [post body]
'''


def is_comment_valid(comment):
    if comment.find("http") == -1 and len(comment) > 1 and comment.find("[deleted]") == -1 and comment.find("[removed]") == -1:
        return True
    else:
        return False


def analyse_text(text):
    req = requests.post(url='http://text-processing.com/api/sentiment/',
                        data={'text': text})

    # Convert decision to 1/0/-1 scale
    if req.json()['label'] == 'pos':
        decision = 1
    elif req.json()['label'] == 'neg':
        decision = -1
    elif req.json()['label'] == 'neutral':
        decision = 0

    # Get a tuple of probabilities
    pos_prob = req.json()['probability']['pos']
    neg_prob = req.json()['probability']['neg']
    neu_prob = req.json()['probability']['neutral']

    probs = (pos_prob, neu_prob, neg_prob)

    return (decision, probs)


def run_script():
    file_name = str(sys.argv[2])
    submission_id = str(sys.argv[1])

    out_file = open(sys.argv[2], 'w')

    client = praw.Reddit(user_agent="some Agent")
    submission = client.get_submission(submission_id=submission_id)
    submission.replace_more_comments(limit=None, threshold=0)

    post_created_time = datetime.datetime.fromtimestamp(submission.created_utc)
    all_comments = praw.helpers.flatten_tree(submission.comments)
    print "Total Comments: ", len(all_comments)

    for c in all_comments:
        if isinstance(c, praw.objects.Comment):
            comment_time = datetime.datetime.fromtimestamp(c.created_utc)
            r_time = dateutil.relativedelta.relativedelta(comment_time, post_created_time)

            if is_comment_valid(c.body):
                c_body = c.body.replace('\n', ' ')
                hours_and_minutes = str(r_time.hours * 60 + r_time.minutes)
                analysis = analyse_text(c_body)

                line = "{} {} {} {} {}\n".format(str(hours_and_minutes),
                                                 str(analysis[0]),
                                                 str(analysis[1][0]),
                                                 str(analysis[1][1]),
                                                 str(analysis[1][2]))
                out_file.write(line)

    out_file.close()


if __name__ == '__main__':
    run_script()
