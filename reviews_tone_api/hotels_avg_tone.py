import pandas as pd
from tqdm import tqdm
from reviews_tone_api.analyze_tone import analyze_tone

REVIEWS = None

def itemwise_avg(list_of_dicts):
	""" Calculate itemwise average of items in multiple dictionaries parameters:
		Parameters:
			list_of_dicts: List[dict]
				  list of dictionaries whose item-wise avg to be calculated
		Return: Dict
			Dictionary of itemwise average. """

	df = pd.DataFrame(list_of_dicts)
	return dict(df.mean().round(2))

	"""
	# alternative method using the built in collection lib instead of pandas
	sums = Counter()
	key_counters = Counter()
	for i in list_of_dicts:
		sums.update(i)
		key_counters.update(i.keys())
	return {x: float(sums[x])/counters[x] for x in sums.keys()}
	"""

def load_data(datapath="reviews_tone_api/data/7282_1.csv"):
	""" Load data and print statistics
	parameters:
		datapath: String
				  path to the csv file containing the data 
	returns: 
		hotel names: list[String]
				  list of hotel names
		"""
	global REVIEWS
	if REVIEWS is None:
		REVIEWS = pd.read_csv(datapath, sep=",", index_col=None)
		# Assumptions: Accepted reviews has a value that is not None at least in its title or text fields
		REVIEWS.dropna(subset=['reviews.text', 'reviews.title'], how="all", inplace=True)
	REVIEWS = REVIEWS[REVIEWS["categories"]=="Hotels"]
	hotel_names = REVIEWS.name.value_counts().keys()
	print("Loaded {reviews_num} reviews for {hotels_num} different hotels\n".format(
		reviews_num=len(REVIEWS),
		hotels_num=len(hotel_names)))
	return hotel_names

def get_reviews(hotel_name):
	""" Gets the average tones for a hotel reviews given its name
		parameters:
			hotel_name: String
						name of the hotel whose reviews are to be tone evaluated """
	try:
		hotel_reviews = REVIEWS[REVIEWS["name"]==hotel_name].reset_index()
		print ("found {} reviews for {}".format(len(hotel_reviews), hotel_name))
		return(hotel_reviews)
	except Exception as e:
		print("Failed to get any reviews for the given hotel")

def get_tones(hotel_reviews)	:
	""" Get the sentimental tones from Watson tone analyzer for the given reviews """
	tones = []
	for index, review in tqdm(hotel_reviews.iterrows()):
		review_text = ""
		review_title, review_body = review["reviews.title"], review["reviews.text"]
		if not pd.isnull(review_title):
			review_text = review_title
		if not pd.isnull(review_body):
			review_text = review_text + " " + review_body
		try:
			raw_result = analyze_tone(review_text)
			# parsing the raw result
			result = {}
			for i in raw_result['document_tone']['tones']:
				result.update({i["tone_id"] : i["score"]})
			tones.append(result)
		except Exception as e:
			print ("Problem getting the tone analysis of the review #{r_id} whose text is {review_text}".format(
				r_id=review["reviews.id"], r_text=review_text))
	return tones

def get_avg_tones(hotel_name, return_hotel_data=False):
	""""""
	if REVIEWS is None:
		_ = load_data()
	hotel_reviews = get_reviews(hotel_name)
	tones = get_tones(hotel_reviews)
	avg_tones = itemwise_avg(tones)
	if return_hotel_data:
		return hotel_reviews, tones, avg_tones
	else:
		return avg_tones

