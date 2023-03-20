from System.units import parse

task = '#задача  \n' \
       'Написать бота  \n' \
       'Ханов  ,     Макурин  \n' \
       'до 23:50 16.03.23   \n' \
       '  сделайте     пожалуйста бота \n' \
       'очень сука блин нужно '

t = parse.message(task, '148866296')
print(t)
