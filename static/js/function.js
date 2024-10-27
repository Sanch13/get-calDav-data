"use strict";

function updateMoscowTime() {
    // Создаем объект даты и времени для текущего момента
    const date = new Date();

    // Определяем московское время (UTC +3)
    const moscowOffset = 3 * 60; // 3 часа в минутах
    const localOffset = date.getTimezoneOffset(); // Локальное смещение от UTC в минутах
    const moscowTime = new Date(
        date.getTime() + (moscowOffset + localOffset) * 60000
    );

    // Форматируем время в строку "ЧЧ:ММ:СС"
    const hours = moscowTime.getHours().toString().padStart(2, "0");
    const minutes = moscowTime
        .getMinutes()
        .toString()
        .padStart(2, "0");
    // const seconds = moscowTime
    // 	.getSeconds()
    // 	.toString()
    // 	.padStart(2, "0");

    // Обновляем содержимое элемента
    document.getElementById(
        "moscowTime"
    ).textContent = `${hours}:${minutes}`;
}

function updateDateTime() {
    const optionsDate = {
        day: "numeric",
        month: "long",
        year: "numeric",
    };
    const optionsDay = { weekday: "long" };
    const now = new Date();

    // Форматирование даты и дня недели
    const currentDate = now.toLocaleDateString(
        "ru-RU",
        optionsDate
    );
    const currentDay = now.toLocaleDateString("ru-RU", optionsDay);

    document.getElementById("currentDate").textContent =
        currentDate;
    document.getElementById("currentDay").textContent = currentDay;
}