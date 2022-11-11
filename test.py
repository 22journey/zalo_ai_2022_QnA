
from concurrent.futures import ProcessPoolExecutor
from time import sleep
 
values = [3,4,5,6]
def cube(x):
    print(f'Cube of {x}:{x*x*x}')
 
 
if __name__ == '__main__':
    result =[]
    with ProcessPoolExecutor(max_workers=5) as exe:
        exe.submit(cube,2)
         
        # Maps the method 'cube' with a iterable
        result = exe.map(cube,values)
     
    for r in result:
      print(r)
