import os


cur_file = os.path.basename(__file__)

print('starting tests...')

for test_file in os.listdir():
    if test_file != cur_file:
        print('running', test_file)
        __import__(test_file)
print('tests finished')
