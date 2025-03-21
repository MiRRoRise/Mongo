from pymongo import MongoClient, errors


"""
Для подключения к MongoDB и работы с базой данных для языка python была создана 
библиотека pymongo. Продемонстрируем принцип работы и способы исполнения
классических запросов 
"""

client = None
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['laba']
    collection = db['prescriptions']

    # 1. Создание и заполнение коллекции
    collection.drop()
    prescriptions = [
        {"_id": 43001, "date": "Понедельник", "patient_id": 1, "doctor_id": 1, "procedure_id": 1, "quantity": 1, "payment": 5000, "payout": 350},
        {"_id": 43002, "date": "Вторник", "patient_id": 2, "doctor_id": 2, "procedure_id": 2, "quantity": 1, "payment": 10000, "payout": 800}
    ]
    collection.insert_many(prescriptions)

    # 2. Вывод содержимого
    print("\nВывод:", list(collection.find()))

    # 3. Обновление документа
    result = collection.update_one({"payment": {"$gt": 6000}}, {"$set": {"payment": 12000, "payout": 960}})
    if result.modified_count > 0:
        print("\nДокументы обновлены")
    else:
        print("\nДокументы для обновления не найдены")
    print("После обновления:", list(collection.find()))

    # 4. Удаление документа
    delete_result = collection.delete_one({"date": "Понедельник"})
    if delete_result.deleted_count > 0:
        print("\nДокумент удален")
    else:
        print("\nДокумент для удаления не найден")
    print("После удаления:", list(collection.find()))

    # 5. Очистка коллекции
    collection.delete_many({})
    print("\nПосле очистки:", list(collection.find()))

except errors.ServerSelectionTimeoutError:
    print("Ошибка подключения к серверу MongoDB")
except errors.PyMongoError as e:
    print(f"Ошибка при работе с MongoDB: {e}")
except Exception as e:
    print(f"Ошибка: {e}")
finally:
    if client:
        client.close()
