from tasks.future import Future
from tasks.taskmanager import TaskManager
from tasks.task import *
import types


"""An API for scheduling tasks that run against Couchbase Server

This module is contains the top-level API's for scheduling and executing tasks. The
API provides a way to run task do syncronously and asynchronously.
"""

class Cluster(object):
    """An API for interacting with Couchbase clusters"""

    def __init__(self):
        self.task_manager = TaskManager("Cluster_Thread")
        self.task_manager.start()

    def async_create_default_bucket(self, bucket_params):
        """Asynchronously creates the default bucket

        Parameters:
            bucket_params - a dictionary containing bucket creation parameters. (Dict)
        Returns:
            BucketCreateTask - A task future that is a handle to the scheduled task."""
        if 'bucket_name' not in bucket_params.keys():
            bucket_params['bucket_name'] = 'default'
        _task = BucketCreateTask(bucket_params)
        self.task_manager.schedule(_task)
        return _task

    def async_create_sasl_bucket(self, name, password, bucket_params):
        """Asynchronously creates a sasl bucket

        Parameters:
            bucket_params - a dictionary containing bucket creation parameters. (Dict)

        Returns:
            BucketCreateTask - A task future that is a handle to the scheduled task."""
        bucket_params['bucket_name'] = name
        bucket_params['password'] = password
        _task = BucketCreateTask(bucket_params)
        self.task_manager.schedule(_task)
        return _task

    def async_create_standard_bucket(self, name, port, bucket_params):
        """Asynchronously creates a standard bucket
        Parameters:
            bucket_params - A dictionary containing a list of bucket creation parameters. (Dict)
        Returns:
            BucketCreateTask - A task future that is a handle to the scheduled task."""

        bucket_params['bucket_name'] = name
        bucket_params['port'] = port
        _task = BucketCreateTask(bucket_params)
        self.task_manager.schedule(_task)
        return _task

    def async_create_memcached_bucket(self, name, port, bucket_params):
        """Asynchronously creates a standard bucket

        Parameters:
            bucket_params - A dictionary containing a list of bucket creation parameters. (Dict)

        Returns:
            BucketCreateTask - A task future that is a handle to the scheduled task."""
        bucket_params['bucket_name'] = name
        bucket_params['port'] = port
        bucket_params['bucket_type'] = 'memcached'
        _task = BucketCreateTask(bucket_params)
        self.task_manager.schedule(_task)
        return _task

    def async_bucket_delete(self, server, bucket='default'):
        """Asynchronously deletes a bucket

        Parameters:
            server - The server to delete the bucket on. (TestInputServer)
            bucket - The name of the bucket to be deleted. (String)

        Returns:
            BucketDeleteTask - A task future that is a handle to the scheduled task."""
        _task = BucketDeleteTask(server, bucket)
        self.task_manager.schedule(_task)
        return _task



    def async_failover(self, servers=[], failover_nodes=[], graceful=False,
                       use_hostnames=False, wait_for_pending=0):
        """Asynchronously failover a set of nodes

        Parameters:
            servers - servers used for connection. (TestInputServer)
            failover_nodes - The set of servers that will under go failover .(TestInputServer)
            graceful = True/False. True - graceful, False - hard. (Boolean)

        Returns:
            FailOverTask - A task future that is a handle to the scheduled task."""
        _task = FailoverTask(servers, to_failover=failover_nodes,
                             graceful=graceful, use_hostnames=use_hostnames,
                             wait_for_pending=wait_for_pending)
        self.task_manager.schedule(_task)
        return _task

    def async_create_scope(self, server, bucket_name, scope_name):
        _task = ScopeCreateTask(server, bucket_name, scope_name)
        self.task_manager.schedule(_task)
        return _task

    def async_create_collection(self, server, bucket_name, scope_name, collection_name, collection_params):
        _task = CollectionCreateTask(server, bucket_name, scope_name, collection_name, collection_params)
        self.task_manager.schedule(_task)
        return _task

    def async_create_scope_collection(self, server, bucket_name, scope_name, collection_name, collection_params):
        _task = ScopeCollectionCreateTask(server, bucket_name, scope_name, collection_name, collection_params)
        self.task_manager.schedule(_task)
        return _task

    def async_delete_scope(self, server, bucket_name, scope_name):
        _task = ScopeDeleteTask(server, bucket_name, scope_name)
        self.task_manager.schedule(_task)
        return _task

    def async_delete_collection(self, server, bucket_name, scope_name, collection_name):
        _task = CollectionDeleteTask(server, bucket_name, scope_name, collection_name)
        self.task_manager.schedule(_task)
        return _task

    def async_delete_scope_collection(self, server, bucket_name, scope_name, collection_name):
        _task = ScopeCollectionDeleteTask(server, bucket_name, scope_name, collection_name)
        self.task_manager.schedule(_task)
        return _task

    def async_init_node(self, server, disabled_consistent_view=None,
                        rebalanceIndexWaitingDisabled=None, rebalanceIndexPausingDisabled=None,
                        maxParallelIndexers=None, maxParallelReplicaIndexers=None, port=None,
                        quota_percent=None, services = None, index_quota_percent = None, gsi_type='forestdb'):
        """Asynchronously initializes a node

        The task scheduled will initialize a nodes username and password and will establish
        the nodes memory quota to be 2/3 of the available system memory.

        Parameters:
            server - The server to initialize. (TestInputServer)
            disabled_consistent_view - disable consistent view
            rebalanceIndexWaitingDisabled - index waiting during rebalance(Boolean)
            rebalanceIndexPausingDisabled - index pausing during rebalance(Boolean)
            maxParallelIndexers - max parallel indexers threads(Int)
            index_quota_percent - index quote used by GSI service (added due to sherlock)
            maxParallelReplicaIndexers - max parallel replica indexers threads(int)
            port - port to initialize cluster
            quota_percent - percent of memory to initialize
            services - can be kv, n1ql, index
            gsi_type - Indexer Storage Mode
        Returns:
            NodeInitTask - A task future that is a handle to the scheduled task."""

        _task = NodeInitializeTask(server, disabled_consistent_view, rebalanceIndexWaitingDisabled,
                          rebalanceIndexPausingDisabled, maxParallelIndexers, maxParallelReplicaIndexers,
                          port, quota_percent, services = services, index_quota_percent = index_quota_percent,
                          gsi_type=gsi_type)
        self.task_manager.schedule(_task)
        return _task

    def async_load_gen_docs(self, server, bucket, generator, kv_store=None, op_type=None, exp=0, flag=0, only_store_hash=True,
                            batch_size=1, pause_secs=1, timeout_secs=5, proxy_client=None, compression=True, collection=None):

        print("-->Cluster.async_load_gen_docs...")
        if isinstance(generator, list):
                print("loading list from LoadDocumentsGeneratorsTask...")
                _task = LoadDocumentsGeneratorsTask(server, bucket, generator, kv_store, op_type, exp, flag,
                                                    only_store_hash, batch_size, compression=compression, collection=collection)
        # Load using java sdk client
        elif not generator.isGenerator():
                print("loading from SDKLoadDocumentsTask...")
                _task = SDKLoadDocumentsTask(server, bucket, generator, pause_secs, timeout_secs)
        else:
                print("loading elements as [] from LoadDocumentsGeneratorsTask...")
                _task = LoadDocumentsGeneratorsTask(server, bucket, [generator], kv_store, op_type, exp, flag,
                                                    only_store_hash, batch_size, compression=compression, collection=collection)

        self.task_manager.schedule(_task)
        return _task

    def async_workload(self, server, bucket, kv_store, num_ops, create, read, update,
                       delete, exp, compression=True, collection=None):
        _task = WorkloadTask(server, bucket, kv_store, num_ops, create, read, update,
                             delete, exp, compression=compression, collection=collection)
        self.task_manager.schedule(_task)
        return _task

    def async_verify_data(self, server, bucket, kv_store, max_verify=None,
                          only_store_hash=True, batch_size=1, replica_to_read=None, timeout_sec=5, compression=True, collection=None):
        if batch_size > 1:
            _task = BatchedValidateDataTask(server, bucket, kv_store, max_verify, only_store_hash, batch_size,
                                            timeout_sec, compression=compression, collection=collection)
        else:
            _task = ValidateDataTask(server, bucket, kv_store, max_verify, only_store_hash, replica_to_read,
                                     compression=compression, collection=collection)
        self.task_manager.schedule(_task)
        return _task

    def async_verify_active_replica_data(self, server, bucket, kv_store, max_verify=None, compression=True, collection=None):
        _task = ValidateDataWithActiveAndReplicaTask(server, bucket, kv_store, max_verify, compression=compression, collection=collection)
        self.task_manager.schedule(_task)
        return _task

    def async_verify_meta_data(self, dest_server, bucket, kv_store, meta_data_store, collection=None):
        _task = VerifyMetaDataTask(dest_server, bucket, kv_store, meta_data_store, collection=collection)
        self.task_manager.schedule(_task)
        return _task

    def async_get_meta_data(self, dest_server, bucket, kv_store, compression=True, collection=None):
        _task = GetMetaDataTask(dest_server, bucket, kv_store, compression=compression, collection=collection)
        self.task_manager.schedule(_task)
        return _task

    def async_verify_revid(self, src_server, dest_server, bucket, src_kv_store, dest_kv_store, max_verify=None,
                           compression=True, collection=None):
        _task = VerifyRevIdTask(src_server, dest_server, bucket, src_kv_store, dest_kv_store, max_verify=max_verify,
                                compression=compression, collection=collection)
        self.task_manager.schedule(_task)
        return _task

    def async_run_fts_query_compare(self, fts_index, es_instance, query_index,
                                    es_index_name=None, n1ql_executor=None):
        _task = ESRunQueryCompare(fts_index,
                                  es_instance,
                                  query_index=query_index,
                                  es_index_name=es_index_name,
                                  n1ql_executor=n1ql_executor)
        self.task_manager.schedule(_task)
        return _task

    def async_rebalance(self, servers, to_add, to_remove, use_hostnames=False,
                        services=None, sleep_before_rebalance=None):
        """Asyncronously rebalances a cluster

        Parameters:
            servers - All servers participating in the rebalance ([TestInputServers])
            to_add - All servers being added to the cluster ([TestInputServers])
            to_remove - All servers being removed from the cluster ([TestInputServers])
            use_hostnames - True if nodes should be added using hostnames (Boolean)

        Returns:
            RebalanceTask - A task future that is a handle to the scheduled task"""
        _task = RebalanceTask(servers, to_add, to_remove,
                              use_hostnames=use_hostnames, services=services,
                              sleep_before_rebalance=sleep_before_rebalance)
        self.task_manager.schedule(_task)
        return _task

    def async_wait_for_stats(self, servers, bucket, param, stat, comparison, value, collection=None):
        """Asynchronously wait for stats

        Waits for stats to match the criteria passed by the stats variable. See
        couchbase.stats_tool.StatsCommon.build_stat_check(...) for a description of
        the stats structure and how it can be built.

        Parameters:
            servers - The servers to get stats from. Specifying multiple servers will
                cause the result from each server to be added together before
                comparing. ([TestInputServer])
            bucket - The name of the bucket (String)
            param - The stats parameter to use. (String)
            stat - The stat that we want to get the value from. (String)
            comparison - How to compare the stat result to the value specified.
            value - The value to compare to.

        Returns:
            RebalanceTask - A task future that is a handle to the scheduled task"""
        _task = StatsWaitTask(servers, bucket, param, stat, comparison, value, collection)
        self.task_manager.schedule(_task)
        return _task

    def async_wait_for_xdcr_stat(self, servers, bucket, param, stat, comparison, value, collection=None):
        """Asynchronously wait for stats

        Waits for stats to match the criteria passed by the stats variable. See
        couchbase.stats_tool.StatsCommon.build_stat_check(...) for a description of
        the stats structure and how it can be built.

        Parameters:
            servers - The servers to get stats from. Specifying multiple servers will
                cause the result from each server to be added together before
                comparing. ([TestInputServer])
            bucket - The name of the bucket (String)
            param - The stats parameter to use. (String)
            stat - The stat that we want to get the value from. (String)
            comparison - How to compare the stat result to the value specified.
            value - The value to compare to.

        Returns:
            RebalanceTask - A task future that is a handle to the scheduled task"""
        _task = XdcrStatsWaitTask(servers, bucket, param, stat, comparison, value, collection=collection)
        self.task_manager.schedule(_task)
        return _task

    def create_default_bucket(self, bucket_params, timeout=600):
        """Synchronously creates the default bucket

        Parameters:
            bucket_params - A dictionary containing a list of bucket creation parameters. (Dict)

        Returns:
            boolean - Whether or not the bucket was created."""

        _task = self.async_create_default_bucket(bucket_params)
        return _task.result(timeout)

    def create_sasl_bucket(self, name, password,bucket_params, timeout=None):
        """Synchronously creates a sasl bucket

        Parameters:
            bucket_params - A dictionary containing a list of bucket creation parameters. (Dict)

        Returns:
            boolean - Whether or not the bucket was created."""

        _task = self.async_create_sasl_bucket(name, password, bucket_params)
        self.task_manager.schedule(_task)
        return _task.result(timeout)

    def create_standard_bucket(self, name, port, bucket_params, timeout=None):
        """Synchronously creates a standard bucket
        Parameters:
            bucket_params - A dictionary containing a list of bucket creation parameters. (Dict)
        Returns:
            boolean - Whether or not the bucket was created."""
        _task = self.async_create_standard_bucket(name, port, bucket_params)
        return _task.result(timeout)

    def bucket_delete(self, server, bucket='default', timeout=None):
        """Synchronously deletes a bucket

        Parameters:
            server - The server to delete the bucket on. (TestInputServer)
            bucket - The name of the bucket to be deleted. (String)

        Returns:
            boolean - Whether or not the bucket was deleted."""
        _task = self.async_bucket_delete(server, bucket)
        return _task.result(timeout)

    def create_scope(self, server, bucket_name, scope_name):
        _task = self.async_create_scope(server, bucket_name, scope_name)
        return _task

    def create_collection(self, server, bucket_name, scope_name, collection_name, collection_params):
        _task = self.async_create_collection(server, bucket_name, scope_name, collection_name, collection_params)
        return _task

    def create_scope_collection(self, server, bucket_name, scope_name, collection_name, collection_params):
        _task = self.async_create_scope_collection(server, bucket_name, scope_name, collection_name, collection_params)
        return _task

    def delete_scope(self, server, bucket_name, scope_name):
        _task = self.async_delete_scope(server, bucket_name, scope_name)
        return _task

    def delete_collection(self, server, bucket_name, scope_name, collection_name):
        _task = self.async_delete_collection(server, bucket_name, scope_name, collection_name)
        return _task

    def delete_scope_collection(self, server, bucket_name, scope_name, collection_name):
        _task = self.async_delete_scope_collection(server, bucket_name, scope_name, collection_name)
        return _task

    def init_node(self, server, async_init_node=True, disabled_consistent_view=None, services = None, index_quota_percent = None):
        """Synchronously initializes a node

        The task scheduled will initialize a nodes username and password and will establish
        the nodes memory quota to be 2/3 of the available system memory.

        Parameters:
            server - The server to initialize. (TestInputServer)
            index_quota_percent - index quota percentage
            disabled_consistent_view - disable consistent view

        Returns:
            boolean - Whether or not the node was properly initialized."""
        _task = self.async_init_node(server, async_init_node, disabled_consistent_view, services = services, index_quota_percent= index_quota_percent)
        return _task.result()

    def rebalance(self, servers, to_add, to_remove, timeout=None,
                  use_hostnames=False, services=None,
                  sleep_before_rebalance=None):
        """Syncronously rebalances a cluster

        Parameters:
            servers - All servers participating in the rebalance ([TestInputServers])
            to_add - All servers being added to the cluster ([TestInputServers])
            to_remove - All servers being removed from the cluster ([TestInputServers])
            use_hostnames - True if nodes should be added using their hostnames (Boolean)
            services - Services definition per Node, default is None (this is since Sherlock release)
            sleep_before_rebalance - If not NONE, rebalance will be delayed for
                                     'n'seconds
        Returns:
            boolean - Whether or not the rebalance was successful"""
        _task = self.async_rebalance(
            servers, to_add, to_remove, use_hostnames, services=services,
            sleep_before_rebalance=sleep_before_rebalance)
        return _task.result(timeout)

    def load_buckets_with_high_ops(self, server, bucket, items, batch=20000,
                                   threads=5, start_document=0, instances=1, ttl=0):
        import subprocess
        from lib.membase.api.rest_client import RestConnection

        cmd_format = "python3 scripts/high_ops_doc_gen.py  --node {0} --bucket {1} --user {2} --password {3} " \
                     "--count {4} --batch_size {5} --threads {6} --start_document {7} --cb_version {8} --instances {9} --ttl {10}"
        cb_version = RestConnection(server).get_nodes_version()[:3]
        cmd = cmd_format.format(server.ip, bucket.name, server.rest_username,
                                server.rest_password,
                                items, batch, threads, start_document,
                                cb_version, instances, ttl)
        print("Running {}".format(cmd))
        result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        output = result.stdout.read()
        error = result.stderr.read()
        if error:
            print(error)
            raise Exception("Failed to run the loadgen.")
        if output:
            loaded = output.split('\n')[:-1]
            total_loaded = 0
            for load in loaded:
                total_loaded += int(load.split(':')[1].strip())
            assert (total_loaded == items),\
                "Failed to load {} items. Loaded only {} items".format(
                                 items,
                                 total_loaded)

    def check_dataloss_for_high_ops_loader(self, server, bucket, items,
                                           batch=20000, threads=5,
                                           start_document=0,
                                           updated=False, ops=0, ttl=0, deleted=False, deleted_items=0):
        import subprocess
        from lib.memcached.helper.data_helper import VBucketAwareMemcached
        from lib.membase.api.rest_client import RestConnection

        cmd_format = "python3 scripts/high_ops_doc_gen.py  --node {0} --bucket {1} --user {2} --password {3} " \
                     "--count {4} " \
                     "--batch_size {5} --threads {6} --start_document {7} --cb_version {8} --validate"
        cb_version = RestConnection(server).get_nodes_version()[:3]
        if updated:
            cmd_format = "{} --updated --ops {}".format(cmd_format, ops)
        if deleted:
            cmd_format = "{} --deleted --deleted_items {}".format(cmd_format, deleted_items)
        if ttl > 0:
            cmd_format = "{} --ttl {}".format(cmd_format, ttl)
        cmd = cmd_format.format(server.ip, bucket.name, server.rest_username,
                                server.rest_password,
                                int(items), batch, threads, start_document, cb_version)
        print("Running {}".format(cmd))
        result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        output = result.stdout.read()
        error = result.stderr.read()
        errors = []
        rest = RestConnection(server)
        VBucketAware = VBucketAwareMemcached(rest, bucket.name)
        _, _, _ = VBucketAware.request_map(rest, bucket.name)
        if error:
            print(error)
            raise Exception("Failed to run the loadgen validator.")
        if output:
            loaded = output.split('\n')[:-1]
            for load in loaded:
                if "Missing keys:" in load:
                    keys = load.split(":")[1].strip().replace('[', '').replace(']', '')
                    keys = keys.split(',')
                    for key in keys:
                        key = key.strip()
                        key = key.replace('\'', '').replace('\\', '')
                        vBucketId = VBucketAware._get_vBucket_id(key)
                        errors.append(
                            ("Missing key: {0}, VBucketId: {1}".format(key, vBucketId)))
                if "Mismatch keys: " in load:
                    keys = load.split(":")[1].strip().replace('[', '').replace(']', '')
                    keys = keys.split(',')
                    for key in keys:
                        key = key.strip()
                        key = key.replace('\'', '').replace('\\', '')
                        vBucketId = VBucketAware._get_vBucket_id(key)
                        errors.append((
                            "Wrong value for key: {0}, VBucketId: {1}".format(
                                key, vBucketId)))
        return errors

    def load_gen_docs(self, server, bucket, generator, kv_store, op_type, exp=0, timeout=None,
                      flag=0, only_store_hash=True, batch_size=1, proxy_client=None, compression=True):
        _task = self.async_load_gen_docs(server, bucket, generator, kv_store, op_type, exp, flag,
                                         only_store_hash=only_store_hash, batch_size=batch_size,
                                         proxy_client=proxy_client, compression=compression)
        return _task.result(timeout)

    def workload(self, server, bucket, kv_store, num_ops, create, read, update, delete, exp, timeout=None,
                 compression=True):
        _task = self.async_workload(server, bucket, kv_store, num_ops, create, read, update,
                                    delete, exp, compression=compression)
        return _task.result(timeout)

    def verify_data(self, server, bucket, kv_store, timeout=None, compression=True):
        _task = self.async_verify_data(server, bucket, kv_store, compression=compression)
        return _task.result(timeout)

    def wait_for_stats(self, servers, bucket, param, stat, comparison, value, timeout=None):
        """Synchronously wait for stats

        Waits for stats to match the criteria passed by the stats variable. See
        couchbase.stats_tool.StatsCommon.build_stat_check(...) for a description o
        the stats structure and how it can be built.

        Parameters:
            servers - The servers to get stats from. Specifying multiple servers will
                cause the result from each server to be added together before
                comparing. ([TestInputServer])
            bucket - The name of the bucket (String)
            param - The stats parameter to use. (String)
            stat - The stat that we want to get the value from. (String)
            comparison - How to compare the stat result to the value specified.
            value - The value to compare to.

        Returns:
            boolean - Whether or not the correct stats state was seen"""
        _task = self.async_wait_for_stats(servers, bucket, param, stat, comparison, value)
        return _task.result(timeout)

    def shutdown(self, force=False):
        self.task_manager.shutdown(force)
        if force:
            print("Cluster instance shutdown with force")

    def async_create_view(self, server, design_doc_name, view, bucket="default", with_query=True,
                          check_replication=False, ddoc_options=None):
        """Asynchronously creates a views in a design doc

        Parameters:
            server - The server to handle create view task. (TestInputServer)
            design_doc_name - Design doc to be created or updated with view(s) being created (String)
            view - The view being created (document.View)
            bucket - The name of the bucket containing items for this view. (String) or (Bucket)
            with_query - Wait indexing to get view query results after creation
            check_replication - Should the test check replication or not (Boolean)
            ddoc_options - DDoc options to define automatic index building (minUpdateChanges, updateInterval ...) (Dict)
        Returns:
            ViewCreateTask - A task future that is a handle to the scheduled task."""
        _task = ViewCreateTask(server, design_doc_name, view, bucket, with_query, check_replication, ddoc_options)
        self.task_manager.schedule(_task)
        return _task

    def create_view(self, server, design_doc_name, view, bucket="default", timeout=None, with_query=True, check_replication=False):
        """Synchronously creates a views in a design doc

        Parameters:
            server - The server to handle create view task. (TestInputServer)
            design_doc_name - Design doc to be created or updated with view(s) being created (String)
            view - The view being created (document.View)
            bucket - The name of the bucket containing items for this view. (String) or (Bucket)
            with_query - Wait indexing to get view query results after creation

        Returns:
            string - revision number of design doc."""
        _task = self.async_create_view(server, design_doc_name, view, bucket, with_query, check_replication)
        return _task.result(timeout)

    def async_delete_view(self, server, design_doc_name, view, bucket="default"):
        """Asynchronously deletes a views in a design doc

        Parameters:
            server - The server to handle delete view task. (TestInputServer)
            design_doc_name - Design doc to be deleted or updated with view(s) being deleted (String)
            view - The view being deleted (document.View)
            bucket - The name of the bucket containing items for this view. (String) or (Bucket)

        Returns:
            ViewDeleteTask - A task future that is a handle to the scheduled task."""
        _task = ViewDeleteTask(server, design_doc_name, view, bucket)
        self.task_manager.schedule(_task)
        return _task

    def delete_view(self, server, design_doc_name, view, bucket="default", timeout=None):
        """Synchronously deletes a views in a design doc

        Parameters:
            server - The server to handle delete view task. (TestInputServer)
            design_doc_name - Design doc to be deleted or updated with view(s) being deleted (String)
            view - The view being deleted (document.View)
            bucket - The name of the bucket containing items for this view. (String) or (Bucket)

        Returns:
            boolean - Whether or not delete view was successful."""
        _task = self.async_delete_view(server, design_doc_name, view, bucket)
        return _task.result(timeout)


    def async_query_view(self, server, design_doc_name, view_name, query,
                         expected_rows=None, bucket="default", retry_time=2):
        """Asynchronously query a views in a design doc

        Parameters:
            server - The server to handle query view task. (TestInputServer)
            design_doc_name - Design doc with view(s) being queried(String)
            view_name - The view being queried (String)
            expected_rows - The number of rows expected to be returned from the query (int)
            bucket - The name of the bucket containing items for this view. (String)
            retry_time - The time in seconds to wait before retrying failed queries (int)

        Returns:
            ViewQueryTask - A task future that is a handle to the scheduled task."""
        _task = ViewQueryTask(server, design_doc_name, view_name, query, expected_rows, bucket, retry_time)
        self.task_manager.schedule(_task)
        return _task

    def query_view(self, server, design_doc_name, view_name, query,
                   expected_rows=None, bucket="default", retry_time=2, timeout=None):
        """Synchronously query a views in a design doc

        Parameters:
            server - The server to handle query view task. (TestInputServer)
            design_doc_name - Design doc with view(s) being queried(String)
            view_name - The view being queried (String)
            expected_rows - The number of rows expected to be returned from the query (int)
            bucket - The name of the bucket containing items for this view. (String)
            retry_time - The time in seconds to wait before retrying failed queries (int)

        Returns:
            ViewQueryTask - A task future that is a handle to the scheduled task."""
        _task = self.async_query_view(server, design_doc_name, view_name, query, expected_rows, bucket, retry_time)
        return _task.result(timeout)


    def modify_fragmentation_config(self, server, config, bucket="default", timeout=None):
        """Synchronously modify fragmentation configuration spec

        Parameters:
            server - The server to handle fragmentation config task. (TestInputServer)
            config - New compaction configuration (dict - see task)
            bucket - The name of the bucket fragementation config applies to. (String)

        Returns:
            boolean - True if config values accepted."""

        _task = ModifyFragmentationConfigTask(server, config, bucket)
        self.task_manager.schedule(_task)
        return _task.result(timeout)

    def async_monitor_active_task(self, servers,
                                  type_task,
                                  target_value,
                                  wait_progress=100,
                                  num_iteration=100,
                                  wait_task=True):
        """Asynchronously monitor active task.

           When active task reached wait_progress this method  will return.

        Parameters:
            servers - list of servers or The server to handle fragmentation config task. (TestInputServer)
            type_task - task type('indexer' , 'bucket_compaction', 'view_compaction' ) (String)
            target_value - target value (for example "_design/ddoc" for indexing, bucket "default"
                for bucket_compaction or "_design/dev_view" for view_compaction) (String)
            wait_progress - expected progress (int)
            num_iteration - failed test if progress is not changed during num iterations(int)
            wait_task - expect to find task in the first attempt(bool)

        Returns:
            list of MonitorActiveTask - A task future that is a handle to the scheduled task."""
        _tasks = []
        if type(servers) != list:
            servers = [servers, ]
        for server in servers:
            _task = MonitorActiveTask(server, type_task, target_value, wait_progress, num_iteration, wait_task)
            self.task_manager.schedule(_task)
            _tasks.append(_task)
        return _tasks

    def async_monitor_view_fragmentation(self, server,
                                         design_doc_name,
                                         fragmentation_value,
                                         bucket="default"):
        """Asynchronously monitor view fragmentation.

           When <fragmentation_value> is reached on the
           index file for <design_doc_name> this method
           will return.

        Parameters:
            server - The server to handle fragmentation config task. (TestInputServer)
            design_doc_name - design doc with views represented in index file. (String)
            fragmentation_value - target amount of fragmentation within index file to detect. (String)
            bucket - The name of the bucket design_doc belongs to. (String)

        Returns:
            MonitorViewFragmentationTask - A task future that is a handle to the scheduled task."""

        _task = MonitorViewFragmentationTask(server, design_doc_name,
                                             fragmentation_value, bucket)
        self.task_manager.schedule(_task)
        return _task

    def async_generate_expected_view_results(self, doc_generators, view,
                                             query):
        """Asynchronously generate expected view query results

        Parameters:
            doc_generators - Generators used for loading docs (DocumentGenerator[])
            view - The view with map function (View)
            query - Query params to filter docs from the generator. (dict)

        Returns:
            GenerateExpectedViewResultsTask - A task future that is a handle to the scheduled task."""

        _task = GenerateExpectedViewResultsTask(doc_generators, view, query)
        self.task_manager.schedule(_task)
        return _task

    def generate_expected_view_query_results(self, doc_generators, view, query,
                                             timeout=None):
        """Synchronously generate expected view query results

        Parameters:
            doc_generators - Generators used for loading docs (DocumentGenerator[])
            view - The view with map function (View)
            query - Query params to filter docs from the generator. (dict)

        Returns:
            list - A list of rows expected to be returned for given query"""

        _task = self.async_generate_expected_view_results(doc_generators, view,
                                                          query)
        return _task.result(timeout)

    def async_monitor_view_query(self, servers, design_doc_name, view_name,
                                 query, expected_docs=None, bucket="default",
                                 retries=100, error=None, verify_rows=False,
                                 server_to_query=0):
        """
        Asynchronously monitor view query results:
        waits for expected rows length match with returned rows length

        Parameters:
            servers - servers to be checked (List of TestInputServer)
            design_doc_name - name of ddoc to query (String)
            view_name - name of view to query (String)
            query - query params (dict)
            expected_docs - expected emitted rows(list)
            bucket - bucket which contains ddoc (String or Bucket)
            retries - how much times it will try to get correct result
            error - for negative tests, expected error raised by query results (String)
            verify_rows - verify values of returned results
            server_to_query - index of server to query (int)
        """
        _task = MonitorViewQueryResultsTask(
            servers, design_doc_name, view_name, query, expected_docs, bucket,
            retries, error, verify_rows, server_to_query)
        self.task_manager.schedule(_task)
        return _task

    def async_n1ql_query_verification(self,
                 server, bucket,
                 query, n1ql_helper = None,
                 expected_result=None,
                 is_explain_query = False,
                 index_name = None,
                 verify_results = True,
                 retry_time=2,
                 scan_consistency = None,
                 scan_vector = None):
        """Asynchronously runs n1ql querya and verifies result if required

        Parameters:
            server - The server to handle query verification task. (TestInputServer)
            query - Query params being used with the query. (dict)
            expected_result - expected result after querying
            is_explain_query - is query explain query
            index_name - index related to query
            bucket - The name of the bucket containing items for this view. (String)
            verify_results -  Verify results after query runs successfully
            retry_time - The time in seconds to wait before retrying failed queries (int)
            n1ql_helper - n1ql helper object
            scan_consistency - consistency value for querying
            scan_vector - scan vector used for consistency
        Returns:
            N1QLQueryTask - A task future that is a handle to the scheduled task."""
        _task = N1QLQueryTask(n1ql_helper = n1ql_helper,
                 server = server, bucket = bucket,
                 query = query, expected_result=expected_result,
                 verify_results = verify_results,
                 is_explain_query = is_explain_query,
                 index_name = index_name,
                 retry_time= retry_time,
                 scan_consistency = scan_consistency,
                 scan_vector = scan_vector)
        self.task_manager.schedule(_task)
        return _task

    def n1ql_query_verification(self,
                 server, bucket,
                 query, n1ql_helper = None,
                 expected_result=None,
                 is_explain_query = False,
                 index_name = None,
                 verify_results = True,
                 scan_consistency = None,
                 scan_vector = None,
                 retry_time=2,
                 timeout = 60):
        """Synchronously runs n1ql querya and verifies result if required

        Parameters:
            server - The server to handle query verification task. (TestInputServer)
            query - Query params being used with the query. (dict)
            expected_result - expected result after querying
            is_explain_query - is query explain query
            index_name - index related to query
            bucket - The name of the bucket containing items for this view. (String)
            verify_results -  Verify results after query runs successfully
            retry_time - The time in seconds to wait before retrying failed queries (int)
            n1ql_helper - n1ql helper object
            scan_consistency - consistency used during querying
            scan_vector - vector used during querying
            timeout - timeout for task
        Returns:
            N1QLQueryTask - A task future that is a handle to the scheduled task."""
        _task = self.async_n1ql_query_verification(n1ql_helper = n1ql_helper,
                 server = server, bucket = bucket,
                 query = query, expected_result=expected_result,
                 is_explain_query = is_explain_query,
                 index_name = index_name,
                 verify_results = verify_results,
                 retry_time= retry_time,
                 scan_consistency = scan_consistency,
                 scan_vector = scan_vector)
        return _task.result(timeout)

    def async_create_index(self,
                 server, bucket,
                 query, n1ql_helper = None,
                 index_name = None,
                 defer_build = False,
                 retry_time=2,
                 timeout = 240):
        """Asynchronously runs create index task

        Parameters:
            server - The server to handle query verification task. (TestInputServer)
            query - Query params being used with the query.
            bucket - The name of the bucket containing items for this view. (String)
            index_name - Name of the index to be created
            defer_build - build is defered
            retry_time - The time in seconds to wait before retrying failed queries (int)
            n1ql_helper - n1ql helper object
            timeout - timeout for index to come online
        Returns:
            CreateIndexTask - A task future that is a handle to the scheduled task."""
        _task = CreateIndexTask(n1ql_helper = n1ql_helper,
                 server = server, bucket = bucket,
                 defer_build = defer_build,
                 index_name = index_name,
                 query = query,
                 retry_time= retry_time,
                 timeout = timeout)
        self.task_manager.schedule(_task)
        return _task

    def async_monitor_index(self,
                 server, bucket, n1ql_helper = None,
                 index_name = None,
                 retry_time=2,
                 timeout = 240):
        """Asynchronously runs create index task

        Parameters:
            server - The server to handle query verification task. (TestInputServer)
            query - Query params being used with the query.
            bucket - The name of the bucket containing items for this view. (String)
            index_name - Name of the index to be created
            retry_time - The time in seconds to wait before retrying failed queries (int)
            timeout - timeout for index to come online
            n1ql_helper - n1ql helper object
        Returns:
            MonitorIndexTask - A task future that is a handle to the scheduled task."""
        _task = MonitorIndexTask(n1ql_helper = n1ql_helper,
                 server = server, bucket = bucket,
                 index_name = index_name,
                 retry_time= retry_time,
                 timeout = timeout)
        self.task_manager.schedule(_task)
        return _task

    def async_build_index(self,
                 server, bucket,
                 query, n1ql_helper = None,
                 retry_time=2):
        """Asynchronously runs create index task

        Parameters:
            server - The server to handle query verification task. (TestInputServer)
            query - Query params being used with the query.
            bucket - The name of the bucket containing items for this view. (String)
            retry_time - The time in seconds to wait before retrying failed queries (int)
            n1ql_helper - n1ql helper object
        Returns:
            BuildIndexTask - A task future that is a handle to the scheduled task."""
        _task = BuildIndexTask(n1ql_helper = n1ql_helper,
                 server = server, bucket = bucket,
                 query = query,
                 retry_time= retry_time)
        self.task_manager.schedule(_task)
        return _task

    def create_index(self,
                 server, bucket,
                 query, n1ql_helper = None,
                 index_name = None,
                 defer_build = False,
                 retry_time=2, timeout= 60):
        """Asynchronously runs drop index task

        Parameters:
            server - The server to handle query verification task. (TestInputServer)
            query - Query params being used with the query.
            bucket - The name of the bucket containing items for this view. (String)
            index_name - Name of the index to be created
            retry_time - The time in seconds to wait before retrying failed queries (int)
            n1ql_helper - n1ql helper object
            defer_build - defer the build
            timeout - timeout for the task
        Returns:
            N1QLQueryTask - A task future that is a handle to the scheduled task."""
        _task = self.async_create_index(n1ql_helper = n1ql_helper,
                 server = server, bucket = bucket,
                 query = query,
                 index_name = index_name,
                 defer_build = defer_build,
                 retry_time= retry_time)
        return _task.result(timeout)

    def async_drop_index(self,
                 server = None, bucket = "default",
                 query = None, n1ql_helper = None,
                 index_name = None,
                 retry_time=2):
        """Synchronously runs drop index task

        Parameters:
            server - The server to handle query verification task. (TestInputServer)
            query - Query params being used with the query.
            bucket - The name of the bucket containing items for this view. (String)
            index_name - Name of the index to be dropped
            retry_time - The time in seconds to wait before retrying failed queries (int)
            n1ql_helper - n1ql helper object
        Returns:
            DropIndexTask - A task future that is a handle to the scheduled task."""
        _task = DropIndexTask(n1ql_helper = n1ql_helper,
                 server = server, bucket = bucket,
                 query = query,
                 index_name = index_name,
                 retry_time= retry_time)
        self.task_manager.schedule(_task)
        return _task


    def drop_index(self,
                 server, bucket,
                 query, n1ql_helper = None,
                 index_name = None,
                 retry_time=2, timeout = 60):
        """Synchronously runs drop index task

        Parameters:
            server - The server to handle query verification task. (TestInputServer)
            query - Query params being used with the query. (dict)
            bucket - The name of the bucket containing items for this view. (String)
            index_name - Name of the index to be created
            retry_time - The time in seconds to wait before retrying failed queries (int)
            n1ql_helper - n1ql helper object
            timeout - timeout for the task
        Returns:
            N1QLQueryTask - A task future that is a handle to the scheduled task."""
        _task = self.async_drop_index(n1ql_helper = n1ql_helper,
                 server = server, bucket = bucket,
                 query = query,
                 index_name = index_name,
                 retry_time= retry_time)
        return _task.result(timeout)

    def async_view_query_verification(self, design_doc_name, view_name, query, expected_rows, num_verified_docs=20, bucket="default", query_timeout=20,
                                      results=None, server=None):
        """Asynchronously query a views in a design doc and does full verification of results

        Parameters:
            server - The server to handle query verification task. (TestInputServer)
            design_doc_name - Design doc with view(s) being queried(String)
            view_name - The view being queried (String)
            query - Query params being used with the query. (dict)
            expected_rows - The number of rows expected to be returned from the query (int)
            num_verified_docs - The number of docs to verify that require memcached gets (int)
            bucket - The name of the bucket containing items for this view. (String)
            query_timeout - The time to allow a query with stale=false to run. (int)
            retry_time - The time in seconds to wait before retrying failed queries (int)
            results - already gotten results to check, if None task will newly get results(dict)

        Returns:
            ViewQueryVerificationTask - A task future that is a handle to the scheduled task."""
        _task = ViewQueryVerificationTask(design_doc_name, view_name, query, expected_rows, server, num_verified_docs, bucket, query_timeout, results=results)
        self.task_manager.schedule(_task)
        return _task

    def view_query_verification(self, server, design_doc_name, view_name, query,
                                expected_rows, num_verified_docs=20,
                                bucket="default", query_timeout=20, timeout=None,
                                results=None):
        """Synchronously query a views in a design doc and does full verification of results

        Parameters:
            server - The server to handle query verification task. (TestInputServer)
            design_doc_name - Design doc with view(s) being queried(String)
            view_name - The view being queried (String)
            query - Query params being used with the query. (dict)
            expected_rows - The number of rows expected to be returned from the query (int)
            num_verified_docs - The number of docs to verify that require memcached gets (int)
            bucket - The name of the bucket containing items for this view. (String)
            query_timeout - The time to allow a query with stale=false to run. (int)
            retry_time - The time in seconds to wait before retrying failed queries (int)
            results - already gotten results to check, if None task will newly get results(dict)

        Returns:
            dict - An object with keys: passed = True or False
                                        errors = reasons why verification failed """
        _task = self.async_view_query_verification(server, design_doc_name, view_name, query, expected_rows, num_verified_docs, bucket, query_timeout, results)
        return _task.result(timeout)


    def monitor_view_fragmentation(self, server,
                                   design_doc_name,
                                   fragmentation_value,
                                   bucket="default",
                                   timeout=None):
        """Synchronously monitor view fragmentation.

           When <fragmentation_value> is reached on the
           index file for <design_doc_name> this method
           will return.

        Parameters:
            server - The server to handle fragmentation config task. (TestInputServer)
            design_doc_name - design doc with views represented in index file. (String)
            fragmentation_value - target amount of fragmentation within index file to detect. (String)
            bucket - The name of the bucket design_doc belongs to. (String)

        Returns:
            boolean - True if <fragmentation_value> reached"""

        _task = self.async_monitor_view_fragmentation(server, design_doc_name,
                                                      fragmentation_value,
                                                      bucket)
        self.task_manager.schedule(_task)
        return _task.result(timeout)

    def async_compact_view(self, server, design_doc_name, bucket="default", with_rebalance=False):
        """Asynchronously run view compaction.

        Compacts index file represented by views within the specified <design_doc_name>

        Parameters:
            server - The server to handle fragmentation config task. (TestInputServer)
            design_doc_name - design doc with views represented in index file. (String)
            bucket - The name of the bucket design_doc belongs to. (String)
            with_rebalance - there are two cases that process this parameter:
                "Error occured reading set_view _info" will be ignored if True
                (This applies to rebalance in case),
                and with concurrent updates(for instance, with rebalance)
                it's possible that compaction value has not changed significantly

        Returns:
            ViewCompactionTask - A task future that is a handle to the scheduled task."""


        _task = ViewCompactionTask(server, design_doc_name, bucket, with_rebalance)
        self.task_manager.schedule(_task)
        return _task

    def compact_view(self, server, design_doc_name, bucket="default", timeout=None, with_rebalance=False):
        """Synchronously run view compaction.

        Compacts index file represented by views within the specified <design_doc_name>

        Parameters:
            server - The server to handle fragmentation config task. (TestInputServer)
            design_doc_name - design doc with views represented in index file. (String)
            bucket - The name of the bucket design_doc belongs to. (String)
            with_rebalance - "Error occured reading set_view _info" will be ignored if True
                and with concurrent updates(for instance, with rebalance)
                it's possible that compaction value has not changed significantly

        Returns:
            boolean - True file size reduced after compaction, False if successful but no work done """

        _task = self.async_compact_view(server, design_doc_name, bucket, with_rebalance)
        return _task.result(timeout)

    def failover(self, servers=[], failover_nodes=[], graceful=False, use_hostnames=False,timeout=None):
        """Synchronously flushes a bucket

        Parameters:
            servers - node used for connection (TestInputServer)
            failover_nodes - servers to be failovered, i.e. removed from the cluster. (TestInputServer)
            bucket - The name of the bucket to be flushed. (String)

        Returns:
            boolean - Whether or not the bucket was flushed."""
        if timeout is None:
            _task = self.async_failover(servers, failover_nodes, graceful, use_hostnames)
        else:
            _task = self.async_failover(servers, failover_nodes, graceful, use_hostnames, timeout)
        return _task.result(timeout)

    def async_bucket_flush(self, server, bucket='default'):
        """Asynchronously flushes a bucket

        Parameters:
            server - The server to flush the bucket on. (TestInputServer)
            bucket - The name of the bucket to be flushed. (String)

        Returns:
            BucketFlushTask - A task future that is a handle to the scheduled task."""
        _task = BucketFlushTask(server, bucket)
        self.task_manager.schedule(_task)
        return _task

    def bucket_flush(self, server, bucket='default', timeout=None):
        """Synchronously flushes a bucket

        Parameters:
            server - The server to flush the bucket on. (TestInputServer)
            bucket - The name of the bucket to be flushed. (String)

        Returns:
            boolean - Whether or not the bucket was flushed."""
        _task = self.async_bucket_flush(server, bucket)
        return _task.result(timeout)



    def async_monitor_db_fragmentation(self, server, fragmentation, bucket, get_view_frag=False):
        """Asyncronously monitor db fragmentation

        Parameters:
            servers - server to check(TestInputServers)
            bucket - bucket to check
            fragmentation - fragmentation to reach
            get_view_frag - Monitor view fragmentation. In case enabled When <fragmentation_value> is reached this method will return (boolean)

        Returns:
            MonitorDBFragmentationTask - A task future that is a handle to the scheduled task"""
        _task = MonitorDBFragmentationTask(server, fragmentation, bucket, get_view_frag)
        self.task_manager.schedule(_task)
        return _task

    def async_monitor_disk_size_fragmentation(self, server, fragmentation, bucket, get_view_frag=False):
        """Asyncronously monitor disk size fragmentation

        Parameters:
            servers - server to check(TestInputServers)
            bucket - bucket to check
            fragmentation - fragmentation to reach
            get_view_frag - Monitor view fragmentation. In case enabled When <fragmentation_value> is reached this method will return (boolean)

        Returns:
            MonitorDiskSizeFragmentationTask - A task future that is a handle to the scheduled task"""
        _task = MonitorDiskSizeFragmentationTask(server, fragmentation, bucket, get_view_frag)
        self.task_manager.schedule(_task)
        return _task

    def cbrecovery(self, src_server, dest_server, bucket_src='', bucket_dest='', username='', password='',
                 username_dest='', password_dest='', verbose=False, wait_completed=True,timeout=None):
        """Synchronously run and monitor cbrecovery

        Parameters:
            src_server - source cluster to restore data from(TestInputServers)
            dest_server - destination cluster to restore data to(TestInputServers)
            bucket_src - source bucket to recover from
            bucket_dest - destination bucket to recover to
            username - REST username for source cluster
            password - REST password for source cluster
            username_dest - REST username for destination cluster or server node
            password_dest - REST password for destination cluster or server node
            verbose - verbose logging; more -v's provide more verbosity
            wait_completed - wait for the end of the cbrecovery

        Returns:
            boolean - Whether or not the cbrecovery completed successfully"""
        _task = self.async_cbrecovery(src_server, dest_server, bucket_src, bucket_dest, username, password,
                 username_dest, password_dest, verbose, wait_completed)
        return _task.result(timeout)

    def async_cbrecovery(self, src_server, dest_server, bucket_src='', bucket_dest='', username='', password='',
                 username_dest='', password_dest='', verbose=False, wait_completed=True):
        """Asyncronously run/monitor cbrecovery

        Parameters:
            src_server - source cluster to restore data from(TestInputServers)
            dest_server - destination cluster to restore data to(TestInputServers)
            bucket_src - source bucket to recover from
            bucket_dest - destination bucket to recover to
            username - REST username for source cluster
            password - REST password for source cluster
            username_dest - REST username for destination cluster or server node
            password_dest - REST password for destination cluster or server node
            verbose - verbose logging; more -v's provide more verbosity
            wait_completed - wait for the end of the cbrecovery

        Returns:
            CBRecoveryTask - A task future that is a handle to the scheduled task"""
        _task = CBRecoveryTask(src_server, dest_server, bucket_src, bucket_dest, username, password,
                 username_dest, password_dest, verbose, wait_completed)
        self.task_manager.schedule(_task)
        return _task

    def async_compact_bucket(self, server, bucket="default"):
        """Asynchronously starts bucket compaction

        Parameters:
            server - source couchbase server
            bucket - bucket to compact

        Returns:
            boolean - Whether or not the compaction started successfully"""
        _task = CompactBucketTask(server, bucket)
        self.task_manager.schedule(_task)
        return _task


    def compact_bucket(self, server, bucket="default"):
        """Synchronously runs bucket compaction and monitors progress

        Parameters:
            server - source couchbase server
            bucket - bucket to compact

        Returns:
            boolean - Whether or not the cbrecovery completed successfully"""
        _task = self.async_compact_bucket(server, bucket)
        status = _task.result()
        return status

    def async_monitor_compact_view(self, server, design_doc_name, bucket="default", with_rebalance=False, frag_value=0):
        """Asynchronously montior view compaction.

        Parameters:
            server - The server to handle fragmentation config task. (TestInputServer)
            design_doc_name - design doc with views represented in index file. (String)
            bucket - The name of the bucket design_doc belongs to. (String)
            with_rebalance - there are two cases that process this parameter:
                "Error occured reading set_view _info" will be ignored if True
                (This applies to rebalance in case),
                and with concurrent updates(for instance, with rebalance)
                it's possible that compaction value has not changed significantly
            frag_value - ViewFragmentationThresholdPercentage set to be compared with fragmentaion value after compaction

        Returns:
            MonitorViewCompactionTask - A task future that is a handle to the scheduled task."""


        _task = MonitorViewCompactionTask(server, design_doc_name, bucket, with_rebalance, frag_value)
        self.task_manager.schedule(_task)
        return _task

    def monitor_compact_view(self, server, design_doc_name, bucket="default", timeout=None, with_rebalance=False, frag_value=0):
        """Synchronously monitor view compaction.

        Parameters:
            server - The server to handle fragmentation config task. (TestInputServer)
            design_doc_name - design doc with views represented in index file. (String)
            bucket - The name of the bucket design_doc belongs to. (String)
            with_rebalance - "Error occured reading set_view _info" will be ignored if True
                and with concurrent updates(for instance, with rebalance)
                it's possible that compaction value has not changed significantly
            frag_value - ViewFragmentationThresholdPercentage set to be compared with fragmentaion value after compaction

        Returns:
            boolean - True file size reduced after compaction, False if successful but no work done """

        _task = self.async_monitor_compact_view(server, design_doc_name, bucket, with_rebalance, frag_value)
        return _task.result(timeout)

    def async_cancel_bucket_compaction(self, server, bucket="default"):
        """Asynchronously starts cancelling bucket compaction

        Parameters:
            server - source couchbase server
            bucket - bucket on which compaction is running

        Returns:
            boolean - Whether or not the compaction cancelled successfully"""
        _task = CancelBucketCompactionTask(server, bucket)
        self.task_manager.schedule(_task)
        return _task

    def cancel_bucket_compaction(self, server, bucket="default"):
        """Synchronously starts cancelling bucket compaction and monitors progress

        Parameters:
            server - source couchbase server
            bucket - bucket on which compaction is running

        Returns:
            boolean - Whether or not the compaction cancelled successfully"""
        _task = self.async_cancel_bucket_compaction(server, bucket)
        status = _task.result()
        return status

    def async_backup_cluster(self, cluster_host, backup_host, directory='', name='',
                             resume=False, purge=False, no_progress_bar=False,
                             cli_command_location='', cb_version=None, num_shards=''):
        """
        Asynchronously starts backup cluster

        :param cluster_host: host to be backed up
        :param backup_host: host where backup happens
        :param directory: backup directory
        :param name: backup name
        :param resume: bool to decide if it is a resume
        :param purge: bool to decide if it is a purge
        :param no_progress_bar: bool to decide progress bar
        :param cli_command_location: command location with respect to os
        :return: task with the output or error message
        """
        _task = EnterpriseBackupTask(cluster_host, backup_host, directory, name, resume,
                                     purge, no_progress_bar, cli_command_location, cb_version,
                                     num_shards)
        self.task_manager.schedule(_task)
        return _task

    def async_restore_cluster(self, restore_host, backup_host, backups=[], start=0, end=0, directory='', name='',
                 force_updates=False, no_progress_bar=False, cli_command_location='', cb_version=None):
        """
        Asynchronously start backup restore
        :param restore_host: cluster to be restored to
        :param backup_host: cluster where backup happens
        :param backups: list of backups available
        :param start: backup start index
        :param end: backup end index
        :param directory: backup directory
        :param name: backup name
        :param force_updates: bool to decide if force_updates
        :param no_progress_bar: bool to decide progress bar
        :param cli_command_location: cli_command_location: command location with respect to os
        :return: task with the output or error message
        """
        _task = EnterpriseRestoreTask(restore_host, backup_host, backups, start, end, directory, name,
                                      force_updates, no_progress_bar, cli_command_location, cb_version)
        self.task_manager.schedule(_task)
        return _task

    def async_merge_cluster(self, backup_host, backups=[], start=0, end=0, directory='', name='',
                            cli_command_location=''):
        """
        Asynchronously start backup merge
        :param backup_host: cluster where backup happens
        :param backups: list of backups available
        :param start: backup start index
        :param end: backup end index
        :param directory: backup directory
        :param name: backup name
        :param no_progress_bar: bool to decide progress bar
        :param cli_command_location: cli_command_location: command location with respect to os
        :return: task with the output or error message
        """
        _task = EnterpriseMergeTask(backup_host, backups, start, end, directory, name,
                                    cli_command_location)
        self.task_manager.schedule(_task)
        return _task

    def async_compact_cluster(self, backup_host, backup_to_compact, backups=[], directory='', name='',
                            cli_command_location=''):
        """
        Asynchronously start backup merge
        :param backup_host: cluster where backup happens
        :param backups: list of backups available
        :param backup_to_compact: backup to be compacted
        :param directory: backup directory
        :param name: backup name
        :param cli_command_location: cli_command_location: command location with respect to os
        :return: task with the output or error message
        """
        _task = EnterpriseCompactTask(backup_host, backup_to_compact, backups, directory, name,
                                    cli_command_location)
        self.task_manager.schedule(_task)
        return _task

    def async_cbas_query_execute(self, server, cbas_endpoint, statement, mode=None, pretty=True):
        """
        Asynchronously execute a CBAS query
        :param server: CB server
        :param cbas_endpoint: CBAS Endpoint URL (/analytics/service)
        :param statement: Query to be executed
        :param mode: Query Execution mode
        :param pretty: Pretty formatting
        :return: task with the output or error message
        """
        _task = CBASQueryExecuteTask(server, cbas_endpoint, statement, mode, pretty)
        self.task_manager.schedule(_task)
        return _task
