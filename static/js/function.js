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
    if (cardDiv) {
        console.log(`Есть cardDiv: ${cardDiv}`);
    }
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
            <div class="card__description ${event.summary.length < 25 ? 'one_line' : 'two_line'}">
                ${event.summary}
            </div>
        </div>
        <div class="card__color" style="background-color: ${event.status === 'free' ? 'green' : 'red'};"></div>
    `;

    return cardDiv
}

function equalsTime(events) {
    if (events.length === 1) {
        return events
    }
    const nowTime = new Date().getTime();
    const firstEventEndTime = new Date(events[0].end).getTime();

    if (nowTime >= firstEventEndTime && events[0].status === "reserved") {
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
    const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diffMs % (1000 * 60)) / 1000);

    // Форматируем часы и минуты, добавляя нули перед одиночными числами
    const formattedHours = String(diffHours).padStart(2, '0');
    const formattedMinutes = String(diffMinutes).padStart(2, '0');
    const formattedSeconds = String(seconds).padStart(2, "0");
    const timerOff = `${formattedHours}:${formattedMinutes}:${formattedSeconds}`;

    // main_timer__off.textContent = timerOff;
    // return `${formattedHours}:${formattedMinutes}`;
    return timerOff
}

function fetchRatesToday() {
    return fetch("/api/v1/rates/")
        .then(response => {
            if (!response.ok) {
                return response.json().then(errData => {
                    throw new Error(errData.error || "Ошибка сети");
                });
            }
            return response.json();
        })
        .then(data => {
            showRatesToday(data);
            return data;
        })
        .catch(error => {
            // showErrorMessage(error.message);
        });
}

function fetchDataWeatherToday() {
    return fetch("/api/v1/weather/")
        .then(response => {
            if (!response.ok) {
                return response.json().then(errData => {
                    throw new Error(errData.error || "Ошибка сети");
                });
            }
            return response.json();
        })
        .then(data => {
            showDataWeatherToday(data);
            return data;
        })
        .catch(error => {
            // showErrorMessage(error.message);
        });
}

function showDataWeatherToday(data) {
    const createImgElement = `
        <img src="${data.icon}"
             alt=""
             class="footer__img"
        >
        <div class="footer__weather" id="footer_weather">${data.tempC > 0 ? '+' + data.tempC : data.tempC}</div>
    `;

    const footer_weather_block = document.getElementById("footer_weather_block");
    footer_weather_block.innerHTML = createImgElement;
}

function showRatesToday(data) {
    const usd = document.getElementById("footer_usd");
    const euro = document.getElementById("footer_euro");
    const rub = document.getElementById("footer_rub");
    const yuan = document.getElementById("footer_yuan");

    if (usd) usd.textContent = data.USD || "N/A";
    if (euro) euro.textContent = data.EUR || "N/A";
    if (rub) rub.textContent = data.RUB || "N/A";
    if (yuan) yuan.textContent = data.CNY || "N/A";
}

function fetchDataFirstRoom() {
    const url = `/api/v1/first/events/?timestamp=${Date.now()}`;
    return fetch(url, {
        method: "GET",
        headers: {
            "Cache-Control": "no-cache",
            "Pragma": "no-cache"
        }
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errData => {
                    throw new Error(errData.error || "Ошибка сети");
                });
            }
            return response.json();
        })
        .then(data => {
            // console.log(getLocalTime(), data);
            updateUI(data);
            return data;
        })
        .catch(error => {
            showErrorMessage(error.message);
        });
}

function fetchDataSecondRoom() {
    const url = `/api/v1/second/events/?timestamp=${Date.now()}`;
    return fetch(url, {
        method: "GET",
        headers: {
            "Cache-Control": "no-cache",
            "Pragma": "no-cache"
        }
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errData => {
                    throw new Error(errData.error || "Ошибка сети");
                });
            }
            return response.json();
        })
        .then(data => {
            // console.log(getLocalTime(), data);
            updateUI(data);
            return data;
        })
        .catch(error => {
            showErrorMessage(error.message);
        });
}

function fetchDataThirdRoom() {
    const url = `/api/v1/third/events/?timestamp=${Date.now()}`;
    return fetch(url, {
        method: "GET",
        headers: {
            "Cache-Control": "no-cache",
            "Pragma": "no-cache"
        }
    })
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

function fetchDataClassRoom() {
    const url = `/api/v1/class-room/events/?timestamp=${Date.now()}`;
    return fetch(url, {
        method: "GET",
        headers: {
            "Cache-Control": "no-cache",
            "Pragma": "no-cache"
        }
    })
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

    const main_window_left = document.getElementById("main-left");
    const main_title = document.getElementById("main__title");
    const main_time = document.getElementById("main__time");
    const main_timer = document.getElementById("main__timer__text");
    const main_timer__off = document.getElementById("timer__off");

    const main__organizer = document.getElementById("main__organizer");
    const main__summary = document.getElementById("main__summary");

    eventsContainer.textContent = "";
    main_window_left.classList.remove("main-left-bg-free", "main-left-bg-reserved");
    main_title.textContent = data.main__title;

    main_window_left.classList.add(`${currentEvent.status === 'free' ? 'main-left-bg-free' : 'main-left-bg-reserved'}`);
    main__summary.classList.remove('main__summary_free', 'main_one_line', 'main_two_line');

    if (currentEvent.organizer !== null) {
        main__organizer.textContent = "Организатор: " + currentEvent.organizer;
        main__summary.textContent = `${currentEvent.summary.length >= 100 ? cutText(currentEvent.summary) : currentEvent.summary}`;
        main__summary.classList.add(`${currentEvent.summary.length >= 29 ? 'main_two_line' : 'main_one_line'}`);
    } else {
        main__organizer.textContent = '';
        main__summary.textContent = currentEvent.summary;
        main__summary.classList.add('main__summary_free');
    }

    main_time.textContent = `
        ${new Date().toLocaleTimeString('ru-ru', {hour: '2-digit', minute: '2-digit'})} -
        ${new Date(currentEvent.end).toLocaleTimeString('ru-ru', {
        hour: '2-digit', minute:
            '2-digit'
    })}
    `;

    // main_timer.textContent = `
    //      ${currentEvent.status === "reserved" ? 'Освободится через :' : ''}
    // `;

    if (currentEvent.status === "reserved") {
        // console.log("---", timerInterval, new Date().toLocaleTimeString());
        if (timerInterval) {
            // console.log("delete", timerInterval);
            clearInterval(timerInterval);
            // console.log("deleted", timerInterval || '');
            timerInterval = null;
            // console.log("сейчас", timerInterval);
        }

        timerInterval = setInterval(() => {
            const timeLeft = showDiffTime(currentEvent);
            main_timer.textContent = 'Освободится через :';
            main_timer__off.textContent = timeLeft;
            // Останавливаем таймер, если время истекло
            if (timeLeft === '00:00:00') {
                clearInterval(timerInterval);
                timerInterval = null;
            }
        }, 1000);
        // console.log("Инициализация", timerInterval, new Date().toLocaleTimeString());

    } else {
        main_timer.textContent = '';
        main_timer__off.textContent = "";
        if (timerInterval) {
            clearInterval(timerInterval);
            timerInterval = null;
        }
    }
    // console.log("---", timerInterval, new Date().toLocaleTimeString());


    // if (currentEvent.status === "reserved") {
    //     // console.log(typeof currentEvent.start, currentEvent.start, typeof currentEvent.end, currentEvent.end);
    //     // console.log(typeof previousStart, previousStart, typeof previousEnd, previousStart);
    //     console.log("---previousStart---", previousStart, "---previousEnd---", previousEnd);
    //     console.log("---TIME EQUALS---", previousStart === currentEvent.start, previousEnd === currentEvent.end);
    //     if (currentEvent.start !== previousStart || currentEvent.end !== previousEnd) {
    //         // Сохраняем новые значения времени
    //         previousStart = currentEvent.start;
    //         previousEnd = currentEvent.end;
    //         // Очищаем старый интервал, если он существует
    //         console.log("---timerInterval---",timerInterval);
    //         if (timerInterval) {
    //             console.log("---DELETE timerInterval---",timerInterval);
    //             clearInterval(timerInterval);
    //             console.log("---timerInterval---",timerInterval);
    //             timerInterval = null;
    //             console.log("---timerInterval---",timerInterval);
    //         }
    //     }
    //
    //
    //     timerInterval = setInterval(() => {
    //         const timeLeft = showDiffTime(currentEvent);
    //         main_timer.textContent = 'Освободится через :';
    //         main_timer__off.textContent = timeLeft;
    //         // Останавливаем таймер, если время истекло
    //         if (timeLeft === '00:00:00') {
    //             clearInterval(timerInterval);
    //             timerInterval = null;
    //         }
    //     }, 1000);
    //
    //
    // } else {
    //     main_timer.textContent = '';
    //     main_timer__off.textContent = "";
    // }

    // main_timer__off.textContent = currentEvent.status === "reserved" ? timeLeft : '';
    // main_timer__off.textContent = currentEvent.status === "reserved" ? showDiffTime(currentEvent) : '';

    if (mainEvents.length === 1) {
        eventsContainer.appendChild(createFirstCardDiv(mainEvents));
    } else {
        eventsContainer.appendChild(createFirstCardDiv(mainEvents));

        mainEvents.slice(1).forEach(event => {
            const card = createOtherCardDiv(event);
            eventsContainer.appendChild(card);
        });
    }
}

function getLocalTime() {
    const date = new Date();
    const moscowOffset = 3 * 60; // 3 часа в минутах
    const localOffset = date.getTimezoneOffset(); // Локальное смещение от UTC в минутах
    const moscowTime = new Date(
        date.getTime() + (moscowOffset + localOffset) * 60000
    );

    const day = moscowTime.getDate().toString().padStart(2, "0");
    const month = (moscowTime.getMonth() + 1).toString().padStart(2, "0"); // Месяцы начинаются с 0, поэтому прибавляем 1
    const year = moscowTime.getFullYear();

    const hours = moscowTime.getHours().toString().padStart(2, "0");
    const minutes = moscowTime.getMinutes().toString().padStart(2, "0");
    const seconds = moscowTime.getSeconds().toString().padStart(2, "0");

    return `${day}.${month}.${year} ${hours}:${minutes}:${seconds}`;
}

function updateDataClassRoom() {
    let now = new Date();
    let msUntilNextMinute = ((60 - now.getSeconds()) * 1000);

    setTimeout(function () {
        fetchDataClassRoom();
        updateMoscowTime();
        updateDateTime();
        updateDataClassRoom();
    }, msUntilNextMinute);
}

function updateDataThirdRoom() {
    let now = new Date();
    let msUntilNextMinute = ((60 - now.getSeconds()) * 1000);

    setTimeout(function () {
        fetchDataThirdRoom();
        updateMoscowTime();
        updateDateTime();
        updateDataThirdRoom();
    }, msUntilNextMinute);
}

function updateDataSecondRoom() {
    let now = new Date();
    let msUntilNextMinute = ((60 - now.getSeconds()) * 1000);

    setTimeout(function () {
        fetchDataSecondRoom();
        updateMoscowTime();
        updateDateTime();
        updateDataSecondRoom();
    }, msUntilNextMinute);
}

function updateDataFirstRoom() {
    let now = new Date();
    let msUntilNextMinute = ((60 - now.getSeconds()) * 1000);

    setTimeout(function () {
        fetchDataFirstRoom();
        updateMoscowTime();
        updateDateTime();
        updateDataFirstRoom();
    }, msUntilNextMinute);
}

function fetchFirstEventsEveryMinute() {
    const now = new Date();
    const secondsToNextMinute = 60 - now.getSeconds();

    setTimeout(() => {
        setInterval(() => {
            fetchDataFirstRoom()
                .then(() => {
                    updateMoscowTime();
                    updateDateTime();
                });
        }, 60000); // Интервал в 60 секунд
    }, secondsToNextMinute * 1000); // Задержка до начала следующей минуты
}

function fetchThirdEventsEveryMinute() {
    const now = new Date();
    const secondsToNextMinute = 60 - now.getSeconds();

    setTimeout(() => {
        setInterval(() => {
            fetchDataThirdRoom()
                .then(() => {
                    updateMoscowTime();
                    updateDateTime();
                });
        }, 60000); // Интервал в 60 секунд
    }, secondsToNextMinute * 1000); // Задержка до начала следующей минуты
}

function showErrorMessage(error) {
    updateMoscowTime()
    updateDateTime()
    const eventsContainer = document.getElementById("events-container");
    eventsContainer.textContent = '';

    const main_window_left = document.getElementById("main-left");
    const main_title = document.getElementById("main__title");
    const main_time = document.getElementById("main__time");
    const main_timer = document.getElementById("main__timer__text");
    const main_timer__off = document.getElementById("timer__off");

    const main__organizer = document.getElementById("main__organizer");
    const main__summary = document.getElementById("main__summary");

    main_window_left.classList.remove("main-left-bg-free", "main-left-bg-reserved");
    main_time.textContent = "";
    main_timer.textContent = "";
    main_timer__off.textContent = "";

    main__organizer.textContent = "";
    main__summary.textContent = "";

    console.log(error);
    main_title.textContent = `Не удалось загрузить данные:  ${error}`;
}

function cutText(txt) {
    return txt.slice(0, 90) + "...";
}

function timeUntilMidnight() {
    const now = new Date();
    const midnight = new Date();
    midnight.setHours(24, 0, 0, 0); // Устанавливаем полночь на следующий день
    return midnight - now; // Возвращаем разницу в миллисекундах
}

