import vk
import re
from datetime import date, time
from time import ctime, sleep, mktime, strptime


class GetPosts:
    """
    Получиние и парсинг информации из группы вк иетодом wall.get.
    Возращает список словарей, каждый словарь это отдельнй распарсеный пост.
    attachments - Медиа элемент поста (фото, видео, аудио и тд.).
    key - Уникальный ключь поста, для предотвраще повторяющихся постов. (Параметр пока удален)
    text - Текст поста.
    """

    def __init__(self, *, api, offset=1, count=1, domain=None):

        self.api = api
        self.offset = offset
        self.count = count
        self.domain = domain
        self.data = []

        try:
            self.wells = self.api.wall.get(owner_id=self.domain, offset=self.offset, count=self.count, filter='all')
        except:
            self.wells = self.api.wall.get(domain=self.domain, offset=self.offset, count=self.count, filter='all')

        self.parse()

    def parse(self):
        for well in self.wells:
            if int is type(well):
                continue

            attachments = []
            if well.setdefault('attachments'):
                for items in well['attachments']:

                    if items.setdefault('audio'):
                        owner_id = items['audio']['owner_id']
                        aid = items['audio']['aid']
                        audio = 'audio{}_{}'.format(owner_id, aid)
                        attachments.append(audio)

                    if items.setdefault('photo'):
                        owner_id = items['photo']['owner_id']
                        pid = items['photo']['pid']
                        photo = 'photo{}_{}'.format(owner_id, pid)
                        attachments.append(photo)

                    if items.setdefault('video'):
                        owner_id = items['video']['owner_id']
                        vid = items['video']['vid']
                        video = 'video{}_{}'.format(owner_id, vid)
                        attachments.append(video)

                    if items.setdefault('doc'):
                        owner_id = items['doc']['owner_id']
                        did = items['doc']['did']
                        doc = 'doc{}_{}'.format(owner_id, did)
                        attachments.append(doc)

            text = re.sub(r'\<[^>]*\>', '', well['text'])
            text = re.sub(r'#[\w]*@[\w]*', '', text)
            self.data.append({'attachments': attachments, 'text': text})


class AddPosts:
    """
    Добавление поста в группу или добалвение отложенного поста.
    """

    def __init__(self, *, api, year=2017, month=9, day=28, hour=0, minutes=0,
                 step=None, domain='', owner_id='', count=1, offset=0):

        self.api = api
        self.owner_id = owner_id
        self.step = step
        self.minutes = minutes
        self.hour = hour
        self.day = day
        self.year = year
        self.month = month

        self.posts = GetPosts(api=self.api, domain=domain, count=count, offset=offset).data
        self.add()

    @staticmethod
    def data_time(*, year=1971, month=1, day=1, hour=0, minutes=0, second=0):
        d = date(year, month, day)
        t = time(hour, minutes, second)
        return int(mktime(strptime(str(d) + ' ' + str(t), '%Y-%m-%d %H:%M:%S')))

    def add(self):
        nums = 0
        for post in self.posts:
            sleep(2)
            date = AddPosts.data_time(year=self.year, month=self.month, day=self.day,
                                      hour=self.hour, minutes=self.minutes)
            try:
                self.api.wall.post(owner_id=self.owner_id, friends_only='0', from_group='1',
                                   message=post['text'], attachments=post['attachments'], services='',
                                   signed='0', publish_date=date, mark_as_ads='0', guid='')
                nums += 1
                print('{} Добавлен пост : {}'.format(nums, ctime(date)))
            except:
                print('Пост уже запланировано на это время. {}'.format(ctime(date)))

            self.minutes += self.step

            if self.minutes >= 60:
                self.minutes = 0
                self.hour += 1

            if self.hour >= 24:
                self.hour = 0
                self.day += 1

            if self.day > 30:
                self.day = 1
                self.month += 1


if __name__ == '__main__':

    session = vk.AuthSession(access_token='access_token')
    api = vk.API(session)

    year = 2017
    month = 1
    day = 1
    hour = 00
    minutes = 00

    step = 30
    count = 25
    offset = 0

    print('Название группы')
    AddPosts(api=api, year=year, month=month, day=day, hour=hour, minutes=minutes,
             step=step, domain='cloudytech', owner_id='-154175714', count=count, offset=offset)

