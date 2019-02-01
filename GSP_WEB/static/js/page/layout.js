function formatDate(date) {
    date = date.replace(" GMT", "");
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear(),
        hour = d.getHours(),
        minute = d.getMinutes(),
        second = d.getSeconds();

        hour = ("0" + hour).slice(-2);
        minutes = ("0" + minutes).slice(-2);
        seconds = ("0" + seconds).slice(-2);

    if(year == null || isNaN(year))
        return '-';

    if (month.length < 2) month = '0' + month;
    if (day.length < 2) day = '0' + day;

    var results = [year, month, day].join('-') + " " + [hour, minute, second].join(':');

    return results;
}

