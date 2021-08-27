# Feast Custom Offline Store
[![test-offline-store](https://github.com/feast-dev/feast-custom-offline-store-demo/actions/workflows/test_custom_offline_store.yml/badge.svg?branch=main)](https://github.com/feast-dev/feast-custom-offline-store-demo/actions/workflows/test_custom_offline_store.yml)

### Overview

This repository demonstrates how developers can create their own custom `offline store`s for Feast.
Custom offline stores allow users to use any underlying data store as their offline feature store. Features can be retrieved from the offline store for model training, and can be materialized into the online feature store for use during model inference. 


### Why create a custom offline store?

Feast uses an offline store as the source of truth for features. These features can be retrieved from the offline store for model training. Typically, scalable data warehouses are used for this purpose.
 
Feast also materializes features from offline stores to an online store for low-latency lookup at model inference time. 

Feast comes with some offline stores built in, e.g, Parquet file, Redshift and Bigquery. However, users can develop their own offline stores by creating a class that implements the contract in the [OfflineStore class](https://github.com/feast-dev/feast/blob/5e61a6f17c3b52f20b449214a4bb56bafa5cfcbc/sdk/python/feast/infra/offline_stores/offline_store.py#L41).

### What is included in this repository?

* [feast_custom_offline_store/](feast_custom_offline_store): An example of a custom offline store, `CustomFileOfflineStore`, which implements OfflineStore. This example offline store overrides the File offline store that is provided by Feast.
* [feature_repo/](feature_repo): A simple feature repository that is used to test the custom offline store. The repository has been configured to use the custom offline store as part of it's `feature_store.yaml`
* [test_custom_offline_store.py](test_custom_offline_store.py): A test case that uses `CustomFileOfflineStore` through the `feature_repo/`

### Testing the custom offline store in this repository

Run the following commands to test the custom offline store ([FileCustomOfflineStore](https://github.com/feast-dev/feast-custom-offline-store-demo/blob/master/feast_custom_offline_store/file.py))

```bash
pip install -r requirements.txt
```

```
pytest test_custom_offline_store.py
```

It is also possible to run Feast CLI commands, which in turn will call the offline store. It may be necessary to add the 
`PYTHONPATH` to the path where your offline store module is located.
```
$ PYTHONPATH=$PYTHONPATH:/$(pwd) feast -c feature_repo apply
```
```
Registered entity driver_id
Registered feature view driver_hourly_stats
Deploying infrastructure for driver_hourly_stats
```
```
$ PYTHONPATH=$PYTHONPATH:/$(pwd) feast -c feature_repo materialize-incremental 2021-08-19T22:29:28
```
```
Materializing 1 feature views to 2021-08-19 15:29:28-07:00 into the sqlite online store.

driver_hourly_stats from 2020-08-24 20:54:03-07:00 to 2021-08-19 15:29:28-07:00:
Pulling latest features from my offline store
100%|███████████████████████████████████████████████████████████████| 5/5 [00:00<00:00, 2122.19it/s]```
