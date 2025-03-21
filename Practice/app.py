from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

def connect_to_db():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["hospital"]
        return db["patients"], client
    except ConnectionFailure as e:
        raise Exception(f"Ошибка подключения к MongoDB: {e}")

def insert_patients(collection, patients_data):
    try:
        collection.insert_many(patients_data)
    except OperationFailure as e:
        raise Exception(f"Ошибка при вставке данных: {e}")

def print_collection(collection):
    try:
        for patient in collection.find():
            print(patient)
    except OperationFailure as e:
        raise Exception(f"Ошибка при чтении данных: {e}")

def update_patient_discount(collection, patient_id, new_discount):
    try:
        collection.update_one({"ID": patient_id}, {"$set": {"Discount": new_discount}})
    except OperationFailure as e:
        raise Exception(f"Ошибка при обновлении данных: {e}")

def delete_patient(collection, patient_id):
    try:
        collection.delete_one({"ID": patient_id})
    except OperationFailure as e:
        raise Exception(f"Ошибка при удалении пациента: {e}")

def clear_collection(collection):
    try:
        collection.delete_many({})
    except OperationFailure as e:
        raise Exception(f"Ошибка при очистке коллекции: {e}")

def main():
    patients = [
        {"ID": 1, "Surname": "Мишин", "Department": "Кардиология", "Discount": 50},
        {"ID": 2, "Surname": "Сивогривов", "Department": "Офтальмология", "Discount": 0},
        {"ID": 3, "Surname": "Пивень", "Department": "Неврология", "Discount": 50},
        {"ID": 4, "Surname": "Макеев", "Department": "Кардиология", "Discount": 0},
        {"ID": 5, "Surname": "Синицын", "Department": "Терапевтия", "Discount": 50},
    ]

    try:
        collection, client = connect_to_db()

        insert_patients(collection, patients)
        print("Содержимое коллекции:")
        print_collection(collection)

        update_patient_discount(collection, 3, 30)
        print("\nПосле обновления:")
        print_collection(collection)

        delete_patient(collection, 4)
        print("\nПосле удаления:")
        print_collection(collection)

        clear_collection(collection)
        print("\nПосле очистки:")
        print_collection(collection)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()