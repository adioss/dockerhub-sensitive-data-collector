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

    def test_Contains_Aws_Credential_File_Pattern(self):
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
            {'value': ' aaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa ', 'expected': True},
            {'value': ' aaaa-aaaa-aaaa-aaaa-aaaaaaaaa aaa ', 'expected': False},
            {'value': '{"digest": $url = \'https://download.microsoft.com/download/6/A/A/6AA4EDFF-645B-48C5-81CC'
                      '-ED5963AEAD48/vc_redist.x64.exe\'}', 'expected': False},
        ]
        for tested in tests:
            # When
            result = finder.contains_secret_pattern(tested['value'], finder.SecretPattern.AZURE_CLIENT_SECRET)
            # Then
            self.assertEqual(result, tested['expected'], "Failed: %s" % tested['value'])
