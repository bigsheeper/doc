# Pulsar Authentication & Authorization

Pulsar 的安全性主要由 Authentication（认证）与 Authorization（授权）来保证。默认情况下，Pulsar 不设置任何认证与授权，即任何客户端都可以使用 URL 进行访问。Pulsar 认证与授权都是插件的机制，认证用于控制哪些用户可以访问集群，授权用于控制访问集群的用户可以进行哪些操作，如发布、订阅消息、创建租户等。

## 初始化 Pulsar Standalone

使用如下命令初始化 standalone，该命令会自动创建一个 `persistent://public/default` namespace：

```bash
$ bin/pulsar standalone
```

## 创建密钥

使用如下命令创建密钥，将其保存至 `/tmp/my-secret.key` 文件中：

```bash
$ bin/pulsar tokens create-secret-key --output /tmp/my-secret.key
```

## 使用密钥创建超级用户

超级用户拥有所有的管理权限，并能够直接发布、订阅所有的 topic。使用如下命令创建超级用户 `admin`，并返回对应的 token：

```bash
$ bin/pulsar tokens create --secret-key file:///tmp/my-secret.key --subject admin
# 输出 token：`eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiJ9.Sc_YVn5a0-8j-Z-8HVmqlmhIewzlK-y1H0IS5t5OgRs`
```

## 超级用户配置

### 配置 Standalone

在 `conf/standalone.conf` 中启用认证与授权，指定认证方式为 token，并配置密钥路径：

```conf
# Configuration to enable authentication and authorization
authenticationEnabled=true
authorizationEnabled=true
authenticationProviders=org.apache.pulsar.broker.authentication.AuthenticationProviderToken

# If using secret key
tokenSecretKey=file:///tmp/my-secret.key
# The key can also be passed inline:
# tokenSecretKey=data:;base64,FLFyW0oLJ2Fi22KKCm21J18mbAdztfSHN/lAT5ucEKU=
```

在 `conf/standalone.conf` 中将 `admin` 指定为超级用户：

```conf
# Role names that are treated as "super-user", meaning they will be able to do all admin
# operations and publish/consume from all topics
superUserRoles=admin
```

### 配置 Client

在 `conf/client.conf` 中配置 client，给 `pulsar-admin` 工具赋予超级用户权限，将认证方式指定为 token，并添加创建超级用户时返回的 token：

```conf
# Authentication plugin to authenticate with servers
# e.g. for TLS
# authPlugin=org.apache.pulsar.client.impl.auth.AuthenticationTls
# authPlugin=org.apache.pulsar.client.impl.auth.AuthenticationToken
authPlugin=org.apache.pulsar.client.impl.auth.AuthenticationToken

# Parameters passed to authentication plugin.
# A comma separated list of key:value pairs.
# Keys depend on the configured authPlugin.
# e.g. for TLS
# authParams=tlsCertFile:/path/to/client-cert.pem,tlsKeyFile:/path/to/client-key.pem
# authParams=file:///home/sheep/pulsar/token.txt
authParams=token:eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiJ9.Sc_YVn5a0-8j-Z-8HVmqlmhIewzlK-y1H0IS5t5OgRs
```

## 重启 Pulsar Standalone

在原来的 standalone 终端中使用 `ctrl+c` 进行关闭，再使用如下命令启动 pulsar standalone：

```bash
$ bin/pulsar standalone -nfw -nss
```

## 使用密钥创建普通用户

创建一个普通用户 `user-1`，默认该用户没有权限执行任何操作：

```bash
$ bin/pulsar tokens create --secret-key file:///tmp/my-secret.key --subject user-1
# 输出 token：`eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyLTEifQ.bUoFd36kmcAadVX7HpP2UDwx7QMnMdz0ZD05ntjZQto`
```

## 对普通用户授权

为用户 `user-1` 授予发布、订阅消息的权限，且仅限于对 `public/default` namespace：

```bash
$ bin/pulsar-admin namespaces grant-permission public/default --role user-1 --actions produce,consume
```

## 使用 python client 发布、订阅消息

对 client 进行认证，在创建 client 时，在 `AuthenticationToken` 类中添加用户 `user-1` 对应的 token。

完整发布消息代码如下：

```python
import pulsar
from pulsar import Client, AuthenticationToken

def produce_test(key):
    client = pulsar.Client('pulsar://localhost:6650', authentication=AuthenticationToken('eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyLTEifQ.bUoFd36kmcAadVX7HpP2UDwx7QMnMdz0ZD05ntjZQto'))
    producer = client.create_producer(key)

    s = "from-"+key+",message:"

    producer.send((s + "aaaaa").encode('utf-8'), partition_key=key)
    producer.send((s + "bbbbb").encode('utf-8'), partition_key=key)
    producer.send((s + "ccccc").encode('utf-8'), partition_key=key)

    client.close()

produce_test("persistent://public/default/topic0")
```

完整订阅消息代码如下：

```python
import pulsar
from pulsar import Client, AuthenticationToken
from _pulsar import ConsumerType

def consumer_data(partition):
    client = pulsar.Client('pulsar://localhost:6650', authentication=AuthenticationToken('eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyLTEifQ.bUoFd36kmcAadVX7HpP2UDwx7QMnMdz0ZD05ntjZQto'))
    consumer = client.subscribe(topic=partition, subscription_name=partition,
                                consumer_type=ConsumerType.Shared)

    while True:
        msg = consumer.receive()
        try:
            print("Received message '{}' id='{}'".format(msg.data(), msg.message_id()))
            # Acknowledge successful processing of the message
            consumer.acknowledge(msg)
        except:
            # Message failed to be processed
            consumer.negative_acknowledge(msg)

    client.close()

consumer_data("persistent://public/default/topic0")
```

## 参考链接

<https://pulsar.apache.org/docs/en/security-jwt/>

<https://pulsar.apache.org/docs/en/security-authorization/>

<https://github.com/apache/pulsar/issues/6309>

<https://mp.weixin.qq.com/s?__biz=MzUxOTc4NDc2MQ==&mid=2247485008&amp;idx=1&amp;sn=e4c7ae95266bfbcbb048a4e4c73319da&source=41#wechat_redirect>
