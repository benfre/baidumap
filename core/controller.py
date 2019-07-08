# -*- coding:utf-8 -*-
from requests.exceptions import RequestException

from baidumap.api.exceptions import NetError, get_exception
from baidumap.core.collector import Collector
from baidumap.core.status import get_status_from_json
from baidumap.util import log

from PIL import Image
import io

class Controller(object):
    '''
    baidu api core controller
    '''

    def __init__(self, ak_key):
        self._collector = Collector(ak_key)
        return

    def get_single(self, url, collect_keys=None):
        '''
        return single result
        '''
        try:
            status, single_result = self._collector.get_single_result(
                url, collect_keys=collect_keys)
            if not status.is_ok():
                log.warning('response is not Ok: %s' % status)
                raise get_exception(status)
            else:
                log.info('single result collected: %s' % url)
                return single_result
        except RequestException as e:
            log.error('net connection broken')
            raise NetError() from e

    def get_list(self, url, collect_keys=None, **kwargs):
        '''
        return list result
        '''
        try:
            status, list_result = self._collector.get_list_result(
                url, collect_keys=collect_keys, **kwargs)
            if not status.is_ok():
                log.warning('response is not Ok: %s' % status)
                raise get_exception(status)
            else:
                log.info('list result collectd: %s' % url)
                return list_result
        except RequestException as e:
            log.error('net connection broken')
            raise NetError() from e

    def get_image(self, url, collect_keys=None):
        '''
        return image result
        '''
        try:
            url.set_param('ak', self._collector.ak_key)
            response = url.get()
            log.debug('requests GET: %s' % url)
            try:
                json = response.json()
                status = get_status_from_json(json)
                if not status.is_ok():
                    log.warning('response is not Ok: %s' % status)
                raise get_exception(status)
            except ValueError:
                pass # this is normal, we should get a png file
            imageStream = io.BytesIO(response.content)
            image = Image.open(imageStream)
            return image
        except RequestException as e:
            log.error('net connection broken')
            raise NetError() from e

    pass
