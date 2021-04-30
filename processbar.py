def progressBar(current, total, barLength = 50):
    percent = float(current) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))
    print('Progress: [%s%s] %d %%' % (arrow, spaces, percent), end='\r')

def create_file_arr():
    H = 100000
    barLength = 100
    #H_fx = 100000
    for i in range(H):
        H -= 1
        Ostatok = H/100000*100
        #time.sleep(0.2)
        P = barLength - int(Ostatok)
        progressBar(P,barLength)

create_file_arr()

