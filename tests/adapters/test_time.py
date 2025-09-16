from football_pipeline.adapters import time


def test_time_now():
    assert time.time_now() != time.fake_time_now()


def test_new_guid():
    assert time.new_guid() != time.fake_new_guid()
