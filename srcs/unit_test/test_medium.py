import sys
import json
import unittest
sys.path.append('srcs')
from medium import Story

JSON_DATA = 'srcs/unit_test/test_data/scraped.json'
CHROME = '/usr/local/bin/chromedriver'


class TestStory(unittest.TestCase):

    def setUp(self):
        self.chrome_driver = CHROME
        # simple stories to scrape
        self.simple_story_url = [
            'https://laurajedeed.medium.com/afghanistan-meant-nothing-9e3f099b00e5',
        ]
        # stories with many pictures
        self.pics_story_url = [
            'https://towardsdatascience.com/improve-linear-regression-for-time-series-forecasting-e36f3c3e3534',
            'https://towardsdatascience.com/xgboost-regression-explain-it-to-me-like-im-10-2cf324b0bbdb',
            'https://medium.datadriveninvestor.com/4-simple-steps-in-building-ocr-1f41c66099c1',
            'https://medium.com/neo4j/article-recommendation-with-personalized-pagerank-and-full-text-search-c0203dd833e8',
            'https://thoughts.t37.net/how-we-reindexed-36-billions-documents-in-5-days-within-the-same-elasticsearch-cluster-cd9c054d1db8',
        ]
        # stories with sections
        self.section_story_url = [
            'https://towardsdatascience.com/nerf-and-what-happens-when-graphics-becomes-differentiable-88a617561b5d',
        ]
        # stories with codes, section, lists
        self.hard_story_url = [
            'https://medium.com/@avra42/streamlit-python-cool-tricks-to-make-your-web-application-look-better-8abfc3763a5b',
            'https://medium.com/swlh/create-rest-api-with-django-and-neo4j-database-using-django-nemodel-1290da717df9',
        ]
        self.gitcodes_story_url = [
            'https://blog.searce.com/tips-tricks-for-using-google-vision-api-for-text-detection-2d6d1e0c6361'
        ]
        # load test data
        with open(JSON_DATA, 'r') as f:
            self.data = json.load(f)

    def test_simple(self):
        """ Test simple stories with only texts. """
        print(f'\n')
        for story_url in self.simple_story_url:
            print(f'Testing: {story_url}')
            story = Story(story_url)
            story.scrape(chrome=self.chrome_driver)
            expected = self.data[story_url]
            self.assertEqual(expected['author'], story.author)
            self.assertEqual(expected['length'], story.length)
            self.assertEqual(expected['title'], story.title)
            self.assertSequenceEqual(expected['tags'], story.tags)
            self.assertSequenceEqual(expected['content'], story.content)

    def test_pictures(self):
        """ Test stories containing many pictures. """
        print(f'\n')
        for story_url in self.pics_story_url:
            print(f'Testing: {story_url}')
            story = Story(story_url)
            story.scrape(chrome=self.chrome_driver)
            expected = self.data[story_url]
            self.assertEqual(expected['author'], story.author)
            self.assertEqual(expected['length'], story.length)
            self.assertEqual(expected['title'], story.title)
            self.assertSequenceEqual(expected['tags'], story.tags)
            self.assertSequenceEqual(expected['content'], story.content)

    def test_section(self):
        """ Test stories containing sections. """
        print(f'\n')
        for story_url in self.section_story_url:
            print(f'Testing: {story_url}')
            story = Story(story_url)
            story.scrape(chrome=self.chrome_driver)
            expected = self.data[story_url]
            self.assertEqual(expected['author'], story.author)
            self.assertEqual(expected['length'], story.length)
            self.assertEqual(expected['title'], story.title)
            self.assertSequenceEqual(expected['tags'], story.tags)
            self.assertSequenceEqual(expected['content'], story.content)

    def test_hard(self):
        """ Test stories containing texts, codes, sections and lists. """
        print(f'\n')
        for story_url in self.hard_story_url:
            print(f'Testing: {story_url}')
            story = Story(story_url)
            story.scrape(chrome=self.chrome_driver)
            expected = self.data[story_url]
            self.assertEqual(expected['author'], story.author)
            self.assertEqual(expected['length'], story.length)
            self.assertEqual(expected['title'], story.title)
            self.assertSequenceEqual(expected['tags'], story.tags)
            self.assertSequenceEqual(expected['content'], story.content)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
