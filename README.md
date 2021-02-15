# intermediate-option
Вектора размерностью 35005x1 ресурсоемкие в сравнении, попробую использовать предобученную сетьVGG16 для уменьшения размерности 500x1.  
1. Cоздать массив заполненный 0 размерностью 150552x1
2. Вставить 35005x1 в массив 150552x1
3. Конвертировать в размерность 224x224x3
4. Обработать в VGG, получить 500x1
5. Сравнивать.  
Сделать замеры скорости.

Пример словаря с ID клиентов:  
"группа 1":[ "9834", "23", "23121", ....]  
"группа 2":[ "983", "3"]  

После получения этих групп, мы сможем посмотреть в каждую группу:
- средний чек  
- количество покупок   
- популярный продукт в группе  
- доминирующий продукт
- доминирующий пол
- активность клиента по его полям 'join_club_success', 'Could_send_sms', 'Could_send_email'
С данным вроде все отлично их много :)
Допустим получим 20т групп, мы сможем по очереди анализировать каждую, снизить вычислительную нагрузку - это мое предположение и рассчитываю что оно верное.

##### TODO:
+ исправить медленные куски кода/оптимезировать
+ создать классы/модули
+ структурировать
##### <a name="Parag"></a>	Выводы:
1. Из всего множества пользователей, 4,14% вернулись в 2020 
``` python3 c_diag_user.py ```
![Иллюстрация к проекту](https://github.com/evilsadko/intermediate-option/blob/main/github/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%20%D0%BE%D1%82%202021-02-10%2019-17-02.png)
2. Из 35376 наименований продуктов, продовались 24290 наименования, 31,4% можно снизить на складе или убрать вообще  
![Иллюстрация к проекту](https://github.com/evilsadko/intermediate-option/blob/main/github/Figure_5.png)
3. 59843 покупателя, совершили 82705 покупки, купив 8239567 едениц товара. На диаграмме показаны товары суммарный обьем продажи привышаеющий 0.5%
``` python3 diag_stat_product.py ```
![Иллюстрация к проекту](https://github.com/evilsadko/intermediate-option/blob/main/github/Figure_6.png)
4. Диаграмма отображает процент средней активности пользователей из 4,14% вернувшихся в 2020. Активными считаем тех, кто оставил какие либо данные или вступил в клуб ``` python3 stat_user.py ```
![Иллюстрация к проекту](https://github.com/evilsadko/intermediate-option/blob/main/github/Figure_7.png)
5. Самые активыне, вступили в клуб, оставили номер телефона, электронную почту, из 4,14% вернувшихся в 2020. Основной клиент комапании, для более детальных выводов нужен анализ потраченых средств ``` python3 stat_user_access.py ```
![Иллюстрация к проекту](https://github.com/evilsadko/intermediate-option/blob/main/github/Figure_8.png)
6. Процентное соотношение пола 
``` python3 c_diag_sex.py ```
![Иллюстрация к проекту](https://github.com/evilsadko/intermediate-option/blob/main/github/Figure_9.png)
7. Поиск аномалий в 3D пространстве, Покупатели/Покупки/Продукты
``` diag_3d.py ```
![Иллюстрация к проекту](https://github.com/evilsadko/intermediate-option/blob/main/github/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%20%D0%BE%D1%82%202021-02-10%2023-49-29.png)
![Иллюстрация к проекту](https://github.com/evilsadko/intermediate-option/blob/main/github/%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%20%D0%BE%D1%82%202021-02-10%2023-48-36.png)
8. 82705 покупок, 8239567 продуктов, среднее количество продуктов в покупке 99,6. Диаграмма не однородна, 3 аномалии, количество покупок привышает в 17 раз в сравнении с другими
``` python3 diag_product_line.py ```
![Иллюстрация к проекту](https://github.com/evilsadko/intermediate-option/blob/main/github/Figure_1.png)
``` python3 diag_product_dots.py ```
![Иллюстрация к проекту](https://github.com/evilsadko/intermediate-option/blob/main/github/Figure_4.png)
![Иллюстрация к проекту](https://github.com/evilsadko/intermediate-option/blob/main/github/Figure_3.png)
9. График продажи продуктов за год ``` python3 diag_per_year.py ```
![Иллюстрация к проекту](https://github.com/evilsadko/intermediate-option/blob/main/github/Figure_1_3.png)
10. График продажи продуктов за месяц ``` python3 diag_per_month.py ```
![Иллюстрация к проекту](https://github.com/evilsadko/intermediate-option/blob/main/github/Figure_1_1.png)
11. График покупок за год ``` python3 diag_per_year.py```
![Иллюстрация к проекту](https://github.com/evilsadko/intermediate-option/blob/main/github/Figure_1_2.png)
12. 12 продуктов, чьи продажи больше 0.5 за год, купленные индиф покупателями за 9 дней января ``` diag_stat_product_.py ```
![Иллюстрация к проекту](https://github.com/evilsadko/intermediate-option/blob/main/github/Figure_10.png)
13. График продажи продуктов за день ``` python3 diag_per_day.py ```
![Иллюстрация к проекту](https://github.com/evilsadko/intermediate-option/blob/main/github/Figure_3_1.jpg)
14. График продуктов и покупов в течении 365 дня ``` python3 diag_per_month_1.py ```
![Иллюстрация к проекту](https://github.com/evilsadko/intermediate-option/blob/main/github/Figure_11.png)

https://habr.com/ru/post/196980/  
https://medium.com/@bigdataschool/4-шага-к-моделированию-machine-learning-практические-примеры-на-python-caee5f123873  
https://konstantinklepikov.github.io/2019/10/08/scikit-learn-preprocessing.html  
http://blog.datalytica.ru/2018/04/blog-post.html     
https://habr.com/ru/post/491552/      
https://habr.com/ru/post/202090/  
https://www.kaggle.com/rohitanil/keras-cnn-lstm-lb-0-059  
https://habr.com/ru/post/468295/  
https://coderoad.ru/51088585/Как-мне-получить-получить-значение-ячейки-и-хранить-в-переменной-с-Pandas  
https://towardsdatascience.com/dealing-with-list-values-in-pandas-dataframes-a177e534f173  
https://nagornyy.me/courses/data-science/social-graphs/  
https://wiki.programstore.ru/algoritmy-obxoda-grafov-na-python-i-c/  
https://coderoad.ru/11483863/Python-массив-индексов-пересечения-numpy  
https://blog.skillfactory.ru/nauka-o-dannyh-data-science/graf_ds/  
https://habr.com/ru/company/ruvds/blog/442516/  
https://towardsdatascience.com/dealing-with-list-values-in-pandas-dataframes-a177e534f173  
https://towardsdatascience.com/stacked-bar-charts-with-pythons-matplotlib-f4020e4eb4a7  
https://pyprog.pro/mpl/mpl_axis_ticks.html  
https://overcoder.net/q/1551755/python-numpy-я-уже-написал-самый-быстрый-код-для-большого-массива  
https://prog-cpp.ru/data-graph/  
https://www.python-course.eu/graphs_python.php  
https://pimiento.github.io/python_graphs.html  
https://coderoad.ru/33281957/более-быстрая-альтернатива-numpy-where  
https://jakevdp.github.io/PythonDataScienceHandbook/04.12-three-dimensional-plotting.html  
https://towardsdatascience.com/the-art-of-effective-visualization-of-multi-dimensional-data-6c7202990c57  
https://medium.com/@kvnamipara/a-better-visualisation-of-pie-charts-by-matplotlib-935b7667d77f  
https://medium.com/swlh/python-data-visualization-with-matplotlib-for-absolute-beginner-part-iii-three-dimensional-8284df93dfab  
https://habr.com/ru/company/skillfactory/blog/510320/  
https://medium.com/nuances-of-programming/4-простые-визуализации-данных-в-python-с-помощью-кода-ca58253fa1a3
```
# data.sort_values(by=name_x, ascending=True, inplace=True)
# f_open.pivot_table("id", "finance_count", "shop_count").plot(kind='bar', stacked=True)
# pd.get_dummies(f_open[name])
# (f_open[name]==True).sum() 
# f_open.nunique()
# f_open[name].nunique()
# f_open.columns.tolist()
# f_open.info()
# f_open.describe()
# np.isnan(arr[r,d])
# (p_open[p_open['Product_ID'].duplicated()] # поиск дубликатов
# (p_open[p_open[['Order_ID']].duplicated() == True])
# p_open[p_open['Product_ID'].duplicated(keep=False)] # поиск дубликатов
# df.index.get_duplicates()
# (p_open['Product_ID'].value_counts())
# .sort_values(by=['Product_ID'], inplace=True) ?
``` 


Victor, [12.02.21 11:40]
Из полей которые могут пригодиться, осталось:
Order: price_before_discount, amount charget, order_date
Product: Total_Amount, TotalDiscount

Victor, [12.02.21 11:43]
Customer: есть поля Start_Mem_Data, End_Mem_Data, renew_data, Clubid, consent - пока что не понимаю некоторые

Victor, [12.02.21 11:46]
Start_Mem_Data, End_Mem_Data  - можно анализировать этот промежуток даты, не понимаю практического смысла.

Victor, [12.02.21 11:46]
renew_data, Clubid, consent - как трактовать?

Victor, [12.02.21 11:47]
Полезным кажется:
Order: price_before_discount, amount charget, order_date
Product: Total_Amount, TotalDiscount
Попробую отсортировать во времени, и показать зависимость от разности Total_Amount, TotalDiscount

Victor, [12.02.21 11:48]
Что даст понимание как скидка влияет на покупательскую активность

Victor, [12.02.21 11:49]
Эта скидка накопительная, или преодичная

Victor, [12.02.21 11:52]
постараюсь сегодня сделать график популярности товара исходя из времени

Victor, [15.02.21 13:47]
Предсказание покупательской активности по месяцам, 50/50, все упирается в данные, реальней по дням, данных больше можно обучать сеть.

Victor, [15.02.21 13:50]
Если по месяцам нужны данные за 10 лет, и скорей всего без сложных моделей будет понятно, что продукт с ID .... , будет продавать в определенный месяц, так как средняя продолжительность закупок продуктов 2 месяца, прав? Графики строили видно...

Victor, [15.02.21 13:54]
Может это связано с временем поставок или скидкой. Время поставки продуктов в бд нет, что с скидками посмотрю вечером.

Victor, [15.02.21 13:57]
Глядя на эти данные, у меня появилось мнение что это не супермаркет, а какой то цент оптовой торговли. Нет продажи определенного продукта в течении года, разовые скачи

Victor, [15.02.21 13:57]
Что то появилось, приехали скупили

Victor, [15.02.21 13:57]
Видно резкие пики продаж и потом спад

Victor, [15.02.21 13:58]
длиться такое не больше 3 месяцев

Victor, [15.02.21 13:58]
Если делать выводы на продолжительности, то самый лучший продукт - с высоким пиком и малым периодом продажи

Victor, [15.02.21 13:59]
Но что бы быть уверенным на 100% нужно смотреть на остатки после этого периода

Victor, [15.02.21 13:59]
если разность поступившего товара с оставшимся меньше какого то процента - значит крутой товар

Victor, [15.02.21 14:01]
Надеюсь мои мысли в правильном направлении...

Victor, [15.02.21 14:10]
Эта задача data analyst, что бы это было ML - скорей всего нужно больше пространственных признаков: рост, вес, возраст, фотография. Сейчас мы поэтапно разберем всю бд и сделаем вывод. Для автоматизации этого процесса, нужно перенести этот опыт и шаги действий на другие данные, и так раз 10-20, что бы собрать свои данные. Скорей всего(уверенность на 86%) не одна из обученных сетей GPT3, BERT не подойдет к этим задачам, вы абсолютно правы - это маркетинг и обещать можно много, и прав я, реализуется это не быстро :(
Аналогия с google translate, существует давно, но использовать ML начала недавно, до этого сидели в индии работники и переводили за 0.6$ в час

Victor, [15.02.21 14:13]
gpt-3, bert - справятся с такими запросами - "что мне делать если" - и тут правильно ставить исходя из наших данных

Victor, [15.02.21 14:14]
Если обучить на своих данных, мы сможем вводить статистику и ждать рекомендация

Victor, [15.02.21 14:15]
https://medium.com/@willwestinvest/getting-investment-advice-from-gpt-3-at-the-aidungeon-d4cdfd0fcbe8

Victor, [15.02.21 14:15]
Тут про торговлю на бирже

Victor, [15.02.21 14:15]
Но применимо и к нам

Victor, [15.02.21 14:20]
https://clockwise.software/blog/how-to-integrate-gpt3/

Victor, [15.02.21 14:20]
Еще одна статья

Victor, [15.02.21 14:21]
Советы она может давать, но точность ее советов под вопросом.
