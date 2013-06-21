# gdb script to solve "policebox" challenge for defcon 21 quals
# by jiva

# Using gdb.execute in python to make gdb STFU

python gdb.execute('file policebox', to_string=True)
python gdb.execute('core-file core', to_string=True)
python gdb.execute('record restore core', to_string=True)

#    0x08048695 <+119>:   mov    BYTE PTR [esp+0x1b],al
python gdb.execute('b *0x08048695', to_string=True)

define stepget
  c
  x/c $esp+0x1b
end

# Begin replay
python gdb.execute('c', to_string=True)
python print 'The key is:', ''.join([gdb.execute('stepget', to_string=True)[-3] for i in xrange(23)])

python gdb.execute('quit', to_string=True)
