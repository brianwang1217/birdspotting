import os
import tweepy
import config
import sys

auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
auth.set_access_token(config.access_token, config.access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

following = []
friend_dict = dict()


def test_methods(user_handle, num_rec):
	mutual_dict = dict()

	friends_array = []

	try:
		current_user = api.get_user(user_handle)
	except tweepy.error.TweepError as e:
		# if user_handle doesn't exist
		if e.api_code == 50:
			print("this handle doesn't exist. try another one!")
			sys.exit()
		# if user_handle is private
		elif e.api_code == 150:
			print("this handle is private. try another one!")
			sys.exit()
	#print(current_user)
	curr_friends = api.friends_ids(current_user.id)
	for friend in curr_friends:
		#print (api.get_user(friend).screen_name)

		# Gives ID of friend user.
		friends_array.append(friend)

	for f in friends_array:
		mutual_friends_array = []

		try:
			#print(api.get_user(f).screen_name)
			mutual_friends_array = api.friends_ids(f)
			for mutual_friend in mutual_friends_array:
				print(api.get_user(mutual_friend).screen_name)
				if mutual_friend not in mutual_dict:
					mutual_dict[mutual_friend] = 1 
				else:
					mutual_dict[mutual_friend] += 1
					
		except tweepy.error.TweepError as e:
			# note: 150 = private acc, 420 = disconnect
			pass

	return (find_max_val(mutual_dict, num_rec))

# return keys with top _num_ vals in dictionary
def find_max_val(dict, num):
	top_keys = []
	for i in range(0, num):
		max_val = 0
		max_key = None
		for key, val in dict.items():
			if val > max_val:
				max_val = val
				max_key = key
		top_keys.append(max_key)
		dict[max_key] = -1
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
	print(test_methods(sys.argv[0], sys.argv[1]))

	#following = get_following("Lil_Drizzles")

	#print("hi")

	#friend_dict = get_recommended_dict(following)
	#print_top_ten_recommended(friend_dict)