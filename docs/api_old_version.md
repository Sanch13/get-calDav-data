Получить список переговорных

calendar.section.get
https://bitrix.miran-bel.com/rest/226/yyejq8bt6p3hn4aq/calendar.section.get.json?type=location&ownerId=0

```
{
  "result": [
    {
      "ID": "54",
      "NAME": "Переговорная 1й этаж",
      "GAPI_CALENDAR_ID": null,
      "DESCRIPTION": null,
      "COLOR": "#00ff00",
      "TEXT_COLOR": null,
      "EXPORT": {
        "ALLOW": true,
        "PATH": "https:\/\/bitrix.miran-bel.com",
        "LINK": "\u0026type=location\u0026owner=0\u0026ncc=1\u0026user=226\u0026sec_id=54\u0026sign=67634374ae88bc25d077e26463558788\u0026bx_hit_hash="
      },
      "CAL_TYPE": "location",
      "OWNER_ID": "0",
      "CREATED_BY": "24",
      "DATE_CREATE": "2022-01-12 09:07:00",
      "TIMESTAMP_X": "2026-09-18 14:56:12",
      "CAL_DAV_CON": false,
      "SYNC_TOKEN": null,
      "PAGE_TOKEN": null,
      "EXTERNAL_TYPE": "local",
      "ACCESS": {
        "G2": 17,
        "U226": 17,
        "U24": 19
      },
      "IS_COLLAB": false,
      "PERM": {
        "view_time": true,
        "view_title": true,
        "view_full": true,
        "add": true,
        "edit": true,
        "edit_section": true,
        "access": true
      }
    },
    {
      "ID": "55",
      "NAME": "Переговорная 3й этаж",
      "GAPI_CALENDAR_ID": null,
      "DESCRIPTION": null,
      "COLOR": "#0092cc",
      "TEXT_COLOR": null,
      "EXPORT": {
        "ALLOW": true,
        "PATH": "https:\/\/bitrix.miran-bel.com",
        "LINK": "\u0026type=location\u0026owner=0\u0026ncc=1\u0026user=226\u0026sec_id=55\u0026sign=2a5d9457d5669b9cd1e5020a57991c1a\u0026bx_hit_hash="
      },
      "CAL_TYPE": "location",
      "OWNER_ID": "0",
      "CREATED_BY": "24",
      "DATE_CREATE": "2022-01-12 09:07:00",
      "TIMESTAMP_X": "2026-09-18 14:07:26",
      "CAL_DAV_CON": false,
      "SYNC_TOKEN": null,
      "PAGE_TOKEN": null,
      "EXTERNAL_TYPE": "local",
      "ACCESS": {
        "G2": 17,
        "U226": 17,
        "U24": 19
      },
      "IS_COLLAB": false,
      "PERM": {
        "view_time": true,
        "view_title": true,
        "view_full": true,
        "add": true,
        "edit": true,
        "edit_section": true,
        "access": true
      }
    },
    {
      "ID": "56",
      "NAME": "Переговорная ЦУП",
      "GAPI_CALENDAR_ID": null,
      "DESCRIPTION": null,
      "COLOR": "#e89b06",
      "TEXT_COLOR": null,
      "EXPORT": {
        "ALLOW": true,
        "PATH": "https:\/\/bitrix.miran-bel.com",
        "LINK": "\u0026type=location\u0026owner=0\u0026ncc=1\u0026user=226\u0026sec_id=56\u0026sign=669252bc8eb228179e01ee7a6b5f31db\u0026bx_hit_hash="
      },
      "CAL_TYPE": "location",
      "OWNER_ID": "0",
      "CREATED_BY": "24",
      "DATE_CREATE": "2022-01-12 09:07:00",
      "TIMESTAMP_X": "2026-09-18 14:19:05",
      "CAL_DAV_CON": false,
      "SYNC_TOKEN": null,
      "PAGE_TOKEN": null,
      "EXTERNAL_TYPE": "local",
      "ACCESS": {
        "G2": 17,
        "U226": 19,
        "U24": 19
      },
      "IS_COLLAB": false,
      "PERM": {
        "view_time": true,
        "view_title": true,
        "view_full": true,
        "add": true,
        "edit": true,
        "edit_section": true,
        "access": true
      }
    },
    {
      "ID": "97",
      "NAME": "Учебный класс",
      "GAPI_CALENDAR_ID": null,
      "DESCRIPTION": null,
      "COLOR": "#de2b24",
      "TEXT_COLOR": null,
      "EXPORT": {
        "ALLOW": true,
        "PATH": "https:\/\/bitrix.miran-bel.com",
        "LINK": "\u0026type=location\u0026owner=0\u0026ncc=1\u0026user=226\u0026sec_id=97\u0026sign=1d2e7d95e45e151bcd904ee66452d0d4\u0026bx_hit_hash="
      },
      "CAL_TYPE": "location",
      "OWNER_ID": "0",
      "CREATED_BY": "226",
      "DATE_CREATE": "2025-10-30 10:41:06",
      "TIMESTAMP_X": "2026-09-18 14:19:11",
      "CAL_DAV_CON": false,
      "SYNC_TOKEN": null,
      "PAGE_TOKEN": null,
      "EXTERNAL_TYPE": null,
      "ACCESS": {
        "G2": 17,
        "U226": 19
      },
      "IS_COLLAB": false,
      "PERM": {
        "view_time": true,
        "view_title": true,
        "view_full": true,
        "add": true,
        "edit": true,
        "edit_section": true,
        "access": true
      }
    }
  ],
  "time": {
    "start": 1789971260,
    "finish": 1789971260.820396,
    "duration": 0.8203959465026855,
    "processing": 0,
    "date_start": "2026-09-21T09:14:20+03:00",
    "date_finish": "2026-09-21T09:14:20+03:00"
  }
}
```

########################################################################################################################

Получить список событий за выбранный период у конкретной переговорки

calendar.event.get
https://bitrix.miran-bel.com/rest/226/yyejq8bt6p3hn4aq/calendar.event.get.json?type=location&ownerId=0&from=2026-09-21&to=2026-09-21&section=54

{
"type": "location",
"ownerId": 0,
"from": "2026-09-18",
"to": "2026-09-18",
"section": [54]
}

```json
{
  "result": [
    {
      "ID": "2137",
      "PARENT_ID": "2138",
      "ACTIVE": "Y",
      "DELETED": "N",
      "CAL_TYPE": "location",
      "OWNER_ID": "0",
      "NAME": "Александр Зубчик",
      "DATE_FROM": "21.09.2026 11:00:00",
      "DATE_TO": "21.09.2026 12:00:00",
      "ORIGINAL_DATE_FROM": null,
      "TZ_FROM": "Europe\/Minsk",
      "TZ_TO": "Europe\/Minsk",
      "TZ_OFFSET_FROM": "10800",
      "TZ_OFFSET_TO": "10800",
      "DATE_FROM_TS_UTC": "1789966800",
      "DATE_TO_TS_UTC": "1789970400",
      "DT_SKIP_TIME": "N",
      "DT_LENGTH": 3600,
      "EVENT_TYPE": null,
      "CREATED_BY": "226",
      "DATE_CREATE": "18.09.2026 14:21:21",
      "TIMESTAMP_X": "18.09.2026 14:56:12",
      "DESCRIPTION": "",
      "DT_FROM": null,
      "DT_TO": null,
      "PRIVATE_EVENT": "",
      "ACCESSIBILITY": "busy",
      "IMPORTANCE": "normal",
      "IS_MEETING": false,
      "MEETING_STATUS": "Y",
      "MEETING_HOST": "0",
      "MEETING": null,
      "LOCATION": "",
      "REMIND": [],
      "COLOR": "",
      "TEXT_COLOR": "",
      "RRULE": "",
      "EXDATE": "",
      "DAV_XML_ID": "",
      "G_EVENT_ID": "",
      "DAV_EXCH_LABEL": "",
      "CAL_DAV_LABEL": "",
      "VERSION": "1",
      "ATTENDEES_CODES": null,
      "RECURRENCE_ID": null,
      "RELATIONS": "",
      "SECTION_ID": "54",
      "SYNC_STATUS": null,
      "UF_CRM_CAL_EVENT": null,
      "UF_WEBDAV_CAL_EVENT": null,
      "SECTION_DAV_XML_ID": null,
      "DATE_FROM_FORMATTED": "Mon Sep 21 2026 11:00:00",
      "DATE_TO_FORMATTED": "Mon Sep 21 2026 12:00:00",
      "IS_DAYLIGHT_SAVING_TZ": "N",
      "SECT_ID": "54",
      "OPTIONS": null,
      "ATTENDEE_LIST": [
        {
          "id": 0,
          "entryId": "2137",
          "status": "Y"
        }
      ],
      "COLLAB_ID": null,
      "~USER_OFFSET_FROM": 0,
      "~USER_OFFSET_TO": 0
    }
  ],
  "time": {
    "start": 1789971459,
    "finish": 1789971459.598064,
    "duration": 0.5980639457702637,
    "processing": 0,
    "date_start": "2026-09-21T09:17:39+03:00",
    "date_finish": "2026-09-21T09:17:39+03:00"
  }
}
```

########################################################################################################################

Получить название события, описание события от владельца регистрации события в переговорной комнаты
calendar.event.getbyid

id=PARENT_ID
https://bitrix.miran-bel.com/rest/226/yyejq8bt6p3hn4aq/calendar.event.getbyid.json?type=user&id=2138

```json
{
  "result": {
    "ID": "2138",
    "PARENT_ID": "2138",
    "DELETED": "N",
    "CAL_TYPE": "user",
    "OWNER_ID": "226",
    "NAME": "Очень важная встреча!",
    "DATE_FROM": "21.09.2026 11:00:00",
    "DATE_TO": "21.09.2026 12:00:00",
    "ORIGINAL_DATE_FROM": null,
    "TZ_FROM": "Europe\/Minsk",
    "TZ_TO": "Europe\/Minsk",
    "TZ_OFFSET_FROM": "10800",
    "TZ_OFFSET_TO": "10800",
    "DATE_FROM_TS_UTC": "1789966800",
    "DATE_TO_TS_UTC": "1789970400",
    "DT_SKIP_TIME": "N",
    "DT_LENGTH": 3600,
    "EVENT_TYPE": null,
    "CREATED_BY": "226",
    "DATE_CREATE": "18.09.2026 14:21:00",
    "TIMESTAMP_X": "18.09.2026 14:56:12",
    "DESCRIPTION": "[QUOTE][QUOTE]\r\n[\/QUOTE]\r\n[\/QUOTE]\r\n[QUOTE]Это тестовое событие!![\/QUOTE]",
    "PRIVATE_EVENT": "",
    "ACCESSIBILITY": "busy",
    "IMPORTANCE": "normal",
    "IS_MEETING": true,
    "MEETING_STATUS": "H",
    "MEETING_HOST": "226",
    "MEETING": {
      "NOTIFY": true,
      "MEETING_CREATOR": 226,
      "REINVITE": false,
      "ALLOW_INVITE": false,
      "HIDE_GUESTS": true,
      "HOST_NAME": "Александр Зубчик",
      "LANGUAGE_ID": "ru",
      "MAIL_FROM": "",
      "CHAT_ID": 0
    },
    "LOCATION": "calendar_54_2137",
    "REMIND": [
      {
        "type": "min",
        "count": 15
      }
    ],
    "COLOR": "",
    "RRULE": "",
    "EXDATE": "",
    "DAV_XML_ID": "20260921T080000Z-400400be9cc0ebfa3fed655f6305747e@bitrix.miran-bel.com",
    "G_EVENT_ID": "",
    "DAV_EXCH_LABEL": "",
    "CAL_DAV_LABEL": "",
    "VERSION": "2",
    "ATTENDEES_CODES": [
      "U226",
      "U289"
    ],
    "RECURRENCE_ID": null,
    "RELATIONS": "",
    "SECTION_ID": "68",
    "SYNC_STATUS": null,
    "UF_CRM_CAL_EVENT": null,
    "UF_WEBDAV_CAL_EVENT": [],
    "SECTION_DAV_XML_ID": null,
    "DATE_FROM_FORMATTED": "Mon Sep 21 2026 11:00:00",
    "DATE_TO_FORMATTED": "Mon Sep 21 2026 12:00:00",
    "IS_DAYLIGHT_SAVING_TZ": "N",
    "SECT_ID": "68",
    "OPTIONS": null,
    "ATTENDEE_LIST": [
      {
        "id": 226,
        "entryId": "2138",
        "status": "H"
      },
      {
        "id": 289,
        "entryId": "2139",
        "status": "Y"
      }
    ],
    "COLLAB_ID": null,
    "attendeesEntityList": [
      {
        "entityId": "user",
        "id": 226
      },
      {
        "entityId": "user",
        "id": 289
      }
    ],
    "~DESCRIPTION": "\u003Cdiv class=\u0027quote\u0027\u003E\u003Ctable class=\u0027quote\u0027\u003E\u003Ctr\u003E\u003Ctd\u003E\u003Cdiv class=\u0027quote\u0027\u003E\u003Ctable class=\u0027quote\u0027\u003E\u003Ctr\u003E\u003Ctd\u003E\u003C\/td\u003E\u003C\/tr\u003E\u003C\/table\u003E\u003C\/div\u003E\u003C\/td\u003E\u003C\/tr\u003E\u003C\/table\u003E\u003C\/div\u003E\u003Cdiv class=\u0027quote\u0027\u003E\u003Ctable class=\u0027quote\u0027\u003E\u003Ctr\u003E\u003Ctd\u003EЭто тестовое событие!!\u003C\/td\u003E\u003C\/tr\u003E\u003C\/table\u003E\u003C\/div\u003E",
    "~USER_OFFSET_FROM": 0,
    "~USER_OFFSET_TO": 0
  },
  "time": {
    "start": 1789971691,
    "finish": 1789971691.498984,
    "duration": 0.49898409843444824,
    "processing": 0,
    "date_start": "2026-09-21T09:21:31+03:00",
    "date_finish": "2026-09-21T09:21:31+03:00"
  }
}
```
