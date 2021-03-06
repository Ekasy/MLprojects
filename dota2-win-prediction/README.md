# Задание

Вам необходимо провести описанные в документе final-statement.html (или final-statement.ipynb) два этапа исследования (для двух подходов к решению задачи), написать по результатам каждого этапа небольшой отчет (ниже указаны вопросы, ответы на которые должны содержаться в отчете), и предоставить для ревью данный отчет и код, с помощью которого вы выполнили задание.

Не забывайте, что в выборке есть признаки, которые "заглядывают в будущее" — они помечены в описании данных как отсутствующие в тестовой выборке. Их прямое использование в модели приведет к переобучению, поэтому не забудьте исключить их из выборки.

---
### Подход 1: градиентный бустинг "в лоб"

Один из самых универсальных алгоритмов, изученных в нашем курсе, является градиентный бустинг. Он не очень требователен к данным, восстанавливает нелинейные зависимости, и хорошо работает на многих наборах данных, что и обуславливает его популярность. В данном разделе предлагается попробовать градиентный бустинг для решения нашей задачи.

**В отчете по данному этапу должны содержаться ответы на следующие вопросы:**

- Какие признаки имеют пропуски среди своих значений (приведите полный список имен этих признаков)? Что могут означать пропуски в этих признаках (ответьте на этот вопрос для двух любых признаков)?
- Как называется столбец, содержащий целевую переменную?
- Как долго проводилась кросс-валидация для градиентного бустинга с 30 деревьями? Инструкцию по измерению времени можно найти выше по тексту. Какое качество при этом получилось?
- Имеет ли смысл использовать больше 30 деревьев в градиентном бустинге? Что можно сделать, чтобы ускорить его обучение при увеличении количества деревьев?
---
### Подход 2: логистическая регрессия

Линейные методы работают гораздо быстрее композиций деревьев, поэтому кажется разумным воспользоваться именно ими для ускорение анализа данных. Одним из наиболее распространенных методов для классификации является логистическая регрессия. В данном разделе предлгается применить ее к данным, а также попробовать различные манипуляции с признаками.

**В отчете по данному этапу должны содержаться ответы на следующие вопросы:**

- Какое качество получилось у логистической регрессии над всеми исходными признаками? Как оно соотносится с качеством градиентного бустинга? Чем можно объяснить эту разницу? Быстрее ли работает логистическая регрессия по сравнению с градиентным бустингом?
- Как влияет на качество логистической регрессии удаление категориальных признаков (укажите новое значение метрики качества)? Чем можно объяснить это изменение?
- Сколько различных идентификаторов героев существует в данной игре?
- Какое получилось качество при добавлении "мешка слов" по героям? Улучшилось ли оно по сравнению с предыдущим вариантом? Чем можно это объяснить?
- Какое минимальное и максимальное значение прогноза на тестовой выборке получилось у лучшего из алгоритмов?

Следует понимать, что конкретные показатели метрик качества могут отличаться в зависимости от конкретных разбиений выборки, значений параметров и версий библиотек. Ответы следует проверять на адекватность — в правильную ли сторону изменяется показатель качества при том или ином изменении модели или выборки, корректные ли выводы делаются из соответствующих результатов.