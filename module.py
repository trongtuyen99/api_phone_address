import re


class Extractor(object):
    def __init__(self):
        self.phone_pattern = r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
        self.addr_sign_pattern = "(xã|ấp|phố|phường|đường|thôn|thị trấn|khu công nghiệp|quận|huyện|tỉnh|thành phố|phố)"
        self.addr_abbr_pattern = "tp|tphn|tphcm|kcn"

    def process(self, message):
        """
        extract phone number and address
        :param message: string, input message
        :return: {"phone":str, "address":str} form message
        """
        result = {
                    "phone": "",
                    "address": ""
                  }
        phone_number = re.findall(self.phone_pattern, message)
        result['phone'] = phone_number
        if re.search(self.addr_sign_pattern, message) or re.search(self.addr_abbr_pattern, message):
            result["address"] = message
        return result


if __name__ == "__main__":
    test_message = "gui den tp viet tri phu tho 0981198111 "
    extractor = Extractor()
    result = extractor.process(test_message)
    print(result)
