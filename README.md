# intermediate-option
Так как у нас будет большие вектора 35005x1 и это может занять много времени, попробую использовать предобученную сетьVGG16, из за того что она работает с изображениями, буду создавать массив заполненный 0 размерностью 150 552x1, в него положу наш 35005x1, затем конвертирую в размерность 224x224x3, отправлю в VGG что бы получить 500x1 и уже буду сравнивать. Проверю что будет быстрей...
После сделаю словарь с ID клиентами, пример:
"группа 1":[ "9834", "23", "23121", ....]
"группа 2":[ "983", "3"]
После получения этих групп, мы сможем посмотреть в каждую группу и посмотреть:
средний чек, количество покупок, популярный продукт в группе, какой пол доминирует
