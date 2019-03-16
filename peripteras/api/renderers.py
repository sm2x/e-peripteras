import json
import re

from rest_framework.renderers import JSONRenderer, six


class CamelCaseJSONRenderer(JSONRenderer):


    def _underscoreToCamel(self, match):
        return match.group()[0] + match.group()[2].upper()

    def camelize(self, data):
        if isinstance(data, dict):
            new_dict = {}
            for key, value in data.items():
                new_key = re.sub(r'[a-z]_[a-z]', self._underscoreToCamel, key)
                new_dict[new_key] = self.camelize(value)
            return new_dict
        if isinstance(data, (list, tuple)):
            for i in range(len(data)):
                data[i] = self.camelize(data[i])
            return data
        return data

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return bytes()

        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)

        camelized_data = self.camelize(data)

        ret = json.dumps(
            camelized_data, cls=self.encoder_class,
            indent=indent, ensure_ascii=self.ensure_ascii
        )

        # On python 2.x json.dumps() returns bytestrings if ensure_ascii=True,
        # but if ensure_ascii=False, the return type is underspecified,
        # and may (or may not) be unicode.
        # On python 3.x json.dumps() returns unicode strings.
        if isinstance(ret, six.text_type):
            return bytes(ret.encode('utf-8'))
        return ret
