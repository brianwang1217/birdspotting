import os
import tweepy
import config


auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
auth.set_access_token(config.access_token, config.access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

following = []
friend_dict = dict()
mutual_dict = dict()


def test_methods():
	friends_array = []

	current_user = api.get_user("Lil_Drizzles")
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
		except:
			pass

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

def print_top_ten_recommended(rec_dict):
	temp_top_ten = []
	for i in range(0, 10):
		temp_top_ten.append(max(rec_dict, key=lambda k: rec_dict[k]))

	for user in temp_top_ten:
		print(user)
	return temp_top_ten


if __name__ == "__main__":
	test_methods()

	#following = get_following("Lil_Drizzles")

	#print("hi")

	#friend_dict = get_recommended_dict(following)
	#print_top_ten_recommended(friend_dict)