// some simple formating functions

// return value or "-" if undefined
function fmt_default(input) {
    return (input && input.length) ? input : "-";
}

// turn float into formated percent number
function fmt_percent(percent) {
    if (isNaN(percent)) return '-'
    return Number.parseFloat(percent).toFixed(2) + '%'
}

// format seconds to human readable duration
function fmt_duration(duration) {
    if (isNaN(duration)) return '-'
    duration = parseInt(duration)
    days = Math.floor(duration / (60 * 60 * 24))
    duration %= 60 * 60 * 24
    hours = Math.floor(duration / (60 * 60))
    duration %= 60 * 60
    minutes = Math.floor(duration / 60)
    if (days > 1) return days + 'd'
    if (days == 1) return (hours + 24) + 'h'
    if (hours > 1) return hours + 'h'
    if (hours == 1) return (minutes + 60) + 'm'
    return minutes + 'm'
}

// format Bits/Bytes to human readable size
function fmt_filesize(size, suffix) {
    if (typeof suffix == 'undefined') {
        suffix = 'B'
    }
    if (isNaN(size)) return '-'
    size = Number.parseFloat(size)
    units = [
        '',
        'Ki',
        'Mi',
        'Gi'
    ]
    for (unit in units) {
        if (Math.abs(size) < 1024) {
            return size.toFixed(1) + units[unit] + suffix
        }
        size /= 1024
    }
    return size.toFixed(1) + 'Ti' + suffix
}
