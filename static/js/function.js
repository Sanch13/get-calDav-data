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
    const optionsDay = {weekday: "long"};
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

function createFirstCardDiv(events) {
    const firstCardDiv = document.createElement('div');
    firstCardDiv.innerHTML = `
            <div class="card">
                <div class="card_current_time ${events[0].status === 'free' ? 'green_status' : 'red_status'}" id="card_current_time">
                    <p>СЕЙЧАС</p>
                </div>
            </div>
        `
    return firstCardDiv
}

function createOtherCardDiv(event) {
    const cardDiv = document.createElement('div');
    cardDiv.classList.add('card');

    // Создаем HTML внутри карточки
            cardDiv.innerHTML = `
                <div class="card_main">
                    <div class="card__time">
                        ${new Date(event.start).toLocaleTimeString([], {
                hour: '2-digit',
                minute: '2-digit'
            })} -
                        ${new Date(event.end).toLocaleTimeString([], {
                hour: '2-digit',
                minute: '2-digit'
            })}
                    </div>
                    <div class="card__description">
                        ${event.summary}
                    </div>
                </div>
                <div class="card__color" style="background-color: ${event.status === 'free' ? 'green' : 'red'};"></div>
            `;

    return cardDiv
}

function reloadPageOnMinuteSync() {
    const now = new Date();
    const secondsToNextMinute = 60 - now.getSeconds();

    // Таймер до следующей минуты
    setTimeout(() => {
        location.reload();  // Перезагрузка страницы
    }, secondsToNextMinute * 1000);
}


function equalsTime(events) {
    if (events.length === 1) {
        return events
    }
    const nowTime = new Date().getTime();
    const firstEventEndTime = new Date(events[0].end).getTime();
    console.log("Now time", nowTime);
    console.log("FIRST time END", firstEventEndTime);

    if (nowTime >= firstEventEndTime && events[0].status === "reserved" ) {
        return events.slice(1)
    } else {
        return events
    }
}