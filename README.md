# API-for-task-management
Функциональность:

Создание задачи: Пользователь может отправить POST-запрос для создания новой задачи. Запрос должен содержать данные о задаче, такие как название и описание.
Получение списка задач: Пользователь может отправить GET-запрос для получения списка всех задач.
Получение одной задачи: Пользователь может отправить GET-запрос с идентификатором задачи для получения подробной информации о конкретной задаче.
Обновление задачи: Пользователь может отправить PUT-запрос с идентификатором задачи для обновления ее данных.
Удаление задачи: Пользователь может отправить DELETE-запрос с идентификатором задачи для удаления ее из списка.

Генерация ключей:
openssl genrsa -out jwt-private.pem 2048
openssl rsa -in jwt-private.pem -outform pem -pubout -out jwt-public.pem