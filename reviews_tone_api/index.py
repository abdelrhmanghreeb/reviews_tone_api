from reviews_tone_api.hotels_avg_tone import get_avg_tones, load_data
from elasticsearch import Elasticsearch
from tqdm import tqdm
import pandas as pd

class Hotels_Index():
	es = None	
	REVIEW_ATTRIBUTES = ['date', 'dateAdded', 'doRecommend', 'rating', 'text', 'title', 'userCity', 'username', 'userProvince']

	def initialize_es(self):
		""" Initialize the elastic search """
		self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

	def index_hotel(self, hotel_name):
		""" Create a single document for the given hotel and index it to ES 
			Parameters: 
				hotel_name: String
					the name of hotel whose information and reviews are to be indexed to ES.
		"""
		hotel_reviews, tones, avg_tones = get_avg_tones(hotel_name, return_hotel_data=True)
		# basic hotel info, based on the provided dataset
		body = {'name': '', 
				'address': '', 
				'categories': '', 
				'city': '', 
				'country': '', 
				'latitude': '', 
				'longitude': '',
				'postalCode': '', 
				'province': '',
				}
		for key in body.keys():
			body[key] = hotel_reviews.iloc[0][key]
		body["reviews_tone_average"] = avg_tones

		reviews = []
		for i, v in hotel_reviews.iterrows():
			review = {}
			for attribute in self.REVIEW_ATTRIBUTES:
				if not pd.isnull(v["reviews."+attribute]):
					review[attribute] = v["reviews."+attribute] 
			review["id"] = (hotel_name + "_" + str(i)).replace(" ", "_")
			review["review_tones"] = tones[i]
			reviews.append(review)
		body["reviews"] = reviews
		try:
			# create or update hotel's document
			self.es.index(index='hotel', id=hotel_name, body=body)
		except Exception as e:
			print(e)
			print(body)


	def create_index(self, hotel_name=None):
		""" Create a single document for the given hotel and index it alongside with its average 
		    review tones to ES. If no name is passed, all hotels in the dataset will be indexed.
		    Parameters:
		    	hotel_name (Optional): String 
		    		the name of hotel whose information and reviews are to be indexed to ES."""
		if self.es is None:
			self.initialize_es()

		if hotel_name is not None:
			self.index_hotel(hotel_name)
		else:
			hotel_names = load_data()
			for hotel_name in tqdm(hotel_names):
				self.index_hotel(hotel_name)

