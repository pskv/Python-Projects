from typing import List

def is_cheaper_flight_exists(src_flight, schedule):
  start = src_flight[0]
  finish = src_flight[1]
  src_weight = src_flight[2]

  for flight in schedule:

    if start in flight:
      if flight[2] > src_weight:
        continue

      local_finish = flight[abs(flight.index(start)-1)]

      if local_finish == finish:
        return 'YES'
      else:
        i = schedule.index(flight)
        if is_cheaper_flight_exists([local_finish, finish, src_weight-flight[2]], schedule[:i]+schedule[i+1:]) == 'NO':
            continue
        else:
            return 'YES'
  return 'NO'

def useless_flight(schedule: List) -> List:
    res = []
    for i in range(len(schedule)):
        if is_cheaper_flight_exists(schedule[i], schedule[:i]+schedule[i+1:]) == 'YES':
            res.append(i)
    return res


if __name__ == '__main__':
    print("Example:")
    # print(useless_flight([['A', 'B', 50],
  # ['B', 'C', 40],
  # ['A', 'C', 100]]))
    print(
        useless_flight([["A","H",35],["A","I",10],["A","J",45],["A","M",70],["B","E",25],["B","H",45],["B","N",55],["B","O",30],["C","D",75],["C","G",85],["C","J",45],["C","K",50],["D","G",30],["D","K",80],["D","L",85],["E","O",85],["F","G",50],["F","J",75],["F","M",70],["F","N",45],["G","J",40],["H","M",40],["H","O",50],["I","K",30],["I","L",90],["I","O",50],["K","L",55],["M","N",75]])
    )

    # These "asserts" are used for self-checking and not for an auto-testing
  #   assert useless_flight([['A', 'B', 50],
  # ['B', 'C', 40],
  # ['A', 'C', 100]]) == [2]
  #   assert useless_flight([['A', 'B', 50],
  # ['B', 'C', 40],
  # ['A', 'C', 90]]) == []
  #   assert useless_flight([['A', 'B', 50],
  # ['B', 'C', 40],
  # ['A', 'C', 40]]) == []
  #   assert useless_flight([['A', 'C', 10],
  # ['C', 'B', 10],
  # ['C', 'E', 10],
  # ['C', 'D', 10],
  # ['B', 'E', 25],
  # ['A', 'D', 20],
  # ['D', 'F', 50],
  # ['E', 'F', 90]]) == [4, 7]
  #   print("Coding complete? Click 'Check' to earn cool rewards!")
