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
10. График продажи продуктов за день ``` python3 diag_per_day.py ```
![Иллюстрация к проекту]()

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
