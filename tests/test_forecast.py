from src.forecast.survey_spec import SurveySpec

def test_survey_grid():

    s = SurveySpec("test",0.1,1.0,5,5)

    z = s.redshift_grid()

    assert len(z) == 5
