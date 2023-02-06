from prefect import flow, task

@flow(log_prints=True)
def test():
    print("hello")

if __name__ == '__main__':
    test()
