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
                        ${new Date(event.start).toLocaleTimeString("ru-ru", {
                hour: '2-digit',
                minute: '2-digit'
            })} -
                        ${new Date(event.end).toLocaleTimeString("ru-ru", {
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

function reloadPageOnHourSync() {
    const now = new Date();
    const minutesToNextHour = 60 - now.getMinutes();
    const secondsToNextHour = (minutesToNextHour * 60) - now.getSeconds();

    // Таймер до начала следующего часа
    setTimeout(() => {
        location.reload();  // Перезагрузка страницы
    }, secondsToNextHour * 1000);
}

function equalsTime(events) {
    if (events.length === 1) {
        return events
    }
    const nowTime = new Date().getTime();
    const firstEventEndTime = new Date(events[0].end).getTime();
    // console.log("Now time", nowTime);
    // console.log("FIRST time END", firstEventEndTime);

    if (nowTime >= firstEventEndTime && events[0].status === "reserved" ) {
        return events.slice(1)
    } else {
        return events
    }
}

function showDiffTime(endTimeEvent) {
    const now = new Date();
    const endTime = new Date(endTimeEvent.end);
    let diffMs = endTime - now;

    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffMinutes = Math.ceil((diffMs % (1000 * 60 * 60)) / (1000 * 60));

    // Форматируем часы и минуты, добавляя нули перед одиночными числами
    const formattedHours = String(diffHours).padStart(2, '0');
    const formattedMinutes = String(diffMinutes).padStart(2, '0');

    return `${formattedHours}:${formattedMinutes}`;
}

function fetchDataFirstRoom() {
    return fetch("/api/v1/first/events")
        .then(response => {
            if (!response.ok) {
                return response.json().then(errData => {
                    throw new Error(errData.error || "Ошибка сети");
                });
            }
            return response.json();
        })
        .then(data => {
            updateUI(data);
            return data;
        })
        .catch(error => {
            showErrorMessage(error.message);
        });
}

function updateUI(data) {
    // Обновляем элементы страницы данными из data
    const events = JSON.parse(data.data_json);
    const eventsContainer = document.getElementById("events-container");
    const mainEvents = equalsTime(events);
    const currentEvent = mainEvents[0];

    const main_window = document.getElementById("main-left");
    const main_title = document.getElementById("main__title");
    const main_status = document.getElementById("main__status");
    const main_time = document.getElementById("main__time");
    const main_timer = document.getElementById("main__timer__text");
    const main_timer__off = document.getElementById("timer__off");

    console.log("API updateUI", mainEvents.length, mainEvents);

    eventsContainer.textContent = "";
    main_window.classList.remove("main-left-bg-free", "main-left-bg-reserved");

    main_window.classList.add(`${currentEvent.status === 'free' ? 'main-left-bg-free' : 'main-left-bg-reserved'}`);
    main_title.textContent = "Переговорная 1 этаж";
    main_status.textContent = `${currentEvent.summary}`;
    main_time.textContent = `
        ${new Date().toLocaleTimeString('ru-ru', {hour: '2-digit', minute: '2-digit'})} -
        ${new Date(currentEvent.end).toLocaleTimeString('ru-ru', {hour: '2-digit', minute:
            '2-digit'})}
    `;
    main_timer.textContent = `
         ${currentEvent.status === "reserved" ? 'Освободится через :' : ''}
    `;
    main_timer__off.textContent = currentEvent.status === "reserved" ? showDiffTime(currentEvent) : '';

    if (mainEvents.length === 1) {
        console.log("API ONLY ONE ITEM");
        eventsContainer.appendChild(createFirstCardDiv(mainEvents));
    } else {
        console.log("API MANY ITEMS");
        eventsContainer.appendChild(createFirstCardDiv(mainEvents));

        mainEvents.slice(1).forEach(event => {
            const card = createOtherCardDiv(event);
            eventsContainer.appendChild(card);
        });
    }
}

function fetchDataEveryMinute() {
    const now = new Date();
    const secondsToNextMinute = 60 - now.getSeconds();

    setTimeout(() => {
        fetchDataFirstRoom().then(() => {
            updateMoscowTime(); // обновление каждые 60 секунд
            updateDateTime(); // обновление каждые 60 секунд
        });

        // Затем продолжаем обновлять каждую минуту
        setInterval(fetchDataFirstRoom, 60000); // обновление каждые 60 секунд
        setInterval(updateMoscowTime, 60000); // обновление каждые 60 секунд
        setInterval(updateDateTime, 60000); // обновление каждые 60 секунд
    }, secondsToNextMinute * 1000);
}

function showErrorMessage(error) {
    updateMoscowTime()
    updateDateTime()
    const eventsContainer = document.getElementById("events-container");
    eventsContainer.textContent = '';

    const main_window = document.getElementById("main-left");
    const main_title = document.getElementById("main__title");
    const main_status = document.getElementById("main__status");
    const main_time = document.getElementById("main__time");
    const main_timer = document.getElementById("main__timer__text");
    const main_timer__off = document.getElementById("timer__off");
    main_window.classList.remove("main-left-bg-free", "main-left-bg-reserved");
    main_status.textContent = "";
    main_time.textContent = "";
    main_timer.textContent = "";
    main_timer__off.textContent = "";
    console.log(error, error.message, error.error);
    main_title.textContent = `Не удалось загрузить данные:  ${error}`;
}
