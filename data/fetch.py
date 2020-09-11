import pandas as pd

# get data
url_problems = "https://github.com/e-sr/moonboard/blob/master/problems/fetch/moonboard_problems_setup_2016.json"
url_setup = "https://github.com/e-sr/moonboard/blob/master/problems/HoldSetup.json"
problems = pd.read_json(url_problems)
setup = pd.read_json(url_setup)
