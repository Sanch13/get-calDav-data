import locale

from datetime import datetime

from utils import (
    get_caldav_config,
    connect_to_calendar,
    get_all_events_json
)

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')  # Установка русской локали

credentials = get_caldav_config()

date_to_search = datetime.now()  # Задайте нужную дату

all_events = connect_to_calendar(**credentials).date_search(start=date_to_search, end=None)  # <class 'caldav.objects.Calendar'>

events_json = get_all_events_json(all_events)

if __name__ == '__main__':
    print(events_json)


# url_miran_by = "https://mail.miran.by/SOGo/dav/a.zubchyk@miran.by/Contacts/users/"
# url_miran_by_2 = "https://mail.miran.by/SOGo/dav/a.zubchyk@miran.by/Contacts/users/a.zubchyk@miran.by"
# url_miran_bel = "https://mail.miran.by/SOGo/dav/a.zubchyk@miran-bel.com/Contacts/users/"
#
# username = 'a.zubchyk@miran.by'
# password = '0)ijig/4[>JLiD,b%&,eeCHIyHGU=G|7P7W'
#
# url_ad = "https://mail.miran.by/SOGo/dav/"
#
# get_address_book(url_miran_by_2,
#                  username=username,
#                  password=password)


