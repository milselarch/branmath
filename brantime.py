import time
import random
import math
import os

import datetime

class Question(object):
    def __init__(self, N1, N2, answers, duration):
        self.answers = answers
        self.duration = duration
        self.N1 = N1
        self.N2 = N2

    def correct(self):
        return len(self.answers) == 1

    def getDifficulty(self):
        return math.log10(1 + self.N1) * math.log10(1 + self.N2)

    def getPoints(self):
        difficulty = self.getDifficulty()
        points = difficulty * int(self.correct())
        discount = 1 - 1 / (10 ** difficulty)
        # print(difficulty, points, discount, self.correct(), self.answers)
        points *= discount
        return points

    def encode(self):
        return {
            'answers': self.answers,
            'duration': self.duration,
            'N1': self.N1,
            'N2': self.N2
        }


class Tester(object):
    def __init__(self):
        self.difficulty = None

    def humanize(self, minutes):
        hours = minutes // 60
        modmin = minutes % 60

        if minutes < 60:
            return f'12:{minutes} AM'
        elif minutes < 60 * 12:
            return f'{hours}:{modmin} AM'
        elif 60 * 12 <= minutes < 60 * 13:
            return f'{12}:{modmin} PM'
        else:
            return f'{hours % 12}:{modmin} PM'

    def readMin(self, output):
        if ':' in output:
            output = [int(x) for x in output.split(':')]
            hours, minutes = output
            output = hours * 60 + minutes

        return int(output)

    def play(self):
        dones = [(0, 0)]
        difficulty = -1

        turn = 1
        stop = False
        startTime = time.time()
        history = []
        points = 0

        while stop is False:
            ans, tries, key = 0, 512, None
            N1, N2 = 0, 0

            while (key is None) or (key in dones):
                # input(f'REPEAT {(N1, N2)}')
                D1 = random.choice(range(60 * 24))
                D2 = random.choice(range(60 * 24))
                D1, D2 = sorted([D1, D2])
                N1 = self.humanize(D1)
                N2 = self.humanize(D2)

                key = (D1, D2)
                ans = D2 - D1
                tries -= 1

                if tries == 0:
                    stop = True
                    break

            question = f"{N1} to {N2} = "
            start = time.time()
            answers = []
            output = None
            os.system('clear')
            # 23.82365378126771s per point

            while output != ans:
                output = input(f"INN[{turn}]: {question}")
                if output == 'STOP':
                    stop = True
                    break

                try:
                    output = self.readMin(output)
                    answers.append(output)
                    # print('OUTANS', output, ans)
                except ValueError:
                    print(f"OUT[{turn}]: INVALID")

            end = time.time()
            duration = end - start
            info = Question(N1, N2, answers, duration)
            dones.append(key)

            points = 1
            # input(f"OUT[{turn}]: points: {round(points, 2)}")
            history.append(info)

            if stop is True:
                break

            turn += 1

        endTime = time.time()
        duration = endTime - startTime
        correct = sum([int(question.correct()) for question in history])
        percentage = correct / turn
        points = sum([question.getPoints() for question in history])
        points *= percentage

        print(f"START {startTime} END {endTime} DURATION {duration}")
        print(f'DONE {turn} CORRECT-P {round(percentage * 100, 2)}%')
        print(f'POINTS {points}')

        fname = datetime.datetime.fromtimestamp(startTime)
        fname = fname.strftime('%m-%d-%Y-%H:%M:%S')
        open(f'stats/{fname}.txt', 'w').write(str({
            'history': [h.encode() for h in history],
            'duration': duration, 'start': startTime,
            'points': points
        }))


if __name__ == '__main__':
    tester = Tester()
    tester.play()
