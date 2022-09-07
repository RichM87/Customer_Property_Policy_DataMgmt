from random_address import real_random_address
import random,pdb,csv,sys
import ctypes
import random_address

states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

real_random_address()

maxRecords = int(sys.argv[1])

def write_to_fakeAddresses(randAddress):
    with open('.\\fakeAddresses.csv', mode='a', newline='') as fakeAddresses:
        street = randAddress['address1']
        city = randAddress['city']
        state = randAddress['state']
        # print(street,city,state)
        # pdb.set_trace()
        csv_writer = csv.writer(fakeAddresses, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([street, city, state])
        # ctypes.windll.user32.MessageBoxW(0, city, "Check It Out", 1)
        #need to delete this file after processing (potentiall)


i = 0
addrList = []

while i <= maxRecords:
    randState = random.choice(states)
    # print(randState)
    randAddress = random_address.real_random_address_by_state(randState)
    if not randAddress:
        # print('empty dictionary')
        continue
    else:
        if randAddress['address1'] in addrList:
            # pdb.set_trace()
            continue
        elif randAddress['address1'] not in  addrList:
            try:
                addrList.append(randAddress['address1'])
                print(randAddress['address1'])
                write_to_fakeAddresses(randAddress)
                i += 1
            except:
                pass
        continue


        # pdb.set_trace()
        # print(randAddress['city'])





