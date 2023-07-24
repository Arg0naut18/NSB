"""parent translator class"""

from .deep_search_exceptions import InvalidInput
import string
class BaseTranslator():
    """
    Abstract class that serve as a parent translator for other different translators
    """
    def __init__(self,
                 base_url=None,
                 source="auto",
                 target="ja",
                 payload_key=None,
                 element_tag=None,
                 element_query=None,
                 **url_params):
        """
        @param source: source language to translate from
        @param target: target language to translate to
        """
        if source == target:
            raise InvalidInput(source)

        self.__base_url = base_url
        self._source = source
        self._target = target
        self._url_params = url_params
        self._element_tag = element_tag
        self._element_query = element_query
        self.payload_key = payload_key
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) '
                                      'AppleWebit/535.19'
                                      '(KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'}
        super(BaseTranslator, self).__init__()

    @staticmethod
    def _validate_payload(payload, min_chars=1, max_chars=5000):
        """
        validate the target text to translate
        @param payload: text to translate
        @return: bool
        """

        if not payload or not isinstance(payload, str) or not payload.strip() or payload.isdigit():
            raise InvalidInput(payload)

        # check if payload contains only symbols
        if all(i in string.punctuation for i in payload):
            raise InvalidInput(payload)

        if not BaseTranslator.__check_length(payload, min_chars, max_chars):
            raise InvalidInput(payload, min_chars, max_chars)
        return True

    @staticmethod
    def __check_length(payload, min_chars, max_chars):
        """
        check length of the provided target text to translate
        @param payload: text to translate
        @param min_chars: minimum characters allowed
        @param max_chars: maximum characters allowed
        @return: bool
        """
        return True if min_chars <= len(payload) < max_chars else False

