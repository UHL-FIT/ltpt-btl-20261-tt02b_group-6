import pandas as pd


def validate_date(date_str):

    """Kiểm tra chuỗi ngày có thể chuyển đổi sang datetime hợp lệ."""
    try:

        pd.to_datetime(date_str)

        return True

    except:

        return False


def validate_name(name):

    if not name or not name.strip():
        return False

    for ch in name.strip():
        if not (ch.isalpha() or ch.isspace()):
            return False

    return True