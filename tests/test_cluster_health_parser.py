import unittest

from prometheus_es_exporter.cluster_health_parser import parse_response
from tests.utils import convert_result


# Sample responses generated by querying the endpoint on a Elasticsearch
# server populated with the following data (http command = Httpie utility):
# > http -v POST localhost:9200/foo/bar/1 val:=1 group1=a group2=a
# > http -v POST localhost:9200/foo/bar/2 val:=2 group1=a group2=b
# > http -v POST localhost:9200/foo/bar/3 val:=3 group1=b group2=b
class Test(unittest.TestCase):
    maxDiff = None

    def test_endpoint(self):
        # Endpoint: /_cluster/health?pretty&level=shards
        response = {
            'cluster_name': 'elasticsearch',
            'status': 'yellow',
            'timed_out': False,
            'number_of_nodes': 1,
            'number_of_data_nodes': 1,
            'active_primary_shards': 5,
            'active_shards': 5,
            'relocating_shards': 0,
            'initializing_shards': 0,
            'unassigned_shards': 5,
            'delayed_unassigned_shards': 0,
            'number_of_pending_tasks': 0,
            'number_of_in_flight_fetch': 0,
            'task_max_waiting_in_queue_millis': 0,
            'active_shards_percent_as_number': 50.0,
            'indices': {
                'foo': {
                    'status': 'yellow',
                    'number_of_shards': 5,
                    'number_of_replicas': 1,
                    'active_primary_shards': 5,
                    'active_shards': 5,
                    'relocating_shards': 0,
                    'initializing_shards': 0,
                    'unassigned_shards': 5,
                    'shards': {
                        '0': {
                            'status': 'yellow',
                            'primary_active': True,
                            'active_shards': 1,
                            'relocating_shards': 0,
                            'initializing_shards': 0,
                            'unassigned_shards': 1
                        },
                        '1': {
                            'status': 'yellow',
                            'primary_active': True,
                            'active_shards': 1,
                            'relocating_shards': 0,
                            'initializing_shards': 0,
                            'unassigned_shards': 1
                        },
                        '2': {
                            'status': 'yellow',
                            'primary_active': True,
                            'active_shards': 1,
                            'relocating_shards': 0,
                            'initializing_shards': 0,
                            'unassigned_shards': 1
                        },
                        '3': {
                            'status': 'yellow',
                            'primary_active': True,
                            'active_shards': 1,
                            'relocating_shards': 0,
                            'initializing_shards': 0,
                            'unassigned_shards': 1
                        },
                        '4': {
                            'status': 'yellow',
                            'primary_active': True,
                            'active_shards': 1,
                            'relocating_shards': 0,
                            'initializing_shards': 0,
                            'unassigned_shards': 1
                        }
                    }
                }
            }
        }

        expected = {
            'status': 1,
            'number_of_nodes': 1,
            'number_of_data_nodes': 1,
            'active_primary_shards': 5,
            'active_shards': 5,
            'relocating_shards': 0,
            'initializing_shards': 0,
            'unassigned_shards': 5,
            'delayed_unassigned_shards': 0,
            'number_of_pending_tasks': 0,
            'number_of_in_flight_fetch': 0,
            'task_max_waiting_in_queue_millis': 0,
            'active_shards_percent_as_number': 50.0,
            'indices_status{index="foo"}': 1,
            'indices_number_of_shards{index="foo"}': 5,
            'indices_number_of_replicas{index="foo"}': 1,
            'indices_active_primary_shards{index="foo"}': 5,
            'indices_active_shards{index="foo"}': 5,
            'indices_relocating_shards{index="foo"}': 0,
            'indices_initializing_shards{index="foo"}': 0,
            'indices_unassigned_shards{index="foo"}': 5,
            'indices_shards_status{index="foo",shard="0"}': 1,
            'indices_shards_primary_active{index="foo",shard="0"}': 1,
            'indices_shards_active_shards{index="foo",shard="0"}': 1,
            'indices_shards_relocating_shards{index="foo",shard="0"}': 0,
            'indices_shards_initializing_shards{index="foo",shard="0"}': 0,
            'indices_shards_unassigned_shards{index="foo",shard="0"}': 1,
            'indices_shards_status{index="foo",shard="1"}': 1,
            'indices_shards_primary_active{index="foo",shard="1"}': 1,
            'indices_shards_active_shards{index="foo",shard="1"}': 1,
            'indices_shards_relocating_shards{index="foo",shard="1"}': 0,
            'indices_shards_initializing_shards{index="foo",shard="1"}': 0,
            'indices_shards_unassigned_shards{index="foo",shard="1"}': 1,
            'indices_shards_status{index="foo",shard="2"}': 1,
            'indices_shards_primary_active{index="foo",shard="2"}': 1,
            'indices_shards_active_shards{index="foo",shard="2"}': 1,
            'indices_shards_relocating_shards{index="foo",shard="2"}': 0,
            'indices_shards_initializing_shards{index="foo",shard="2"}': 0,
            'indices_shards_unassigned_shards{index="foo",shard="2"}': 1,
            'indices_shards_status{index="foo",shard="3"}': 1,
            'indices_shards_primary_active{index="foo",shard="3"}': 1,
            'indices_shards_active_shards{index="foo",shard="3"}': 1,
            'indices_shards_relocating_shards{index="foo",shard="3"}': 0,
            'indices_shards_initializing_shards{index="foo",shard="3"}': 0,
            'indices_shards_unassigned_shards{index="foo",shard="3"}': 1,
            'indices_shards_status{index="foo",shard="4"}': 1,
            'indices_shards_primary_active{index="foo",shard="4"}': 1,
            'indices_shards_active_shards{index="foo",shard="4"}': 1,
            'indices_shards_relocating_shards{index="foo",shard="4"}': 0,
            'indices_shards_initializing_shards{index="foo",shard="4"}': 0,
            'indices_shards_unassigned_shards{index="foo",shard="4"}': 1,
        }
        result = convert_result(parse_response(response))
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
