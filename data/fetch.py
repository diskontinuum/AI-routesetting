import json
import os
import requests

"""
Gets and saves the .json files from github that specify the 2016 moonboard setup
and the collection of problems.
"""
############################### Hard-coded #####################################
YEAR = '2016'
PATHS = {"input":{}, "output":{}}
PATHS["input"]["setup"]= "https://raw.github.com/e-sr/moonboard/master/problems/HoldSetup.json"
PATHS["input"]["problems"]= "https://raw.github.com/e-sr/moonboard/master/problems/fetch/moonboard_problems_setup_{}.json".format(YEAR)
PATHS["output"]["setup"] = os.path.join(os.getcwd(), "setup.json")
PATHS["output"]["problems"] = os.path.join(os.getcwd(), "problems_{}.json".format(YEAR))
################################################################################

class BoardData():
    def __init__(self, input, output):
        self.url = input
        self.outpath = output
    def fetch(self):
        data = requests.get(self.url)
        self.data = data.json()
    def write(self):
        with open(self.outpath, 'w') as outfile:
            json.dump(self.data, outfile)

# get setup data
setup = BoardData(input=PATHS["input"]["setup"],output=PATHS["output"]["setup"])
setup.fetch()
setup.write()
# get problems data
problems = BoardData(input=PATHS["input"]["problems"],output=PATHS["output"]["problems"])
problems.fetch()
problems.write()

"""
**setup structure**
 "2016": {
      "H7": {
         "HoldSet": "OS",
         "Hold": 1,
         "Orientation": "SE}
         ...}
**problems structure** "341208": {
      "Method": "Feet follow hands",
      "Name": "OFF THE MATTRESS",
      "Grade": "8A+",
      "MoonBoardConfigurationId": 0,
      "Setter": {
         "Nickname": "bcy",
         "Firstname": "Bocheng",
         "Lastname": "Yang"
      },
      "Rating": 0,
      "Repeats": 0,
      "Holdsetup": {
         "Id": 1,
         "Description": "MoonBoard 2016",
         "HoldLayoutId": 0
      },
      "IsBenchmark": false,
      "IsAssessmentProblem": false,
      "Moves": [
         {
            "Id": 1910055,
            "Description": "K18",
            "IsStart": false,
            "IsEnd": true
         },
         {
            "Id": 1910056,
            "Description": "K16",
            "IsStart": false,
            "IsEnd": false
         },
         {
            "Id": 1910057,
            "Description": "F15",
            "IsStart": false,
            "IsEnd": false
         },
         {
            "Id": 1910058,
            "Description": "B11",
            "IsStart": false,
            "IsEnd": false
         },
         {
            "Id": 1910059,
            "Description": "A5",
            "IsStart": true,
            "IsEnd": false
         },
         {
            "Id": 1910060,
            "Description": "H15",
            "IsStart": false,
            "IsEnd": false
         }
      ],
      "DateInserted": "/Date(1554298797933)/"
   },
   "341206":
   ...
"""
