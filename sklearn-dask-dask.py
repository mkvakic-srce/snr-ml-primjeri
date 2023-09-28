
import os

from xgboost.dask import DaskXGBClassifier
from dask_ml.datasets import make_classification

from distributed import Client, progress, wait

def main():

    # client
    client = Client(os.environ['SCHEDULER_ADDRESS'])

    # vars
    n_samples = 10**8
    n_features = 50
    n_workers = len(client.scheduler_info()['workers'])

    # data
    X, y = make_classification(n_samples=n_samples,
                               n_features=n_features,
                               n_informative=n_features//5,
                               chunks=(n_samples//n_workers, n_features))

    # fit
    estimator = DaskXGBClassifier()
    estimator.fit(X, y)

    # shutdown
    client.shutdown()

if __name__ == '__main__':
    main()