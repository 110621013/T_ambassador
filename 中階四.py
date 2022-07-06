

if __name__ == '__main__':
    input_num_str = input('input cards number:')
    
    #check input
    while True:
        if len(input_num_str) != 16:
            print('cards number length error, re-input!')
            input_num_str = input('input cards number:')
            continue
        
        all_num_flag = True
        for c in input_num_str:
            if ord(c)<=57 and ord(c)>=48:
                pass
            else:
                all_num_flag = False
        if not all_num_flag:
            print('all chr must be number, re-input!')
            input_num_str = input('input cards number:')
            continue
        
        break
    
    result = 0
    for i in range(0, 16, 2):
        new_num = int(input_num_str[i])*2
        if new_num>=10:
            result += new_num%10 + 1
        else:
            result += new_num
    for i in range(1, 16, 2):
        result += int(input_num_str[i])
        
    if result%10 == 0:
        print('cards number correct!! 水啦')
    else:
        print('cards number error!!')