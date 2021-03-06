rest_port=8091
ssl_rest_port=18091
capi_port=8092
ssl_capi_port=18092
query_port=8093
ssl_query_port=18093
fts_http_port=8094
fts_ssl_port=18094
cbas_http_port=8095
cbas_ssl_port=18095
eventing_http_port=8096
eventing_ssl_port=18096
indexer_admin_port=9100
indexer_scan_port=9101
indexer_http_port=9102
indexer_stinit_port=9103
indexer_stcatchup_port=9104
indexer_stmaint_port=9105
cbas_admin_port=9110
cbas_cc_http_port=9111
cbas_cc_cluster_port=9112
cbas_cc_client_port=9113
cbas_console_port=9114
cbas_cluster_port=9115
cbas_data_port=9116
cbas_result_port=9117
cbas_messaging_port=9118
cbas_auth_port=9119
cbas_replication_port=9120
cbas_metadata_port=9121
cbas_metadata_callback_port=9122
fts_grpc_port=9130
fts_grpc_ssl_port=19130
eventing_debug_port=9140
xdcr_rest_port=9998
projector_port=9999
memcached_dedicated_port=11209
memcached_port=11210
memcached_ssl_port=11207
default_non_secure_ports={"rest_port" : rest_port, "capi_port" : capi_port, "query_port"
: query_port, "fts_http_port": fts_http_port, "cbas_http_port" : cbas_http_port }
default_secure_ports={"rest_port" : ssl_rest_port, "capi_port":ssl_capi_port,
                      "query_port" : ssl_query_port, "fts_http_port": fts_ssl_port,
                      "cbas_http_port":cbas_ssl_port}