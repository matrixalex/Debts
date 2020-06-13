function get_django_date(datetime) {
    let date = datetime.split('T')[0].split('-');
    let year = parseInt(date[0]);
    let month = parseInt(date[1]);
    let day = parseInt(date[2]);
    date = new Date(year, month - 1, day);
    return date;
}
