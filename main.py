"""
The moonboard is a fixed-size grid
 indexed by capitalized roman letters {A,...,K} horizontally and
 indexed by integers {1,...,18} vertically.
 Each grid point has a fixed hold attached to it.
 A given setup specifiex the hold type and hold orientation
 on every grid point.
 For every official setup there is a collection of boulder problems, which
 are specified simply as set of coordinates, designating the holds
  that may be used when climbing the board.

 Here we consider the 2016 moonboard setup, which has the largest
 collection of problems (TODO: verify).

 For now we don't need the setup, because it is fixed for the entire dataset
 and all holds are different within the setup.
 """
import data
import os
import json
import tensorflow as tf
import numpy as np
from typing import Dict, Tuple, Sequence, Any, List



############################# HARD-CODED #######################################
YEAR = '2016'
PATHS = {}
PATHS['setup'] = os.path.join(os.getcwd(), 'data', 'setup.json')
PATHS['problems'] = os.path.join(os.getcwd(), 'data', 'problems_{}.json'.format(YEAR))

grade_mapping = {   '6B+':1,  '6C' :2,  '6C+':3,
                    '7A' :4,  '7A+':5,  '7B' :6,
                    '7B+':7,  '7C' :8,  '7C+':9,
                    '8A' :10, '8A+':11, '8B':12 }
 # 25907 problems
horizontal = ['A', 'B', 'C', 'D','E', 'F', 'G', 'H', 'I', 'J', 'K']
vertical = [i for i in range(1,19)]

################################################################################
# define a numeric moonboard grid (coordinate system)
def get_location_map(
            horizontal: List[str],
            vertical: List[int]
            ) -> Dict[str, Any]:
            """
            Maps board locations from string (e.g. "A18") to a tuple (e.g. (1,18))
            that corresponds to integer coordinates on a 11x18 grid as Dict[str, Tuple[int,int]].
            """
            location_map = {}
            location_map['horizontal_dim'] = len(horizontal)
            location_map['vertical_dim'] = len(vertical)
            for number in vertical:
                number_for_letter = 1
                for letter in horizontal:
                    location_map[letter+str(number)] = (number_for_letter, number)
                    number_for_letter += 1
            return location_map

# load data
def load_data(paths: Dict[str,str]) -> Dict[str, Any]:
    """
    reads problem and setup json-data from /data`

    """
    with open(paths['setup'], 'r') as f:
         tmp = json.load(f)
         setup = tmp[YEAR]
    with open(paths['problems'], 'r') as f:
         problems = json.load(f)
    return setup, problems


def preprocess(location_map: Dict[str, Any], problems: Dict[str, Any]) -> (Any, Any):
    """
    # Prepares data set.
    Each example is a 2-dimensional boolean list indicating the hold location.

    """
    labels = []
    examples = [] #
    for problem_number, value in problems.items():
        # get grade as integer numeric label
        labels.append(grade_mapping[value['Grade']])
        # get moves from json and represent as integer-valued 2-dim np array
        example = get_moves_board(value['Moves'], location_map)
        examples.append(example)
    return labels, examples

def get_moves_board(
        moves: List[Dict[str, Any]],
        location_map: Dict[str, Any]
        )-> np.ndarray:
        """
        Maps moves from json file to two-dimensional numpy array,
            with integers indicating:
                    # 1 for regular moves
                    # 2 for starting holds
                    # 3 for finishing holds
        """
        n = location_map["horizontal_dim"]
        m = location_map["vertical_dim"]
        boolean_board = np.zeros((n,m), dtype=np.uint8)  # initialize board mapping (zeros(11,18))
        for move in moves :
            i, j = location_map[move["Description"]]
            IsStart =  move["IsStart"]
            IsEnd =  move["IsEnd"]
            if IsStart and IsEnd:
                boolean_board[i,j] = 4 # hypothetical occurance only
            elif IsStart: # ATTENTION, "false" not "False"
                boolean_board[i,j] = 3
            elif IsEnd:
                boolean_board[i,j] = 2
            else:
                boolean_board[i,j] = 1
        return boolean_board



# Driver code
location_map = get_location_map(horizontal, vertical)
setup, problems = load_data(PATHS)
labels, examples = preprocess(location_map, problems)


"""
{'8A+': 59, '6B+': 8394, '6C': 2609, '7A+': 2769,
'7C': 1214, '6C+': 3844, '7A': 3569, '7B': 1218,
'7C+': 434, '7B+': 1542, '8B+': 29, '8A': 198, '8B': 28}
"""
""" old code """
# Don't need after introducing mapping
def get_grade_dict(grade_string: str) -> Dict[str, Any]:
    grade_dict = {}
    grade_dict['g_number'] = grade_string[0]
    grade_dict['g_letter'] = grade_string[1]
    if len(grade_string) == 3: #there is a '+'
        grade_dict['g_increment'] = grade_string[2]
    else:
        grade_dict['g_increment'] = None
    return grade_dict
# Don't need, take len(problems)
def count_grade_instances(
    g_instances : Dict[str, Any],
    new_grade: str) -> Dict[str, int]:
    if new_grade in g_instances :
        g_instances[new_grade] += 1
    else:
        g_instances[new_grade] = 1

"""
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

"""
