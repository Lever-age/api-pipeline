# coding: utf-8

import hmac

shared_secret = b'ILIKEWORKINGWITHLEVERAGE'

def generate_hmac(header_row_list, row_dict):

    hmac_calculated = hmac.new(key=shared_secret)

    for f in header_row_list:
        hmac_calculated.update('{}={}'.format(f, row_dict[f]).encode('utf-8'))

    return hmac_calculated.hexdigest()

