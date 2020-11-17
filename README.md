# Hotel Reviews Analyzer and Indexer
A fully working Flask API that uses IBM Watson's tone analyzer to index hotel reviews to a Elastic Search. Projects requirements can be found [here](https://docs.google.com/document/d/19Gd62uxdqTs5L25B-n0qY-PQ71E25c8s_1JbUWlydQ8/edit?usp=sharing)

## API Documentation
### 1. POST-GET '/avg_tone'
#### Request
Gets the average tones for a hotel reviews given its name. The sent json should be formatted as following:
```
{
    "hotel_name": <string>
                the name of the hotel to get its average tones.
}
```
#### Response
The average tones are returned as a dictionary. Scores are approximated to two numbers.
```
{'tone':'score',..}
```
#### Example
```
> wget <service_url>/avg_tone/Hotel Russo Palace
{'joy': 0.75, 'tentative': 0.71, 'analytical': 0.7, 'confident': 0.78, 'sadness': 0.54}
```

### 2. POST-GET '/index_hotel'
#### Request
Index the data of the given hotel to Elastic Search. The sent json should be formatted as following:
```
{
    "hotel_name": <string>
                the name of the hotel to be indexed.
}
```
If no name was passed, all hotels found in the dataset meeting the requirements* are going to be indexed.

* Requirements: Dataset enteries with `Hotels` in its `categories` value and that at least one of its `reviews.title` and `reviews.text` is not None.

#### Response
For a valid request, a success message is returned.
```
{"message":"Index created successfuly for the given hotel."}
```
or
```
{"message":"Index created successfuly of all hotels."}
```
#### Example
```
> wget <service_url>/index_hotel/
{"message":"Index created successfuly of all hotels."}
```

## Steps to run the service
### Docker
To generate a deployable docker image:
- Add a valid Watson tone analyzer API key at the appropriate place in ```Dockerfile ``` ([line #37](https://github.com/abdelrhmanghreeb/reviews_tone_api/blob/master/Dockerfile#L37))
- Build and run the Dockerimage
```
sudo docker image build <image-name> .
sudo docker image run -p 5000:5000 --env-file=dock.run.vars --name <image-name> -it <image-name>
```
- Now you can send your requests to the service running inside the Docker image. 
Example:
```
curl http://0.0.0.0:5000/<endpoint>/<hotel name>
```
### Unittests
To run unittests:
1- Make sure to add your Watson tones API key to the environemnt 
```
export WATSON_TONE_ANALYZER_API_KEY=<your-key>
```
2- Run the following command when at the directory root
```
python3 -m unittest reviews_tone_api/tests/test.py
```
## Assumptions
- While some entries of the data found in the file `7282_1.csv` do have `Hotels` as part of their `categories` value, they were ignored because they have other categories along side with `Hotels`. This was done for simplicity.
- A review is accepted if it has textual value in either its title or text(body) attributes.
- If the hotel is already indexed in the ES, skip it. This is acheieved by using 'elasticsearch.index' instead of 'elasticsearch.create' method. Routines to update hotel index to add news reviews and update average tones can be added in future work.
- Multi-threading and parallel computing can be used to speed up the service when quering the Watson tone analyzer. This is also left for future work.
- The following structure is used to index the hotel data to elastic search
```
	{'name': '', 
	'address': '', 
	'categories': '', 
	'city': '', 
	'country': '', 
	'latitude': '', 
	'longitude': '',
	'postalCode': '', 
	'province': '',
	"reviews_tone_average": {}
	'reviews': [{
		'id': '',
		'date':'', 
		'dateAdded':'', 
		'doRecommend':'', 
		'rating':'', 
		'text':'', 
		'title':'', 
		'userCity':'', 
		'username':'', 
		'userProvince': '',
		'review_tones':{}}, 
		{}]
	}
```
* For review's id, the hotel name is used after spaces are replaced with underscores and an index is appended to it. For example, the first review of the hotel `Hotel Russo Palace` has the id `Hotel_Russo_Palace_1`

## Service workflow
- Hotel Tone Analyzer Endpoint takes the hotel name as input and gets all the reviews related to this hotel name from the CSV file and gets the emotional tone for this hotel.
- Hotel Indexer Endpoint can work in two modes, the first mode with no input/parameter to index all hotels & their reviews. The second mode when you send hotel name to the endpoint, it gets the emotional tone of this hotel reviews then reindex only this selected hotel along with reviews & calculated tones

## Deliverables
- Fully working API wrapped in a Docker image that is ready for deployment.
- Unittests
- Well documented code uploaded to github
