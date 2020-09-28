from datetime import datetime, timedelta


def past_timestamp(**kwargs):
    return str(datetime.timestamp(datetime.now() - timedelta(**kwargs)))


def older_than_threshold(ts, threshold=0):
    return True if float(ts) < float(threshold) else False


def clean_url(link):
    return link.replace("&", "&amp;")
