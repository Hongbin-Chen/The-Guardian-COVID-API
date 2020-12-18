#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def test_news_type():
    example = ("video")
    expected = results[results['type']=='video']
    assert actual == expected
test_news_type()

