import unittest

from secrets import finder


class DefaultFinderTestCase(unittest.TestCase):
    """ Test module 'finder' """

    def test_contains_aws_key_pattern(self):
        """ test """
        # Given
        tests = [
            {'value': 'test', 'expected': False},
            {'value': 'tototo AKIA test ', 'expected': True},
            {'value': 'tototo AKIA', 'expected': True},
            {'value': 'AKIA', 'expected': True},
            {'value': ' AKIA-ldskqjq ', 'expected': True},
            {'value': ' AKIAJJBR3C4YPHOVBYCV ', 'expected': True},
            {'value': 'ENV AWS_ACCESS_KEY_ID=AKIAJQGZKV7GX7CFXFUB', 'expected': True},
            {'value': ' TOTOJJBR3C4YPHOVBYCV ', 'expected': False}
        ]
        for tested in tests:
            # When
            result = finder.contains_secret_pattern(tested['value'], finder.SecretPattern.AWS_KEY)
            # Then
            self.assertEqual(result, tested['expected'], "Failed: %s" % tested['value'])

    def test_contains_aws_credential_file_pattern(self):
        """ test """
        # Given
        tests = [
            {'value': 'in /root/.aws/credential ', 'expected': False},
            {'value': 'in /root/.aws/credentials ', 'expected': True}
        ]
        for tested in tests:
            # When
            result = finder.contains_secret_pattern(tested['value'], finder.SecretPattern.CREDENTIAL_FILE)
            # Then
            self.assertEqual(result, tested['expected'], "Failed: %s" % tested['value'])

    def test_contains_aws_secret_pattern(self):
        """ test """
        # Given
        tests = [
            {'value': '/bin/sh -c curl -SLO "http://resin-packages.s3.amazonaws.com/resin-xbuild/v1.0.0/resin-xbuild1'
                      '.0.0.tar.gz  && rm "resin-xbuild1.0.0.tar.gz"   && chmod +x resin-xbuild   && mv resin-xbuild '
                      '/usr/bin   && ln -sf resin-xbuild /usr/bin/cross-build-start   && ln -sf resin-xbuild '
                      '/usr/bin/cross-build-end', 'expected': False},
            {'value': 'tototo bFIiK2Ta5Dd3MEPJcnXzbJb01yRByZnrWMAvLpMa test ', 'expected': False},
            {'value': 'ADD file:093f0723fa46f6cdbd6f7bd146448bb70ecce54254c35701feeceb956414622f in ',
             'expected': False},
            {'value': 'add dir:093f0723fa46f6cdbd6f7bd146448bb70ecce54254c35701feeceb956414622f in ',
             'expected': False},
            {'value': ' ENV AWS_SECRET_ACCESS_KEY=bFIiK2Ta5Dd3MEPJcnXzbJb01yRByZnrWMAvLpMa', 'expected': True},
            {'value': ' ENV AWS_SECRET_ACCESS_KEY=4FcmDrL8tJ7jx7poyV0L5GOVqabM/Mk6wBHQREOH', 'expected': True},
            {'value': 'tototo aws bFIiK2Ta5Dd3MEPJcnXzbJb01yRByZnrWMAvLpMa test ', 'expected': True},
            {'value': 'https://apk.corretto.aws/amazoncorretto.rsa.pub && '
                      'SHA_SUM=\"6cfdf08be09f32ca298e2d5bd4a359ee2b275765c09b56d514624bf831eafb91', 'expected': False},
        ]
        for tested in tests:
            # When
            result = finder.contains_secret_pattern(tested['value'], finder.SecretPattern.AWS_SECRET)
            # Then
            self.assertEqual(result, tested['expected'], "Failed: %s" % tested['value'])

    def test_contains_github_key_pattern(self):
        """ test """
        # Given
        tests = [
            {'value': 'titi ghp_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa123456 tutu ', 'expected': True}
        ]
        for tested in tests:
            # When
            result = finder.contains_secret_pattern(tested['value'], finder.SecretPattern.GITHUB_KEY)
            # Then
            self.assertEqual(result, tested['expected'], "Failed: %s" % tested['value'])

    def test_contains_azure_client_secret_pattern(self):
        """ test """
        # Given
        tests = [
            {'value': 'ENV AZURE_ID=c35ba882-b5ed-405f-b929-39e8d8abd3f6 test', 'expected': True},
            {'value': 'ENV azure_id=c35ba882-b5ed-405f-b929-39e8d8abd3f6', 'expected': True},
            {'value': 'data before ENV azure_id=c35ba882-b5ed-405f-b929-39e8d8abd3f6 data after', 'expected': True},
            {'value': ' aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa ', 'expected': False},
            {'value': 'ENV AZURE_ID=a882-b5ed-405f-b929-39e8d8abd3f6', 'expected': False},
            {'value': 'ENV WEBSITE_ID=c35ba882-b5ed-405f-b929-39e8d8abd3f6', 'expected': False},
            {'value': '854600d3-f5d9-45d7-9ff2-17d851f2831a', 'expected': False},
            {'value': '{"digest": $url = \'https://download.microsoft.com/download/6/A/A/6AA4EDFF-645B-48C5-81CC'
                      '-ED5963AEAD48/vc_redist.x64.exe\'}', 'expected': False},
        ]
        for tested in tests:
            # When
            result = finder.contains_secret_pattern(tested['value'], finder.SecretPattern.AZURE_CLIENT_ID)
            # Then
            self.assertEqual(result, tested['expected'], "Failed: %s" % tested['value'])

    def test_contains_npm_token_pattern(self):
        """ test """
        # Given
        tests = [
            {'value': 'NPM_TOKEN=affa60d0-4fb5-4f88-9745-6c244e29372a', 'expected': True},
            {'value': '1 NPM_TOKEN=affa60d0-4fb5-4f88-9745-6c244e29372a /bin/sh -c apt-get update ', 'expected': True},
            {'value': '2 NPM_KEY=08a0a385-e6e2-4f3a-b96b-feaf0a574d36 NPM_REPO=https://registry.npmjs.org/ ',
             'expected': True},
            {'value': '{"digest": $url = \'https://download.microsoft.com/download/6/A/A/6AA4EDFF-645B-48C5-81CC'
                      '-ED5963AEAD48/vc_redist.x64.exe\'}', 'expected': False},
        ]
        for tested in tests:
            # When
            result = finder.contains_secret_pattern(tested['value'], finder.SecretPattern.NPM_TOKEN)
            # Then
            self.assertEqual(result, tested['expected'], "Failed: %s" % tested['value'])
