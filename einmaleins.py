import datetime
import itertools
from random import shuffle, randrange


def generate_exercises(min_size, limit, num_exercises, type_exercises):
    exercise_list = []
    for i, j in itertools.product(range(min_size, limit + 1), range(1, 11)):
        exercise_list.append((i, j, (i) * (j), '*'))
    while len(exercise_list) < num_exercises:
        exercise_list += exercise_list
    shuffle(exercise_list)
    if type_exercises == 'd':
        exercise_list = [type_exercise_to_division(x) for x in exercise_list]
    if type_exercises == 'b':
        global percentage_division
        counter = 0
        for i in range(len(exercise_list)):
            if randrange(100) <= percentage_division:
                counter+=1
                exercise_list[i] = type_exercise_to_division(exercise_list[i])
        print(str(counter)+" von "+str(num_exercises)+" Aufgaben sind Division.")
    return exercise_list[0:num_exercises]


def type_exercise_to_division(exercise):
    if randrange(2) == 1:
        exercise = exercise[2], exercise[1], exercise[0], '/'
    else:
        exercise = exercise[2], exercise[0], exercise[1], '/'
    return exercise


def get_user_input(question, default_value):
    choice = ''
    while choice == '':
        try:
            choice = input(question + " ")
            if choice == '':
                choice = default_value
            choice = int(choice)
        except:
            choice = ''
    return choice


def get_user_value(question, allowed_values):
    choice = ''
    while choice not in allowed_values:
        choice = str(input(question + " ")).lower()
    return choice


if __name__ == "__main__":
    minsize = get_user_input("Ab welcher Zahl soll das 1*1 starten? [1]", 1)
    gridsize = get_user_input("Bis zu welcher Zahl soll das 1*1 gehen? [10]", 10)
    print("OK, dann geht es bis %s*%s." % (gridsize, gridsize))
    num_exercises = get_user_input("Wie viele Aufgaben sollen gestellt werden? [%s]" % (gridsize ** 2),
                                   gridsize ** 2)
    print("Es werden also %i Aufgaben gestellt." % (num_exercises))
    type_exercises = get_user_value("Nur (M)ultiplikation, nur (D)ivision oder (b)eides?", ('m', 'd', 'b'))
    if type_exercises=='b':
        percentage_division = get_user_input("Wieviel Prozent sollen Division sein? [50]", 50)
    exercise_list = generate_exercises(minsize, gridsize, num_exercises, type_exercises)
    incorrect_answers = 0
    started = datetime.datetime.now().replace(microsecond=0)
    do_end = False
    count = 0
    while not do_end and len(exercise_list) > 0:
        if len(exercise_list) % 10 == 0 and len(exercise_list) != num_exercises:
            print("Es sind noch %s Aufgaben uebrig." % (len(exercise_list)))
        exercise = exercise_list.pop(0)
        result = ''
        failed = False
        while not do_end:
            result = input(str(exercise[0]) + ' ' + exercise[3] + ' ' + str(exercise[1]) + " = ")
            result = result.strip()
            if result == 'q':
                do_end = True
                break
            count = count + 1
            if result != str(exercise[2]):
                if not failed:
                    print("Das Ergebnis ist leider nicht richtig. Versuche es noch einmal.")
                    incorrect_answers += 1
                    failed = True
                else:
                    print("Dieses Ergebnis ist leider auch falsch. Denk noch einmal in Ruhe nach!")
            else:
                break
    ended = datetime.datetime.now().replace(microsecond=0)
    print("Du hast von %s Aufgaben %s im ersten Anlauf richtig beantwortet." % (
        count, count - incorrect_answers))
    print("Insgesamt hast Du %s gebraucht." % (ended - started))
