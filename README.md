# test_trade_calculator
#Автоматический тест test_calculator генерирует тестовые данные с использованием allpairspy и записывает их в parameters.json. 
#Отправляет get запрос с тестовыми данными и проверяем полученные параметры по формулам.

#перед запуском тестов необходимо установить:
pip install pytest
pip install requests
pip install allpairspy

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



