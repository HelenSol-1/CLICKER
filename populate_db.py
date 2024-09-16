from sqlalchemy.orm import Session
from database import Base, engine, DietType, Product

# Создаем таблицы (если они еще не созданы)
Base.metadata.create_all(engine)

# Создаем сессию для работы с базой данных
with Session(engine) as session:
    # Создаем типы питания
    diet_types = [
        DietType(name='Сбалансированное', protein_percent=0.3, fat_percent=0.3, carbs_percent=0.4),
        DietType(name='Высокобелковое', protein_percent=0.5, fat_percent=0.2, carbs_percent=0.3),
        DietType(name='Низкоуглеводное', protein_percent=0.4, fat_percent=0.4, carbs_percent=0.2),
    ]

    # Добавляем типы питания в сессию
    session.add_all(diet_types)
    session.commit()

    # Создаем продукты
    products = [
        Product(name='Куриная грудка', protein=23.6, fat=1.9, carbs=0.4, calories=113, category='Мясо'),
        Product(name='Яйцо куриное', protein=12.7, fat=10.9, carbs=0.7, calories=157, category='Яйца'),
        Product(name='Овсяная каша', protein=12.3, fat=6.1, carbs=59.5, calories=342, category='Крупы'),
        Product(name='Яблоко', protein=0.4, fat=0.4, carbs=9.8, calories=47, category='Фрукты'),
        Product(name='Брокколи', protein=2.8, fat=0.4, carbs=7.0, calories=34, category='Овощи'),
        # Добавьте другие продукты по необходимости
    ]

    # Добавляем продукты в сессию
    session.add_all(products)
    session.commit()

    # Устанавливаем связи между продуктами и типами питания
    # Пример: Куриная грудка подходит для всех типов питания
    products[0].diets.extend(diet_types)
    # Яйцо куриное подходит для Сбалансированного и Высокобелкового
    products[1].diets.extend([diet_types[0], diet_types[1]])
    # Овсяная каша подходит для Сбалансированного и Высокобелкового
    products[2].diets.extend([diet_types[0], diet_types[1]])
    # Яблоко подходит для всех типов питания
    products[3].diets.extend(diet_types)
    # Брокколи подходит для всех типов питания
    products[4].diets.extend(diet_types)

    # Сохраняем изменения
    session.commit()

print("База данных успешно заполнена начальными данными.")
