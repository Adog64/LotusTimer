VALID_TIME_FORMATS = ('00:00:00.00', '0:00:00.00', '00:00.00', '0:00.00', '00.00', '0.00', '.00',
                 '0:00', '00:00', '0:00:00', '00:00:00', '0.0', '00.0', '0:00.0', '00:00.0', '0:00:00.0', '00:00:00.0',
                 '0.', '00.', '0:00.', '00:00.', '0:00:00.', '00:00:00.', '')

def time_ms(time):
        f = '00:00:00.00'
        if time[-2:] == '+2':
            time = time[:-2]
        elif time[-3:] == 'dnf':
            time = time[:-3]
        time = '00' + time + '00'
        dec = time.find('.')
        col = time.find(':')
        col2 = time.rfind(':')
        if '.' in time:
            f = f[:9] + time[dec+1:dec+3]
            f = f[:6] + time[dec-2:dec] + f[8:]
        if ':' in time:
            f = f[:6] + time[col2+1:col2+3] + f[8:]
            f = f[:3] + time[col2-2:col2] + f[5:]
        if col != col2:
             f = time[col-2:col] + f[2:]
        if dec == col:
            time = time[2:-2]
            while len(time) < 8:
                time = '0' + time
            f = time[:2] + ':' + time[2:4] + ':' + time[4:6] + '.' + time[6:]
        ms = 0
        mul = 10
        for c in f[-1::-1]:
            if c.isnumeric():
                ms += int(c) * mul
                mul*=10
            elif c == ':':
                mul*=60
        return ms

print(time_ms('15:49'))