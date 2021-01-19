var countDownDate = new Date('Jan 24, 2021 00:00:00').getTime();

function validate() {
    let validated = document.getElementById('nickname').value.length >= 3 && document.getElementById('fullname').value.length >= 6 && document.getElementById('email').value.length >= 6 && document.getElementById('phone').value.length >= 10 && document.getElementById('class').value.length > 1 && document.getElementById('school').value != '0' && document.getElementById('fullname').value.trim().indexOf(' ') >= 0;
    document.getElementById('apply').disabled = !validated && (countDownDate - (new Date).getTime()) > 0;
}

function getCase(days) {
    let day = 'дней';
    switch (days) {
        case 1:
        case 21:
        case 31:
            day = 'день';
            break;
        case 2:
        case 3:
        case 4:
        case 22:
        case 23:
        case 24:
            day = 'дня';
            break;
    }
    return day;
}

function update() {
    var e = (new Date).getTime(),
        t = countDownDate - e,
        n = Math.floor(t / 86400000),
        o = Math.floor(t % 86400000 / 3600000),
        a = Math.floor(t % 3600000 / 60000),
        r = Math.floor(t % 60000 / 1000);
    document.getElementById('timer').innerHTML = (n >= 10 ? n : '0' + n) + ' ' + getCase(n) + ' ' + (o >= 10 ? o : '0' + o) + ' : ' + (a >= 10 ? a : '0' + a) + ' : ' + (r >= 10 ? r : '0' + r);
    if (t < 0) {
        document.getElementById('timer').innerHTML = '0 дней 00 : 00 : 00';
        document.getElementById('apply').disabled = true;
    }
}

function submit() {
    document.getElementById('apply').disabled = true;
    document.getElementById('apply').innerHTML = 'Отправляем заявку...';
    $.post('https://kaletise.me/submit', {email: document.getElementById('email').value, phone: document.getElementById('phone').value, nickname: document.getElementById('nickname').value, class: document.getElementById('class').value, fullname: document.getElementById('fullname').value, school: document.getElementById('school').value}).done(function(response) {
        var data = JSON.parse(response);
        document.getElementById('window-apply').style.display = 'none';
        if (data.status == 1) {
            document.getElementById('window-success').style.display = 'block';
        } else if (data.status == 2) {
            document.getElementById('window-fail-exists').style.display = 'block';
        } else {
            document.getElementById('window-fail').style.display = 'block';
        }
    }).fail(function(xhr, status, error) {
        document.getElementById('window-apply').style.display = 'none';
        document.getElementById('window-fail').style.display = 'block';
    });
}

update(), setInterval(function() {
    update()
}, 1000);