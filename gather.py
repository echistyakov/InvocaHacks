import datetime
import dateutil.relativedelta
import praw
import sys
'''
CL args:
[id of reddit post from URL] [outfile]

Format of printed comments:
[hours after post] [minutes after post] [post body]
'''

def comment_valid(comment):
	if comment.find("http") == -1 and len(comment) > 1:
		return True
	else:
		return False

data_f = open(sys.argv[2], 'w')

client = praw.Reddit(user_agent="some Agent")
submission = client.get_submission(submission_id = sys.argv[1])

post_created_time = datetime.datetime.fromtimestamp( submission.created_utc )
all_comments = praw.helpers.flatten_tree(submission.comments)

for c in all_comments:
	if isinstance(c, praw.objects.Comment):
		comment_time = datetime.datetime.fromtimestamp( c.created_utc )
		r_time = dateutil.relativedelta.relativedelta(comment_time, post_created_time)

		if comment_valid(c.body):
			c_body = c.body.replace('\n', ' ')
			c_body.encode('ascii', 'ignore')

			line = str(r_time.hours) + " " + str(r_time.minutes) + " " + c_body.encode("ascii", "ignore") + "\n"
			data_f.write(line)

data_f.close()
