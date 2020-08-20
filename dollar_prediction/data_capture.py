"""
Для сбора новостей использован сервис GoogleNews и его API
Для сбора курса доллара использовано API сайта https://exchangeratesapi.io/
"""

import datetime
from GoogleNews import GoogleNews
import requests
import csv
from multiprocessing.pool import ThreadPool


URL = 'https://api.exchangeratesapi.io/{}?base=USD'
tags = ['politics', 'economy', 'technology', 'oil']


class Major:
    """
    класс реализует загрузку новостей по заданным тегам и курса доллара через указанный промежуток времени
    и представляет всю собранную информацию в виде csv файла
    """
    def __init__(self, from_date_, to_date_, delta_=7):
        """
        :param from_date_: дата, с начала которой необходимо загружать данные (в виде кортежа вида (год, месяц, день))
        :param to_date_: дата, до которой необходимо загружать данные (в виде кортежа вида (год, месяц, день))
        :param delta_: интервал времени, за который необходимо собрать информацию в качестве одной записи
        """
        self.from_date = datetime.datetime(from_date_[0], from_date_[1], from_date_[2]).date()
        self.to_date = datetime.datetime(to_date_[0], to_date_[1], to_date_[2]).date()
        self.delta = delta_

    @staticmethod
    def __to_api_form(start, end):
        """
        возвращающает вводимые даты в удобном для API виде
        """
        d = str(start).split('-')
        f = d[1:] + d[:1]
        d = str(end).split('-')
        t = d[1:] + d[:1]
        return '/'.join(f), '/'.join(t)

    def __news_request(self, tag, dates):
        """
        :param tag: тег новости
        :param dates: кортеж из двух дат: гранцы временного поиска
        :return: 5 новостей по введенному тегу
        """
        print('=== {} - start ==='.format(tag))
        googlenews = GoogleNews(lang='ru', start=dates[0], end=dates[1])
        googlenews.search('{}'.format(tag))
        titles = googlenews.gettext()
        googlenews.clear()
        print('=== {} - end ==='.format(tag))
        return '\n'.join(titles[:5])

    def __load_news(self, current_date):
        """
        загружает новости. Распараллеливает вызовы к API
        :param current_date: дата, от которой следует собирать информацию
        :return: словарь из тегов и соответствующих им новостей
        """
        delta_date = current_date + datetime.timedelta(days=self.delta)
        dates = Major.__to_api_form(current_date, delta_date)
        text = dict()
        for tag in tags:
            text[tag] = []

        pool = ThreadPool(processes=len(tags))
        tasks = {}
        for tag in tags:
            tasks[tag] = pool.apply_async(self.__news_request, (tag, dates))

        results = {}
        for tag in tags:
            results[tag] = tasks[tag].get()

        return results

    def __load_dollar(self, current_date):
        """
        загружает курс доллара по введенной дате
        :param current_date: дата
        :return: курс доллара или None
        """
        delta_date = current_date + datetime.timedelta(days=self.delta)
        request = requests.get(URL.format(str(delta_date)))
        if request.status_code == 200:
            rub = request.json()['rates']['RUB']
            return round(rub, 6)
        else:
            return None

    def data_capture(self):
        """
        основная функция сбора всей информации, управляет вызовами всех предыдущих функций
        основной цикл идет от from_date к to_date каждые delta дней и собирает информацию в общий вид
        :return: собранный словарь, готовый к дальнейшим путешествиям
        """
        current_date = self.from_date
        data = dict()
        for tag in tags:
            data[tag] = []
        data['dollar'] = []
        # data['from_date'] = []
        data['to_date'] = []
        while current_date + datetime.timedelta(days=self.delta) <= self.to_date:
            news = self.__load_news(current_date)
            for tag in tags:
                data[tag].append(news[tag])
            data['dollar'].append(self.__load_dollar(current_date))
            # data['from_date'].append(str(current_date))
            current_date += datetime.timedelta(days=self.delta)
            data['to_date'].append(str(current_date))

        print(current_date, self.to_date)

        if current_date + datetime.timedelta(days=self.delta) > self.to_date:
            buf = self.delta
            self.delta = (self.to_date - current_date).days

            news = self.__load_news(current_date)
            for tag in tags:
                data[tag].append(news[tag])
            data['dollar'].append(self.__load_dollar(current_date))
            # data['from_date'].append(str(current_date))
            data['to_date'].append(str(self.to_date))
            self.delta = buf

        return data

    def to_csv(self, filename='dollar_prediction.csv'):
        """
        запускает сбор информации и записывает ее в csv файл
        :param filename: имя csv файла
        :return: True, если запись прошла без ошибок, иначе False
        """
        start = datetime.datetime.now()
        data = self.data_capture()
        print(datetime.datetime.now() - start)
        try:
            with open(filename, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                columns = tags + ['date', 'dollar']
                writer.writerow(tuple(columns))
                for i in range(len(data['dollar'])):
                    l = []
                    for tag in tags:
                        l.append(data[tag][i])
                    l.append(data['to_date'][i])
                    l.append(data['dollar'][i])
                    writer.writerow(tuple(l))
            return True
        except:
            return False


# начальные данные
beg = (2018, 1, 1)
end = (2020, 8, 19)
period = 3
obj = Major(beg, end, period)

if obj.to_csv():
    print('Файл успешно записан')
else:
    print('Произошла ошибка')
