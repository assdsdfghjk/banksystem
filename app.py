{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "31eb6801-f7c8-4f21-b725-5299ab17275b",
   "metadata": {},
   "outputs": [
    {
     "ename": "ModuleNotFoundError",
     "evalue": "No module named 'flask_cors'",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[1], line 2\u001b[0m\n\u001b[0;32m      1\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m \u001b[38;5;21;01mflask\u001b[39;00m \u001b[38;5;28;01mimport\u001b[39;00m Flask, request, jsonify\n\u001b[1;32m----> 2\u001b[0m \u001b[38;5;28;01mfrom\u001b[39;00m \u001b[38;5;21;01mflask_cors\u001b[39;00m \u001b[38;5;28;01mimport\u001b[39;00m CORS\n\u001b[0;32m      3\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m \u001b[38;5;21;01mjwt\u001b[39;00m\n\u001b[0;32m      4\u001b[0m \u001b[38;5;28;01mimport\u001b[39;00m \u001b[38;5;21;01mdatetime\u001b[39;00m\n",
      "\u001b[1;31mModuleNotFoundError\u001b[0m: No module named 'flask_cors'"
     ]
    }
   ],
   "source": [
    "from flask import Flask, request, jsonify\n",
    "from flask_cors import CORS\n",
    "import jwt\n",
    "import datetime\n",
    "\n",
    "app = Flask(__name__)\n",
    "CORS(app)  # Разрешаем запросы с фронта\n",
    "app.config[\"SECRET_KEY\"] = \"mysecret\"\n",
    "\n",
    "# Фейковая база данных\n",
    "users = {}\n",
    "\n",
    "# Регистрация пользователя\n",
    "@app.route(\"/register\", methods=[\"POST\"])\n",
    "def register():\n",
    "    data = request.json\n",
    "    username = data[\"username\"]\n",
    "    password = data[\"password\"]\n",
    "\n",
    "    if username in users:\n",
    "        return \"Пользователь уже существует!\", 400\n",
    "\n",
    "    users[username] = {\"password\": password, \"balance\": 100.0}\n",
    "    return \"Регистрация успешна!\", 201\n",
    "\n",
    "# Вход в систему (создание токена)\n",
    "@app.route(\"/login\", methods=[\"POST\"])\n",
    "def login():\n",
    "    data = request.json\n",
    "    username = data[\"username\"]\n",
    "    password = data[\"password\"]\n",
    "\n",
    "    if username not in users or users[username][\"password\"] != password:\n",
    "        return jsonify({\"message\": \"Неверные данные\"}), 401\n",
    "\n",
    "    token = jwt.encode({\"username\": username, \"exp\": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},\n",
    "                       app.config[\"SECRET_KEY\"], algorithm=\"HS256\")\n",
    "    return jsonify({\"token\": token})\n",
    "\n",
    "# Проверка баланса (нужен токен)\n",
    "@app.route(\"/balance\", methods=[\"GET\"])\n",
    "def check_balance():\n",
    "    token = request.headers.get(\"Authorization\")\n",
    "\n",
    "    if not token:\n",
    "        return jsonify({\"message\": \"Требуется токен\"}), 401\n",
    "\n",
    "    try:\n",
    "        token = token.split()[1]  # Берем токен после \"Bearer \"\n",
    "        data = jwt.decode(token, app.config[\"SECRET_KEY\"], algorithms=[\"HS256\"])\n",
    "        username = data[\"username\"]\n",
    "        return jsonify({\"balance\": users[username][\"balance\"]})\n",
    "    except jwt.ExpiredSignatureError:\n",
    "        return jsonify({\"message\": \"Срок действия токена истек\"}), 401\n",
    "    except jwt.InvalidTokenError:\n",
    "        return jsonify({\"message\": \"Недействительный токен\"}), 401\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    app.run(debug=True)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "967cfbc6-ed6d-4dd9-ba19-c3acb9202a54",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
