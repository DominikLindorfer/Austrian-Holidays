## Austrian-Holidays

Austria has a considerable amount of public holidays (see e.g. [here](https://www.austria.info/en/service-and-facts/about-austria/holidays-daylight-savings-time)) resulting in many bridge-days per year, i.e. days between the public holiday and the weekend. This project counts the number of bridge-days per year and sends out reminder e-mails three weeks before a bridge-day, so we can book time off work.

### Usage

Please fill in the smtp server, your e-Mail address and the year you want to get reminder Mails, accordingly:

```python
config = {
            "to_address" : "dominik.lindorfer@posteo.at",
            "from_address" : "Reminder Zwickeltag <dominik.lindorfer@posteo.at>",
            "smpt" : None,
            "year" : 2023
}
```

The reminder e-Mail that is sent out works for Microsoft Outlook 2019 and ongoing:


![image](https://github.com/DominikLindorfer/Austrian-Holidays/assets/21077042/9e237e8c-8e27-4e2d-8658-81caca78382b)
