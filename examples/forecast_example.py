import numpy as np

from src.models.lcdm import LCDMModel
from src.forecast.survey_spec import SurveySpec
from src.forecast.mock_data import generate_mock

survey = SurveySpec("mock",0.1,1.5,15,5)

z = survey.redshift_grid()

model = LCDMModel()

data = generate_mock(model,z,survey.sigma)

print("mock H(z) data")
print(data)
