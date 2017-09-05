# vCloud CLI 0.1
#
# Copyright (c) 2014 VMware, Inc. All Rights Reserved.
#
# This product is licensed to you under the
# Apache License, Version 2.0 (the "License").
# You may not use this product except in compliance with the License.
#
# This product may include a number of subcomponents with
# separate copyright notices and license terms. Your use of the source
# code for the these subcomponents is subject to the terms and
# conditions of the subcomponent's license, as noted in the LICENSE file.
#

import click
from pyvcloud.vcd.cluster import Cluster
from subprocess import call
from vcd_cli.utils import restore_session
from vcd_cli.utils import stderr
from vcd_cli.utils import stdout
from vcd_cli.vcd import abort_if_false
from vcd_cli.vcd import cli


@cli.group(short_help='manage clusters')
@click.pass_context
def cluster(ctx):
    """Work with kubernetes clusters in vCloud Director.

\b
    Examples
        vcd cluster list
            Get list of kubernetes clusters in current virtual datacenter.
\b
        vcd cluster create k8s-cluster --nodes 2
            Create a kubernetes cluster in current virtual datacenter.
\b
        vcd cluster delete 692a7b81-bb75-44cf-9070-523a4b304733
            Deletes a kubernetes cluster by id.
    """  # NOQA
    if ctx.invoked_subcommand is not None:
        try:
            restore_session(ctx)
            if not ctx.obj['profiles'].get('vdc_in_use') or \
               not ctx.obj['profiles'].get('vdc_href'):
                raise Exception('select a virtual datacenter')
        except Exception as e:
            stderr(e, ctx)


@cluster.command(short_help='list clusters')
@click.pass_context
def list(ctx):
    try:
        client = ctx.obj['client']
        cluster = Cluster(client)
        result = []
        clusters = cluster.get_clusters()
        for c in clusters:
            result.append({'name': c['name'],
                           'IP master': c['leader_endpoint'],
                           'nodes': len(c['nodes']),
                           'vdc': c['vdc_name']
                           })
        stdout(result, ctx, show_id=True)
    except Exception as e:
        stderr(e, ctx)


@cluster.command(short_help='create cluster')
@click.pass_context
@click.argument('name',
                metavar='<name>',
                required=True)
@click.option('-N',
              '--nodes',
              'node_count',
              required=False,
              default=2,
              metavar='<nodes>',
              help='Number of nodes to create')
@click.option('-n',
              '--network',
              'network_name',
              default=None,
              required=False,
              metavar='<network>',
              help='Network name')
@click.option('-w',
              '--wait',
              'wait',
              is_flag=True,
              default=False,
              required=False,
              help='Wait until finish')
def create(ctx, name, node_count, network_name, wait):
    try:
        client = ctx.obj['client']
        cluster = Cluster(client)
        result = cluster.create_cluster(
                    ctx.obj['profiles'].get('vdc_in_use'),
                    network_name,
                    name,
                    node_count)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@cluster.command(short_help='delete cluster')
@click.pass_context
@click.argument('name',
                metavar='<name>',
                required=True)
@click.option('-y',
              '--yes',
              is_flag=True,
              callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to delete the cluster?')
def delete(ctx, name):
    try:
        client = ctx.obj['client']
        cluster = Cluster(client)
        result = cluster.delete_cluster(name)
        stdout(result, ctx)
    except Exception as e:
        stderr(e, ctx)


@cluster.command(short_help='get cluster config')
@click.pass_context
@click.argument('name',
                metavar='<name>',
                required=True)
def config(ctx, name):
    try:
        client = ctx.obj['client']
        cluster = Cluster(client)
        click.secho(cluster.get_config(name))
    except Exception as e:
        stderr(e, ctx)


@cluster.command(short_help='script to initialize helm')
@click.pass_context
def helm_init(ctx):
  try:
    client = ctx.obj['client']
    cluster = Cluster(client)
    click.secho(cluster.get_helm_script())
  except Exception as e:
    stderr(e, ctx)


@cluster.command(short_help='chart list')
@click.pass_context
def helm_help(ctx):
  text =  """stable and incubator chart list
incubator/
cassandra         check-mk     docker-registry
elasticsearch     etcd         gogs
istio             kafka        kube-registry-proxy
patroni           redis-cache  spring-cloud-data-flow
tensorflow-inception           zookeeper

stable/
acs-engine-autoscaler artifactory        aws-cluster-autoscaler centrifugo 
chaoskube             chronograf         cluster-autoscaler     cockroachdb
concourse             consul             coredns                coscale
dask-distributed      datadog            dokuwiki               drupal
etcd-operator         external-dns       factorio               fluent-bit
g2                    gcloud-endpoints   gcloud-sqlproxy        ghost
gitlab-ce             gitlab-ee          grafana                heapster
influxdb              ipfs               jasperreports          jenkins
joomla                kapacitor          keel                   kube-lego
kube-ops-view         kube-state-metrics kube2iam               kubernetes-dashboard
linkerd               locust             magento                mailhog
mariadb               mediawiki          memcached              metabase
minecraft             minio              mongodb-replicaset     mongodb
moodle                mysql              namerd                 nginx-ingress
nginx-lego            odoo               opencart               openvpn
orangehrm             osclass            owncloud               parse
percona               phabricator        phpbb                  postgresql
prestashop            prometheus         rabbitmq               redis
redmine               rethinkdb          risk-advisor           rocketchat
sapho                 selenium           sensu                  sentry
spark                 spartakus          spinnaker              spotify-docker-gc
stash                 sugarcrm           suitecrm               sumokube
sumologic-fluentd     sysdig             telegraf               testlink
traefik               uchiwa             voyager                weave-cloud
wordpress             zetcd

Example: vcd cluster helm_create zetcd 

    """  
  print(text)

  
@cluster.command(short_help='create chart')
@click.pass_context
@click.argument('name',
                metavar='<name>',
                required=True)
def helm_create(ctx, name):
  chart = 'stable/%s' % (name)
  call('helm install %s' % (chart), shell=True)


@cluster.command(short_help='list deployments')
@click.pass_context
def helm_list(ctx):
  call('helm list', shell=True)


@cluster.command(short_help='delete chart from kubernetes')
@click.pass_context
@click.argument('name',
                metavar='<name>',
                required=True)
def helm_delete(ctx, name):
  call('helm delete %s' % name , shell=True)
