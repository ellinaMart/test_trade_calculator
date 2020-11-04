# test_trade_calculator
#Автоматический тест test_calculator_api генерирует тестовые данные с использованием allpairspy и записывает их в parameters.json. 
#Отправляет get запрос с тестовыми данными и проверяем полученные параметры по формулам.

#Сценарий api теста:
#1. Получаем список инструментов для формы standart и генерируем тестовые данные в файл data/parameters.json
#2. Отправляем запрос на расчет параметров со сгенерированными тестовыми данными
#3. Проверяем параметр margin по формулам

#Сценарий ui теста:
#1. Открываем страницу калькулятора
#2. Выбираем параметры и нажимаем рассчитать
#3. Рассчитываем margin и сравниваем со значением на странице


#перед запуском тестов необходимо установить:
pip install pytest
pip install requests
pip install allpairspy
pip install selenium

#установка и запуск виртуального окружения
virtualenv venv
source venv/bin/activate

#install allure
pip install allure-pytest
#создали папку с отчетом
pytest --alluredir ../reports
#запускаем allure с отчетом в папке reports
allure serve reports
#запуск тестов из папки tests с allure
py.test --alluredir=reports ./tests



