# kubebuilder 实战

## 初始化

```bash
kubebuilder init --domain my.domain
```

## 创建 API

通过 `kubebuilder create api` 命令可以创建一个新的 Kind。

```bash
kubebuilder create api --group webapp --version v1 --kind Guestbook
```

此处创建了一个名为 Guestbook 的 kind。kubebuilder 会创建一个简单的 Guestbook 框架，需要我们在 Spec 与 Status 类型中添加自定义内容来构建 CRD。

```Go
// GuestbookSpec defines the desired state of Guestbook
type GuestbookSpec struct {
	// INSERT ADDITIONAL SPEC FIELDS - desired state of cluster
	// Important: Run "make" to regenerate code after modifying this file

	// Quantity of instances
	// +kubebuilder:validation:Minimum=1
	// +kubebuilder:validation:Maximum=10
	Size int32 `json:"size"`

	// Name of the ConfigMap for GuestbookSpec's configuration
	// +kubebuilder:validation:MaxLength=15
	// +kubebuilder:validation:MinLength=1
	ConfigMapName string `json:"configMapName"`

	// +kubebuilder:validation:Enum=Phone;Address;Name
	Type string `json:"alias,omitempty"`
}

// GuestbookStatus defines the observed state of Guestbook
type GuestbookStatus struct {
	// INSERT ADDITIONAL STATUS FIELD - define observed state of cluster
	// Important: Run "make" to regenerate code after modifying this file

	// PodName of the active Guestbook node.
	Active string `json:"active"`

	// PodNames of the standby Guestbook nodes.
	Standby []string `json:"standby"`
}
```

Spec 和 Status 中可以是 kubernetes 对象，也可以是自定义的数值、字符串对象，还可以是嵌套的另一个 Spec 或 Status 对象。

之后，通过 Spec 与 Status 定义 CRD：

```Go
// Guestbook is the Schema for the guestbooks API
type Guestbook struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   GuestbookSpec   `json:"spec,omitempty"`
	Status GuestbookStatus `json:"status,omitempty"`
}

// +kubebuilder:object:root=true

// GuestbookList contains a list of Guestbook
type GuestbookList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []Guestbook `json:"items"`
}
```

最后，将 CRD 注册到 scheme 中：

```Go
func init() {
	SchemeBuilder.Register(&Guestbook{}, &GuestbookList{})
}
```

使用命令，将自定义的 CRD 安装到当前的 kubernetes 集群中:

```bash
make install
```

使用 describe 命令查看 CRD：

```bash
sheep@sheep:~/workspace/milvus/sheep/kube-example$ kubectl get CustomResourceDefinition
NAME                                 CREATED AT
backups.pingcap.com                  2020-07-24T09:54:12Z
backupschedules.pingcap.com          2020-07-24T09:54:12Z
guestbooks.webapp.my.domain          2020-07-27T02:51:06Z
restores.pingcap.com                 2020-07-24T09:54:12Z
tidbclusterautoscalers.pingcap.com   2020-07-24T09:54:12Z
tidbclusters.pingcap.com             2020-07-24T09:54:12Z
tidbinitializers.pingcap.com         2020-07-24T09:54:12Z
tidbmonitors.pingcap.com             2020-07-24T09:54:12Z
```

创建 CRD 的一个实例并 apply 到 kubernetes 集群中，使用 describe 查看：

```bash
sheep@sheep:~/workspace/milvus/sheep/kube-example$ kubectl describe Guestbook guestbook-sample
Name:         guestbook-sample
Namespace:    default
Labels:       <none>
Annotations:  API Version:  webapp.my.domain/v1
Kind:         Guestbook
Metadata:
  Creation Timestamp:  2020-07-27T03:29:10Z
  Generation:          1
  Managed Fields:
    API Version:  webapp.my.domain/v1
    Fields Type:  FieldsV1
    fieldsV1:
      f:metadata:
        f:annotations:
          .:
          f:kubectl.kubernetes.io/last-applied-configuration:
      f:spec:
        .:
        f:configMapName:
        f:size:
        f:type:
    Manager:         kubectl
    Operation:       Update
    Time:            2020-07-27T03:29:10Z
  Resource Version:  387578
  Self Link:         /apis/webapp.my.domain/v1/namespaces/default/guestbooks/guestbook-sample
  UID:               bdcfd527-0864-4d69-850d-7b81972fb91d
Spec:
  Config Map Name:  bookA
  Size:             5
  Type:             Atype
Events:             <none>
```

## 控制器

控制器是 kubernetes 的核心，也是 operator 的核心。控制器用于保证所有的对象的状态与期望的状态想匹配。该过程称为 **reconciling**。

用于保证 reconciling 的所有逻辑都被定义在 **Reconciler** 中。每个 Reconciler 都包含两个元素：期望状态所包含的对象、是否需要重新 reconciling 的 bool 值。

一个控制器与一个 kind 相对应。

### Reconciler

kubebuilder 会为我们搭建一个基础的 reconciler，包含一个 client，一个 logger以及一个 scheme：

```Go
// GuestbookReconciler reconciles a Guestbook object
type GuestbookReconciler struct {
	client.Client
	Log    logr.Logger
	Scheme *runtime.Scheme
}
```

### Reconcile

Reconcile 是 Reconciler 最主要的一个函数。通过返回空结果来表示已经完成 reconciling。

```Go
func (r *GuestbookReconciler) Reconcile(req ctrl.Request) (ctrl.Result, error) {
	_ = context.Background()
	_ = r.Log.WithValues("guestbook", req.NamespacedName)

	// your logic here

	return ctrl.Result{}, nil
}
```

### SetupWithManager

SetupWithManager 也是 Reconciler 的一个函数，用于将当前的 Reconciler 添加到 manager 中，当 manager 启动时该函数被调用。

```Go
func (r *GuestbookReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&webappv1.Guestbook{}).
		Complete(r)
}
```