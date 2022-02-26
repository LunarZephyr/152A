import sys

# I: A file
# O: An array of strings containing each line of the file
def open_file(file):
    peek = open(file)
    contents = [line.strip() for line in peek.readlines()]
    peek.close()

    return contents

# I: An array of strings representing the address blocks
# O: A list of arrays that represent each possible address block
def parse_db(db):
    list = []
    for i in range(0, len(db)):
        line = db[i].split(" ")
        list.append(line)

    return list

# I: ipaddress
# O: ipaddress in binary notation
def ipaddress(ip, prefix = '32'):
    ipadd = map(int, ip.split('.'))
    try:
        binary = '{0:08b}{1:08b}{2:08b}{3:08b}'.format(*ipadd)
    except:
        return #couple of ip addresses that are incomplete, have errors; this to ignore those
    return binary[:int(prefix)]

# I: An IP address and a database record block
# O: True if they overlap
#def overlap(ip_address, db_block):
    # Code
def longest_prefix_match(ip, dbase):
    binary = ipaddress(ip)
    while True:
        if binary in dbase.keys():
            return dbase[binary]
        binary = binary[:-1]
    
def make_hash(db):
    hash_table = {}
    for i in db[:-1]: #remove '[]' entry error
        binary = ipaddress(i[0], i[1])
        hash_table[binary] = i
        #if i == ['255.255.254.0', '24', '5650']:
            #print(binary)
    return hash_table

# I: Database and IP lists
# O: The IP and the block with the record w/ the longest prefix
def ip2as(db, ip):
    # Map each IP to an overlapping block
    dbase = make_hash(db)
    match = ''
    for i in ip:
        value = longest_prefix_match(i, dbase)
        match = match + ('%s/%s %s %s\n' %(value[0], value[1], value[2], i))
    file = open('output.txt', 'w')
    file.write(match)

def main():
    db_file = open_file(sys.argv[1])
    db_list = parse_db(db_file)
    ip_list = open_file(sys.argv[2])

    output = ip2as(db_list, ip_list)
    #print(output)

if __name__ == "__main__":
    main()
