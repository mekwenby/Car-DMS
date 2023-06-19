import random
from multiprocessing import Pool
import Model


def create_workorder_with_ids(ids):
    Model.create_demo_workorder(ids)


if __name__ == '__main__':
    Model.WorkOrder.update(delete_=True).where(Model.WorkOrder.checkout==False).execute()
    '''pool = Pool(12)  # start 8 worker processes
    cars = Model.Car.select()
    ids = random.randint(0, len(Model.Car.select()) - 5)
    for _ in range(300000):
        ids = random.randint(1, len(cars) - 4)
        pool.apply_async(create_workorder_with_ids, args=(ids,))
    pool.close()
    pool.join()'''
