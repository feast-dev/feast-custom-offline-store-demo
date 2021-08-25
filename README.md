# Feast Custom Offline Store
[![test-offline-store](https://github.com/feast-dev/feast-custom-offline-store-demo/actions/workflows/test_offline_store.yml/badge.svg?branch=main)](https://github.com/feast-dev/feast-custom-offline-store-demo/actions/workflows/test_offline_store.yml)

### Overview

This repository demonstrates how developers can create their own custom `providers` for Feast. Custom providers can be
used like plugins which allow Feast users to execute any custom logic. Typical examples include
* Launching custom streaming ingestion jobs (Spark, Beam)
* Launching custom batch ingestion (materialization) jobs (Spark, Beam)
* Adding custom validation to feature repositories during `feast apply`
* Adding custom infrastructure setup logic which runs during `feast apply`
* Extending Feast commands with in-house metrics, logging, or tracing

### Why create a custom provider?

All Feast operations execute through a provider. Operations like materializing data from the offline to the online
store, updating infrastructure like databases, launching streaming ingestion jobs, building training datasets, and
reading features from the online store.

Feast comes with providers built in, e.g, LocalProvider, GcpProvider, and AwsProvider. However, users can develop their
own providers by creating a class that implements the contract in the [Provider class](https://github.com/feast-dev/feast/blob/745a1b43d20c0169b675b1f28039854205fb8180/sdk/python/feast/infra/provider.py#L22).

Most developers, however, simply want to add new logic to Feast and don't necessarily want to create a whole provider on
their own. The fastest way to add custom logic to Feast is to extend an existing provider. The most generic
provider is the LocalProvider, which contains no custom logic specific to a cloud environment.

### What is included in this repository?

* [feast_custom_offline_store/](feast_custom_offline_store): An example of a custom provider, `MyCustomProvider`, which extends the Feast
`LocalProvider`. This example provider simply prints messages to the console.
* [feature_repo/](basic_feature_repo): A simple feature repository that is used to test the custom provider. The repository has been configured to use the custom provider as part of it's `feature_store.yaml`
* [test_custom_offline_store.py](test_custom_provider.py): A test case that uses `MyCustomProvider` through the `basic_feature_repo/`

### Testing the custom provider in this repository

Run the following commands to test the custom offline store ([FileCustomOfflineStore](https://github.com/feast-dev/feast-custom-offline-store-demo/blob/master/feast_custom_offline_store/file.py))

```bash
pip install -r requirements.txt
```

```
pytest test_custom_provider.py
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