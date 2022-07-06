input_str =  '"K<K qk(lp](lzYl]uYzc(gn |`m Kgvlzgt LY|Y(;wjxgzY|awf6'
output_str = '*CDC is the trademark of the Control Data Corporation.'
input_str_2 =  '"KLJ;(:ifs qk(Yugv_{l(lp](dijo]{l(hza~Y|]tq(gfm\(Zifsk(av \Yqoif6'
output_str_2 = '*CTBC Bank is amongst the largest privately owned banks in Taiwan.'

if __name__ == '__main__':
    print('in main', len(input_str), len(output_str))
    print('in main 2', len(input_str_2), len(output_str_2))
    
    # if idx odd -> K=-8 / idx even -> K=+8 / ' ' still ' '
    #for idx in range(len(input_str)):
    #    print(idx, ord(input_str[idx]), ord(output_str[idx]), ord(input_str[idx])-ord(output_str[idx]))
        
    # begin decoding
    i_s = input_str_2 # any input_str you want
    o_s = ''
    for idx in range(len(i_s)):
        if i_s[idx] == ' ':
            o_s += ' '
        elif idx%2 == 0:
            o_s += chr(ord(i_s[idx])+8)
        else:
            o_s += chr(ord(i_s[idx])-8)
    print(i_s)
    print(o_s)
    print(output_str_2)