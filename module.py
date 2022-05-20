import re
import pandas as pd
from unidecode import unidecode


class Extractor(object):
    def __init__(self):
        self.phone_pattern = r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
        self.addr_sign_pattern = "(xã|ấp|phố|phường|đường|thôn|thị trấn|khu công nghiệp|quận|huyện|tỉnh|thành phố|phố)"
        self.__init_complex_pattern__()

    def process(self, message):
        """
        extract phone number and address
        :param message: string, input message
        :return: {
                  "set_attributes": {
                    "ship_address": "some value",
                    "phone_number": "0xxx"
                  }
                } 
                form message
        """
        result = {
                  "set_attributes": {
                    "ship_address": "",
                    "phone_number": ""
                  }
                }
        phone_number = re.findall(self.phone_pattern, message)
        result["set_attributes"]['phone_number'] = phone_number
        if len(phone_number) > 0:
            for phone in phone_number:
                message = message.replace(phone, " ")
        message = re.sub(r"\s+", " ", message)
        message_no_sign = unidecode(message).lower()
        message_no_sign_copy = message_no_sign

        score = 0

        if re.search(self.addr_sign_pattern, message):
            score += 0.5  # int threshold => may be

        flag_match_detail = 0
        for pattern in self.pattern_detail:
            match = re.findall(pattern, message_no_sign)
            if len(match) > 0:
                for m in match:
                    if isinstance(m, tuple):
                        for nm in m:
                            message_no_sign_copy = message_no_sign_copy.replace(nm, " ")
                    else:
                        message_no_sign_copy = message_no_sign_copy.replace(m, " ")
                flag_match_detail = 1
        score += flag_match_detail

        flag_match_ward = 0
        match_ward_with_prefix = re.findall(self.pattern_ward_with_prefix, message_no_sign)
        match_ward_with_prefix = [match for match in match_ward_with_prefix if len(match.strip()) > 0]
        if len(match_ward_with_prefix) > 0:
            for m in match_ward_with_prefix:
                message_no_sign_copy = message_no_sign_copy.replace(m, " ")
            flag_match_ward = 1
        else:
            match_ward = re.findall(self.pattern_ward, message_no_sign)
            match_ward = [match for match in match_ward if len(match.strip()) > 0]
            if len(match_ward) > 0:
                for m in match_ward:
                    message_no_sign_copy = message_no_sign_copy.replace(m, " ")
                flag_match_ward = 1
        score += flag_match_ward

        flag_match_district = 0
        match_district_with_prefix = re.findall(self.pattern_district_with_prefix, message_no_sign)
        match_district_with_prefix = [match for match in match_district_with_prefix if len(match.strip()) > 0]
        if len(match_district_with_prefix) > 0:
            for m in match_district_with_prefix:
                message_no_sign_copy = message_no_sign_copy.replace(m, " ")
            flag_match_district = 1
        score += flag_match_district

        flag_match_province = 0
        match_province = re.findall(self.pattern_province, message_no_sign)
        match_province = [match for match in match_province if len(match.strip()) > 0]
        if len(match_province) > 0:
            for m in match_province:
                message_no_sign_copy = message_no_sign_copy.replace(m, " ")
            flag_match_province = 1
        score += flag_match_province
        score_extra = len(message_no_sign) - len(message_no_sign_copy)
        if score > 2 and score_extra > 6:
            result["set_attributes"]["ship_address"] = message
        return result

    def __init_complex_pattern__(self):
        """
        # todo: config if u need
        # todo: idea improve (if necessary): pattern with sign
        make pattern for match
        :return:
        """
        df_addr_detail = pd.read_csv('data/address_detail_202111261358.csv')
        df_ward = pd.read_csv('data/ward_202111261355.csv')
        df_district = pd.read_csv('data/district_202111261354.csv')
        df_province = pd.read_csv('data/province_202111261354.csv')

        self.pattern_detail = df_addr_detail.query('is_active == 1').pattern.tolist()

        pattern_ward = df_ward.sync_words.tolist()
        self.pattern_ward = "|".join([f"{syn_word.strip()}" for syn_word in pattern_ward
                                      if len(syn_word) > 3]).replace(',', "|")
        pattern_ward_with_prefix = df_ward.priority_sync_words.tolist()
        self.pattern_ward_with_prefix = "|".join([f"{syn_word.strip()}" for syn_word in pattern_ward_with_prefix
                                                  if len(syn_word) > 3]).replace(',', "|")

        pattern_district_with_prefix = df_district.sync_words.tolist()
        self.pattern_district_with_prefix = "|".join([f"{syn_word.strip()}" for syn_word in pattern_district_with_prefix
                                                      if len(syn_word) > 3]).replace(',', "|")

        pattern_province = df_province.sync_words.tolist()
        self.pattern_province = "|".join([f"{syn_word.strip()}" for syn_word in pattern_province
                                          if len(syn_word) > 3]).replace(',', "|")


if __name__ == "__main__":
    test_message = "Xa chi cong.tuy phong.binh thuan,gui ra"
    extractor = Extractor()
    df_test = pd.read_excel('data/Địa-chỉ.xlsx')
    result = extractor.process(test_message)
    df_test['api_result'] = df_test['Địa chỉ'].map(lambda x: extractor.process(x))
    df_test.to_csv('data/df_test_result.csv', index=False, encoding='utf-8-sig')
    print(result)
