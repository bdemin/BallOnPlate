months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']
          
def valid_month(month):
    month = month.capitalize()
    if any(month in item for item in months):
        return month
    else:
        return None

print(valid_month('august'))

print(valid_month('July'))
print(valid_month('asd'))
print(valid_month('34'))
print(valid_month('AuGust'))