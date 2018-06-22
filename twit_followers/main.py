import os
import tweepy
import config
import sys
from collections import defaultdict

auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
auth.set_access_token(config.access_token, config.access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

following = []
friend_dict = dict()


def test_methods(user_handle, num_rec):
	mutual_dict = defaultdict(int)

	friends_array = []

	# checking for proper arguments
	if len(sys.argv) != 3:
		print("you're missing one or two parameters! this script takes in two arguments: \'python main.py [user_handle] [number_of_recommended_users]\'")
		sys.exit()
	try:
		current_user = api.get_user(user_handle)
	except tweepy.error.TweepError as e:
		# if user_handle doesn't exist
		if e.api_code == 50:
			print(user_handle + " doesn't exist. try another one!")
		# if user_handle is private
		elif e.api_code == 150:
			print("this handle is private. try another one!")
		sys.exit()
	#print(current_user)

	for f in api.friends_ids(current_user.id):
		try:
			#print(api.get_user(f).screen_name)
			for mutual_friend in api.friends_ids(f):
				#print(api.get_user(mutual_friend).screen_name)
				# make sure you aren't following user already
				if api.exists_frienship(current_user, mutual_friend):
					mutual_dict[mutual_friend] += 1
					
		except tweepy.error.TweepError as e:
			# note: 150 = private acc, 420 = disconnect
			pass

	return find_max_val(mutual_dict, num_rec)

# return keys with top _num_ vals in dictionary
def find_max_val(d, num):
	top_keys = []
	for i in range(0, num):
		max_val = 0
		max_key = None
		for key, val in d.items():
			if val > max_val:
				max_val = val
				max_key = key
		top_keys.append(api.get_user(max_key).screen_name)
		d[max_key] = -1
	return top_keys




# not in use
def get_following(user_handle):

	# The user and his/her ID, to be used in search.
	current_user = api.get_user(user_handle)
	user_id = current_user.id
	#print(current_user)

	temp_following = []

	# Get IDs of all "friends" of user, or users that the user is following.
	for user in api.friends_ids(user_id):
		print(user)
		temp_following.append(user)
		'''
		try:
			temp_following.append(user)
		except tweepy.TweepError:
			time.sleep(60 * 15)
			continue
		except StopIteration:
			break
			'''
	return temp_following

# not in use
def get_recommended_dict(following_array):
	temp_dict = dict()

	for user_id in following_array:
		user_obj = api.get_user(user_id)
		for mutual_user in api.friends_ids(user_id):
			# Temp method: use user_id as dict; may update to user_obj
			if mutual_user not in temp_dict:
				temp_dict[mutual_user] = 1
			else:
				temp_dict[mutual_user] += 1

	return temp_dict

# not in use
def print_top_recommended(rec_dict):
	temp_top = []
	for i in range(0, 10):
		temp_top.append(max(rec_dict, key=lambda k: rec_dict[k]))

	for user in temp_top:
		print(user)
	return temp_top


if __name__ == "__main__":
	print(test_methods(sys.argv[1], sys.argv[2]))

	#following = get_following("_")

	#print("hi")

	#friend_dict = get_recommended_dict(following)
	#print_top_ten_recommended(friend_dict)
