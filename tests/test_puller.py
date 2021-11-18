import unittest

from dsdc.dockerhub.puller import collect_sensitive_data_from_tag


class DefaultPullerTestCase(unittest.TestCase):
    """ Test module 'puller' """

    def test_extract_sensitive_data_from_tag(self):
        """ test sensitive content extracted from remote docker image """
        # Given
        repository = "adioss/dontreproduceathome"
        tag = "latest"

        # When
        data_from_tag = collect_sensitive_data_from_tag(repository, tag)

        # Then
        self.assertTrue(len(data_from_tag) == 1)
        self.assertEqual(data_from_tag[0].value, 'bFIiK2Ta5Ed3MEPJcnXzbJb01yRByZnrWMAxLpMa')
