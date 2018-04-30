function fmt_percent(percent) {
  if (isNaN(percent)) return percent
  return Number.parseFloat(percent).toFixed(2) + '%'
}

function fmt_duration(duration) {
  if (isNaN(duration)) return duration
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

function fmt_filesize(size) {
  if (isNaN(size)) return size
  size = Number.parseFloat(size)
  units = [
    '',
    'Ki',
    'Mi',
    'Gi'
  ]
  for (unit in units) {
    if (Math.abs(size) < 1024) {
      return size.toFixed(1) + units[unit] + 'B'
    }
    size /= 1024
  }
  return size.toFixed(1) + 'TiB'
}

