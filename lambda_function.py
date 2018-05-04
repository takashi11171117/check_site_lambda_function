from datetime import datetime
import requests
import json

SITE = 'https://virtualspace-lum.com/'  # URL of the site to check
EXPECTED = '仮想空間生活'  # String expected to be on the page
rtn_str = ''


def validate(res):
    '''Return False to trigger the canary

    Currently this simply checks whether the EXPECTED string is present.
    However, you could modify this to perform any number of arbitrary
    checks on the contents of SITE.
    '''
    return EXPECTED in res


def lambda_handler(event, context):
    rtn_str = 'Checking {} at {}...\n'.format(SITE, event['time'])
    try:
        if not validate(requests.get(SITE).text):
            raise Exception('Validation failed')
    except:
        rtn_str += 'Check failed!\n'
        raise
    else:
        rtn_str += 'Check passed!\n'
        return event['time']
    finally:
        rtn_str += 'Check complete at {}'.format(str(datetime.now()))
        print(rtn_str)
        requests.post('https://hooks.slack.com/services/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', data = json.dumps({
            'text': rtn_str, # 投稿するテキスト
            'username': u'me', # 投稿のユーザー名
            'icon_emoji': u':ghost:', # 投稿のプロフィール画像に入れる絵文字
            'link_names': 1, # メンションを有効にする
        }))
