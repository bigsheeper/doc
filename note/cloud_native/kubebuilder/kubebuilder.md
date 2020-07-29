# Kubebuilder

## 核心概念

### Group、Version、Kinds、Resources

Group：API 功能的集合。

Version: Group 的版本，用于 API 的演进。

Kinds： API GroupVersion 的类型。

Resources： Kind 的对象标识; 在 CRD 中，Kinds 与 Resources 是一对一的。

### Scheme

用于提供 kinds 与 Go types 的映射，每一组 Controller 都需要一个 scheme。

### Informer

主要用于获取 kubernetes 的对象。

### Reconcile

用于实现 Spec 与 Status 相匹配。

### Controller

Kubebuidler 为我们生成的脚手架文件，我们只需要实现 Reconcile 方法即可。

### Cache

Kubebuilder 的核心组件，负责在 Controller 进程里面根据 Scheme 同步 Api Server 中所有该 Controller 关心 GVKs 的 GVRs，其核心是 GVK -> Informer 的映射，Informer 会负责监听对应 GVK 的 GVRs 的创建/删除/更新操作，以触发 Controller 的 Reconcile 逻辑。

### Clients

在实现 Controller 的时候不可避免地需要对某些资源类型进行创建/删除/更新，就是通过该 Clients 实现的，其中查询功能实际查询是本地的 Cache，写操作直接访问 Api Server。

### Manager

Kubebuilder 的核心组件，用于：

- 负责运行所有的 Controllers;
- 初始化共享 caches，包含 listAndWatch 功能;
- 初始化 clients 用于与 Api Server 通信。

### OwnerReference

K8s GC 在删除一个对象时，任何 ownerReference 是该对象的对象都会被清除，与此同时，Kubebuidler 支持所有对象的变更都会触发 Owner 对象 controller 的 Reconcile 方法。

## 创建 API

通过 `kubebuilder create api` 命令可以创建一个新的 Kind。

```bash
kubebuilder create api --group batch --version v1 --kind CronJob
```

此处创建了一个名为 Guestbook 的 kind。kubebuilder 会创建一个简单的 Guestbook 框架，需要我们在 Spec 与 Status 类型中添加自定义内容来构建 CRD。

```Go
// CronJobSpec defines the desired state of CronJob
type CronJobSpec struct {
    // INSERT ADDITIONAL SPEC FIELDS - desired state of cluster
    // Important: Run "make" to regenerate code after modifying this file
}

// CronJobStatus defines the observed state of CronJob
type CronJobStatus struct {
    // INSERT ADDITIONAL STATUS FIELD - define observed state of cluster
    // Important: Run "make" to regenerate code after modifying this file
}
```

Spec 和 Status 中可以是 kubernetes 对象，也可以是自定义的数值、字符串对象，还可以是嵌套的另一个 Spec 或 Status 对象。

之后，通过 Spec 与 Status 定义 CRD：

```Go
// +kubebuilder:object:root=true

// CronJob is the Schema for the cronjobs API
type CronJob struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata,omitempty"`

    Spec   CronJobSpec   `json:"spec,omitempty"`
    Status CronJobStatus `json:"status,omitempty"`
}

// +kubebuilder:object:root=true

// CronJobList contains a list of CronJob
type CronJobList struct {
    metav1.TypeMeta `json:",inline"`
    metav1.ListMeta `json:"metadata,omitempty"`
    Items           []CronJob `json:"items"`
}
```

最后，将 CRD 注册到 scheme 中：

```Go
func init() {
    SchemeBuilder.Register(&CronJob{}, &CronJobList{})
}
```

## 控制器

控制器是 kubernetes 的核心，也是 operator 的核心。控制器用于保证所有的对象的状态与期望的状态想匹配。该过程称为 **reconciling**。

用于保证 reconciling 的所有逻辑都被定义在 **Reconciler** 中。每个 Reconciler 都包含两个元素：期望状态所包含的对象、是否需要重新 reconciling 的 bool 值。

一个控制器与一个 kind 相对应。

### Reconciler

kubebuilder 会为我们搭建一个基础的 reconciler，包含一个 client，一个 logger以及一个 scheme：

```Go
// CronJobReconciler reconciles a CronJob object
type CronJobReconciler struct {
    client.Client
    Log    logr.Logger
    Scheme *runtime.Scheme
}
```

### 访问授权

在 Kubernetes 中，授权有 ABAC（基于属性的访问控制）、RBAC（基于角色的访问控制）、Webhook、Node、AlwaysDeny（一直拒绝）和 AlwaysAllow（一直允许）这6种模式。

我们需要赋予控制器能够在集群中运行的门槛权限，该权限赋予通过 controller-tools 注释实现：

```Go
// +kubebuilder:rbac:groups=batch.tutorial.kubebuilder.io,resources=cronjobs,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=batch.tutorial.kubebuilder.io,resources=cronjobs/status,verbs=get;update;patch
```

### Reconcile

Reconcile 是 Reconciler 的一个函数。通过 Reconciler 中的 client 可以获取 cache 中的对象（此处仅仅用到了 Reconciler 的 log），通过返回空结果来表示已经完成 reconciling。

context 是所有 client 方法中的第一个参数，用于取消请求和追踪等操作。

```Go
func (r *CronJobReconciler) Reconcile(req ctrl.Request) (ctrl.Result, error) {
    _ = context.Background()
    _ = r.Log.WithValues("cronjob", req.NamespacedName)

    // your logic here

    return ctrl.Result{}, nil
}
```

### SetupWithManager

SetupWithManager 也是 Reconciler 的一个函数，用于将当前的 Reconciler 添加到 manager 中，当 manager 启动时该函数被调用。

```Go
func (r *CronJobReconciler) SetupWithManager(mgr ctrl.Manager) error {
    return ctrl.NewControllerManagedBy(mgr).
        For(&batchv1.CronJob{}).
        Complete(r)
}
```

## 示例

### API

#### CronJob

```Go
// CronJobSpec defines the desired state of CronJob
type CronJobSpec struct {
	// +kubebuilder:validation:MinLength=0

	// The schedule in Cron format, see https://en.wikipedia.org/wiki/Cron.
	Schedule string `json:"schedule"`

	// +kubebuilder:validation:Minimum=0

	// Optional deadline in seconds for starting the job if it misses scheduled
	// time for any reason.  Missed jobs executions will be counted as failed ones.
	// +optional
	StartingDeadlineSeconds *int64 `json:"startingDeadlineSeconds,omitempty"`

	// Specifies how to treat concurrent executions of a Job.
	// Valid values are:
	// - "Allow" (default): allows CronJobs to run concurrently;
	// - "Forbid": forbids concurrent runs, skipping next run if previous run hasn't finished yet;
	// - "Replace": cancels currently running job and replaces it with a new one
	// +optional
	ConcurrencyPolicy ConcurrencyPolicy `json:"concurrencyPolicy,omitempty"`

	// This flag tells the controller to suspend subsequent executions, it does
	// not apply to already started executions.  Defaults to false.
	// +optional
	Suspend *bool `json:"suspend,omitempty"`

	// Specifies the job that will be created when executing a CronJob.
	JobTemplate batchv1beta1.JobTemplateSpec `json:"jobTemplate"`

	// +kubebuilder:validation:Minimum=0

	// The number of successful finished jobs to retain.
	// This is a pointer to distinguish between explicit zero and not specified.
	// +optional
	SuccessfulJobsHistoryLimit *int32 `json:"successfulJobsHistoryLimit,omitempty"`

	// +kubebuilder:validation:Minimum=0

	// The number of failed finished jobs to retain.
	// This is a pointer to distinguish between explicit zero and not specified.
	// +optional
	FailedJobsHistoryLimit *int32 `json:"failedJobsHistoryLimit,omitempty"`
}

/*
We define a custom type to hold our concurrency policy.  It's actually
just a string under the hood, but the type gives extra documentation,
and allows us to attach validation on the type instead of the field,
making the validation more easily reusable.
*/

// ConcurrencyPolicy describes how the job will be handled.
// Only one of the following concurrent policies may be specified.
// If none of the following policies is specified, the default one
// is AllowConcurrent.
// +kubebuilder:validation:Enum=Allow;Forbid;Replace
type ConcurrencyPolicy string

const (
	// AllowConcurrent allows CronJobs to run concurrently.
	AllowConcurrent ConcurrencyPolicy = "Allow"

	// ForbidConcurrent forbids concurrent runs, skipping next run if previous
	// hasn't finished yet.
	ForbidConcurrent ConcurrencyPolicy = "Forbid"

	// ReplaceConcurrent cancels currently running job and replaces it with a new one.
	ReplaceConcurrent ConcurrencyPolicy = "Replace"
)

/*
Next, let's design our status, which holds observed state.  It contains any information
we want users or other controllers to be able to easily obtain.

We'll keep a list of actively running jobs, as well as the last time that we successfully
ran our job.  Notice that we use `metav1.Time` instead of `time.Time` to get the stable
serialization, as mentioned above.
*/

// CronJobStatus defines the observed state of CronJob
type CronJobStatus struct {
	// INSERT ADDITIONAL STATUS FIELD - define observed state of cluster
	// Important: Run "make" to regenerate code after modifying this file

	// A list of pointers to currently running jobs.
	// +optional
	Active []corev1.ObjectReference `json:"active,omitempty"`

	// Information when was the last time the job was successfully scheduled.
	// +optional
	LastScheduleTime *metav1.Time `json:"lastScheduleTime,omitempty"`
}
```

#### TiDBCluster

```Go
// +k8s:openapi-gen=true
// TidbClusterSpec describes the attributes that a user creates on a tidb cluster
type TidbClusterSpec struct {
	// Discovery spec
	Discovery DiscoverySpec `json:"discovery,omitempty"`

	// PD cluster spec
	PD PDSpec `json:"pd"`

	// TiDB cluster spec
	TiDB TiDBSpec `json:"tidb"`

	// TiKV cluster spec
	TiKV TiKVSpec `json:"tikv"`

	// TiFlash cluster spec
	// +optional
	TiFlash *TiFlashSpec `json:"tiflash,omitempty"`

	// TiCDC cluster spec
	// +optional
	TiCDC *TiCDCSpec `json:"ticdc,omitempty"`

	// Pump cluster spec
	// +optional
	Pump *PumpSpec `json:"pump,omitempty"`

	// Helper spec
	// +optional
	Helper *HelperSpec `json:"helper,omitempty"`

	// Indicates that the tidb cluster is paused and will not be processed by
	// the controller.
	// +optional
	Paused bool `json:"paused,omitempty"`

	// TODO: remove optional after defaulting logic introduced
	// TiDB cluster version
	// +optional
	Version string `json:"version"`

	// SchedulerName of TiDB cluster Pods
	// +kubebuilder:default=tidb-scheduler
	SchedulerName string `json:"schedulerName,omitempty"`

	// Persistent volume reclaim policy applied to the PVs that consumed by TiDB cluster
	// +kubebuilder:default=Retain
	PVReclaimPolicy *corev1.PersistentVolumeReclaimPolicy `json:"pvReclaimPolicy,omitempty"`

	// ImagePullPolicy of TiDB cluster Pods
	// +kubebuilder:default=IfNotPresent
	ImagePullPolicy corev1.PullPolicy `json:"imagePullPolicy,omitempty"`

	// ImagePullSecrets is an optional list of references to secrets in the same namespace to use for pulling any of the images.
	// +optional
	ImagePullSecrets []corev1.LocalObjectReference `json:"imagePullSecrets,omitempty"`

	// ConfigUpdateStrategy determines how the configuration change is applied to the cluster.
	// UpdateStrategyInPlace will update the ConfigMap of configuration in-place and an extra rolling-update of the
	// cluster component is needed to reload the configuration change.
	// UpdateStrategyRollingUpdate will create a new ConfigMap with the new configuration and rolling-update the
	// related components to use the new ConfigMap, that is, the new configuration will be applied automatically.
	// +kubebuilder:validation:Enum=InPlace,RollingUpdate
	// +kubebuilder:default=InPlacne
	ConfigUpdateStrategy ConfigUpdateStrategy `json:"configUpdateStrategy,omitempty"`

	// Whether enable PVC reclaim for orphan PVC left by statefulset scale-in
	// Optional: Defaults to false
	// +optional
	EnablePVReclaim *bool `json:"enablePVReclaim,omitempty"`

	// Whether enable the TLS connection between TiDB server components
	// Optional: Defaults to nil
	// +optional
	TLSCluster *TLSCluster `json:"tlsCluster,omitempty"`

	// Whether Hostnetwork is enabled for TiDB cluster Pods
	// Optional: Defaults to false
	// +optional
	HostNetwork *bool `json:"hostNetwork,omitempty"`

	// Affinity of TiDB cluster Pods
	// +optional
	Affinity *corev1.Affinity `json:"affinity,omitempty"`

	// PriorityClassName of TiDB cluster Pods
	// Optional: Defaults to omitted
	// +optional
	PriorityClassName *string `json:"priorityClassName,omitempty"`

	// Base node selectors of TiDB cluster Pods, components may add or override selectors upon this respectively
	// +optional
	NodeSelector map[string]string `json:"nodeSelector,omitempty"`

	// Base annotations of TiDB cluster Pods, components may add or override selectors upon this respectively
	// +optional
	Annotations map[string]string `json:"annotations,omitempty"`

	// Base tolerations of TiDB cluster Pods, components may add more tolerations upon this respectively
	// +optional
	Tolerations []corev1.Toleration `json:"tolerations,omitempty"`

	// Time zone of TiDB cluster Pods
	// Optional: Defaults to UTC
	// +optional
	Timezone string `json:"timezone,omitempty"`

	// Services list non-headless services type used in TidbCluster
	// Deprecated
	// +k8s:openapi-gen=false
	Services []Service `json:"services,omitempty"`

	// EnableDynamicConfiguration indicates whether DynamicConfiguration is enabled for the tidbcluster
	// +optional
	EnableDynamicConfiguration *bool `json:"enableDynamicConfiguration,omitempty"`
}

// TidbClusterStatus represents the current status of a tidb cluster.
type TidbClusterStatus struct {
	ClusterID  string                    `json:"clusterID,omitempty"`
	PD         PDStatus                  `json:"pd,omitempty"`
	TiKV       TiKVStatus                `json:"tikv,omitempty"`
	TiDB       TiDBStatus                `json:"tidb,omitempty"`
	Pump       PumpStatus                `josn:"pump,omitempty"`
	TiFlash    TiFlashStatus             `json:"tiflash,omitempty"`
	TiCDC      TiCDCStatus               `json:"ticdc,omitempty"`
	Monitor    *TidbMonitorRef           `json:"monitor,omitempty"`
	AutoScaler *TidbClusterAutoScalerRef `json:"auto-scaler,omitempyt"`
	// Represents the latest available observations of a tidb cluster's state.
	// +optional
	Conditions []TidbClusterCondition `json:"conditions,omitempty"`
	// +optional
	TiKVGroups []GroupRef `json:"tikv-groups,omitempty"`
	// +optional
	TiDBGroups []GroupRef `json:"tidb-groups,omitempty"`
}
```

### 控制器

```Go
func (r *CronJobReconciler) Reconcile(req ctrl.Request) (ctrl.Result, error) {
	ctx := context.Background()
	log := r.Log.WithValues("cronjob", req.NamespacedName)

	/*
		### 1: Load the CronJob by name

		We'll fetch the CronJob using our client.  All client methods take a
		context (to allow for cancellation) as their first argument, and the object
		in question as their last.  Get is a bit special, in that it takes a
		[`NamespacedName`](https://godoc.org/sigs.k8s.io/controller-runtime/pkg/client#ObjectKey)
		as the middle argument (most don't have a middle argument, as we'll see
		below).

		Many client methods also take variadic options at the end.
	*/
	var cronJob batch.CronJob
	if err := r.Get(ctx, req.NamespacedName, &cronJob); err != nil {
		log.Error(err, "unable to fetch CronJob")
		// we'll ignore not-found errors, since they can't be fixed by an immediate
		// requeue (we'll need to wait for a new notification), and we can get them
		// on deleted requests.
		return ctrl.Result{}, client.IgnoreNotFound(err)
	}

	/*
		### 2: List all active jobs, and update the status

		To fully update our status, we'll need to list all child jobs in this namespace that belong to this CronJob.
		Similarly to Get, we can use the List method to list the child jobs.  Notice that we use variadic options to
		set the namespace and field match (which is actually an index lookup that we set up below).
	*/
	var childJobs kbatch.JobList
	if err := r.List(ctx, &childJobs, client.InNamespace(req.Namespace), client.MatchingFields{jobOwnerKey: req.Name}); err != nil {
		log.Error(err, "unable to list child Jobs")
		return ctrl.Result{}, err
	}

	/*

		<aside class="note">

		<h1>What is this index about?</h1>

		<p>The reconciler fetches all jobs owned by the cronjob for the status. As our number of cronjobs increases,
		looking these up can become quite slow as we have to filter through all of them. For a more efficient lookup,
		these jobs will be indexed locally on the controller's name. A jobOwnerKey field is added to the
		cached job objects. This key references the owning controller and functions as the index. Later in this
		document we will configure the manager to actually index this field.</p>

		</aside>

		Once we have all the jobs we own, we'll split them into active, successful,
		and failed jobs, keeping track of the most recent run so that we can record it
		in status.  Remember, status should be able to be reconstituted from the state
		of the world, so it's generally not a good idea to read from the status of the
		root object.  Instead, you should reconstruct it every run.  That's what we'll
		do here.

		We can check if a job is "finished" and whether it succeeded or failed using status
		conditions.  We'll put that logic in a helper to make our code cleaner.
	*/

	// find the active list of jobs
	var activeJobs []*kbatch.Job
	var successfulJobs []*kbatch.Job
	var failedJobs []*kbatch.Job
	var mostRecentTime *time.Time // find the last run so we can update the status

	/*
		We consider a job "finished" if it has a "succeeded" or "failed" condition marked as true.
		Status conditions allow us to add extensible status information to our objects that other
		humans and controllers can examine to check things like completion and health.
	*/
	isJobFinished := func(job *kbatch.Job) (bool, kbatch.JobConditionType) {
		for _, c := range job.Status.Conditions {
			if (c.Type == kbatch.JobComplete || c.Type == kbatch.JobFailed) && c.Status == corev1.ConditionTrue {
				return true, c.Type
			}
		}

		return false, ""
	}
	// +kubebuilder:docs-gen:collapse=isJobFinished

	/*
		We'll use a helper to extract the scheduled time from the annotation that
		we added during job creation.
	*/
	getScheduledTimeForJob := func(job *kbatch.Job) (*time.Time, error) {
		timeRaw := job.Annotations[scheduledTimeAnnotation]
		if len(timeRaw) == 0 {
			return nil, nil
		}

		timeParsed, err := time.Parse(time.RFC3339, timeRaw)
		if err != nil {
			return nil, err
		}
		return &timeParsed, nil
	}
	// +kubebuilder:docs-gen:collapse=getScheduledTimeForJob

	for i, job := range childJobs.Items {
		_, finishedType := isJobFinished(&job)
		switch finishedType {
		case "": // ongoing
			activeJobs = append(activeJobs, &childJobs.Items[i])
		case kbatch.JobFailed:
			failedJobs = append(failedJobs, &childJobs.Items[i])
		case kbatch.JobComplete:
			successfulJobs = append(successfulJobs, &childJobs.Items[i])
		}

		// We'll store the launch time in an annotation, so we'll reconstitute that from
		// the active jobs themselves.
		scheduledTimeForJob, err := getScheduledTimeForJob(&job)
		if err != nil {
			log.Error(err, "unable to parse schedule time for child job", "job", &job)
			continue
		}
		if scheduledTimeForJob != nil {
			if mostRecentTime == nil {
				mostRecentTime = scheduledTimeForJob
			} else if mostRecentTime.Before(*scheduledTimeForJob) {
				mostRecentTime = scheduledTimeForJob
			}
		}
	}

	if mostRecentTime != nil {
		cronJob.Status.LastScheduleTime = &metav1.Time{Time: *mostRecentTime}
	} else {
		cronJob.Status.LastScheduleTime = nil
	}
	cronJob.Status.Active = nil
	for _, activeJob := range activeJobs {
		jobRef, err := ref.GetReference(r.Scheme, activeJob)
		if err != nil {
			log.Error(err, "unable to make reference to active job", "job", activeJob)
			continue
		}
		cronJob.Status.Active = append(cronJob.Status.Active, *jobRef)
	}

	/*
		Here, we'll log how many jobs we observed at a slightly higher logging level,
		for debugging.  Notice how instead of using a format string, we use a fixed message,
		and attach key-value pairs with the extra information.  This makes it easier to
		filter and query log lines.
	*/
	log.V(1).Info("job count", "active jobs", len(activeJobs), "successful jobs", len(successfulJobs), "failed jobs", len(failedJobs))

	/*
		Using the date we've gathered, we'll update the status of our CRD.
		Just like before, we use our client.  To specifically update the status
		subresource, we'll use the `Status` part of the client, with the `Update`
		method.

		The status subresource ignores changes to spec, so it's less likely to conflict
		with any other updates, and can have separate permissions.
	*/
	if err := r.Status().Update(ctx, &cronJob); err != nil {
		log.Error(err, "unable to update CronJob status")
		return ctrl.Result{}, err
	}

	/*
		Once we've updated our status, we can move on to ensuring that the status of
		the world matches what we want in our spec.

		### 3: Clean up old jobs according to the history limit

		First, we'll try to clean up old jobs, so that we don't leave too many lying
		around.
	*/

	// NB: deleting these is "best effort" -- if we fail on a particular one,
	// we won't requeue just to finish the deleting.
	if cronJob.Spec.FailedJobsHistoryLimit != nil {
		sort.Slice(failedJobs, func(i, j int) bool {
			if failedJobs[i].Status.StartTime == nil {
				return failedJobs[j].Status.StartTime != nil
			}
			return failedJobs[i].Status.StartTime.Before(failedJobs[j].Status.StartTime)
		})
		for i, job := range failedJobs {
			if int32(i) >= int32(len(failedJobs))-*cronJob.Spec.FailedJobsHistoryLimit {
				break
			}
			if err := r.Delete(ctx, job, client.PropagationPolicy(metav1.DeletePropagationBackground)); client.IgnoreNotFound(err) != nil {
				log.Error(err, "unable to delete old failed job", "job", job)
			} else {
				log.V(0).Info("deleted old failed job", "job", job)
			}
		}
	}

	if cronJob.Spec.SuccessfulJobsHistoryLimit != nil {
		sort.Slice(successfulJobs, func(i, j int) bool {
			if successfulJobs[i].Status.StartTime == nil {
				return successfulJobs[j].Status.StartTime != nil
			}
			return successfulJobs[i].Status.StartTime.Before(successfulJobs[j].Status.StartTime)
		})
		for i, job := range successfulJobs {
			if int32(i) >= int32(len(successfulJobs))-*cronJob.Spec.SuccessfulJobsHistoryLimit {
				break
			}
			if err := r.Delete(ctx, job, client.PropagationPolicy(metav1.DeletePropagationBackground)); (err) != nil {
				log.Error(err, "unable to delete old successful job", "job", job)
			} else {
				log.V(0).Info("deleted old successful job", "job", job)
			}
		}
	}

	/* ### 4: Check if we're suspended

	If this object is suspended, we don't want to run any jobs, so we'll stop now.
	This is useful if something's broken with the job we're running and we want to
	pause runs to investigate or putz with the cluster, without deleting the object.
	*/

	if cronJob.Spec.Suspend != nil && *cronJob.Spec.Suspend {
		log.V(1).Info("cronjob suspended, skipping")
		return ctrl.Result{}, nil
	}

	/*
		### 5: Get the next scheduled run

		If we're not paused, we'll need to calculate the next scheduled run, and whether
		or not we've got a run that we haven't processed yet.
	*/

	/*
		We'll calculate the next scheduled time using our helpful cron library.
		We'll start calculating appropriate times from our last run, or the creation
		of the CronJob if we can't find a last run.

		If there are too many missed runs and we don't have any deadlines set, we'll
		bail so that we don't cause issues on controller restarts or wedges.

		Otherwise, we'll just return the missed runs (of which we'll just use the latest),
		and the next run, so that we can know when it's time to reconcile again.
	*/
	getNextSchedule := func(cronJob *batch.CronJob, now time.Time) (lastMissed time.Time, next time.Time, err error) {
		sched, err := cron.ParseStandard(cronJob.Spec.Schedule)
		if err != nil {
			return time.Time{}, time.Time{}, fmt.Errorf("Unparseable schedule %q: %v", cronJob.Spec.Schedule, err)
		}

		// for optimization purposes, cheat a bit and start from our last observed run time
		// we could reconstitute this here, but there's not much point, since we've
		// just updated it.
		var earliestTime time.Time
		if cronJob.Status.LastScheduleTime != nil {
			earliestTime = cronJob.Status.LastScheduleTime.Time
		} else {
			earliestTime = cronJob.ObjectMeta.CreationTimestamp.Time
		}
		if cronJob.Spec.StartingDeadlineSeconds != nil {
			// controller is not going to schedule anything below this point
			schedulingDeadline := now.Add(-time.Second * time.Duration(*cronJob.Spec.StartingDeadlineSeconds))

			if schedulingDeadline.After(earliestTime) {
				earliestTime = schedulingDeadline
			}
		}
		if earliestTime.After(now) {
			return time.Time{}, sched.Next(now), nil
		}

		starts := 0
		for t := sched.Next(earliestTime); !t.After(now); t = sched.Next(t) {
			lastMissed = t
			// An object might miss several starts. For example, if
			// controller gets wedged on Friday at 5:01pm when everyone has
			// gone home, and someone comes in on Tuesday AM and discovers
			// the problem and restarts the controller, then all the hourly
			// jobs, more than 80 of them for one hourly scheduledJob, should
			// all start running with no further intervention (if the scheduledJob
			// allows concurrency and late starts).
			//
			// However, if there is a bug somewhere, or incorrect clock
			// on controller's server or apiservers (for setting creationTimestamp)
			// then there could be so many missed start times (it could be off
			// by decades or more), that it would eat up all the CPU and memory
			// of this controller. In that case, we want to not try to list
			// all the missed start times.
			starts++
			if starts > 100 {
				// We can't get the most recent times so just return an empty slice
				return time.Time{}, time.Time{}, fmt.Errorf("Too many missed start times (> 100). Set or decrease .spec.startingDeadlineSeconds or check clock skew.")
			}
		}
		return lastMissed, sched.Next(now), nil
	}
	// +kubebuilder:docs-gen:collapse=getNextSchedule

	// figure out the next times that we need to create
	// jobs at (or anything we missed).
	missedRun, nextRun, err := getNextSchedule(&cronJob, r.Now())
	if err != nil {
		log.Error(err, "unable to figure out CronJob schedule")
		// we don't really care about requeuing until we get an update that
		// fixes the schedule, so don't return an error
		return ctrl.Result{}, nil
	}

	/*
		We'll prep our eventual request to requeue until the next job, and then figure
		out if we actually need to run.
	*/
	scheduledResult := ctrl.Result{RequeueAfter: nextRun.Sub(r.Now())} // save this so we can re-use it elsewhere
	log = log.WithValues("now", r.Now(), "next run", nextRun)

	/*
		### 6: Run a new job if it's on schedule, not past the deadline, and not blocked by our concurrency policy

		If we've missed a run, and we're still within the deadline to start it, we'll need to run a job.
	*/
	if missedRun.IsZero() {
		log.V(1).Info("no upcoming scheduled times, sleeping until next")
		return scheduledResult, nil
	}

	// make sure we're not too late to start the run
	log = log.WithValues("current run", missedRun)
	tooLate := false
	if cronJob.Spec.StartingDeadlineSeconds != nil {
		tooLate = missedRun.Add(time.Duration(*cronJob.Spec.StartingDeadlineSeconds) * time.Second).Before(r.Now())
	}
	if tooLate {
		log.V(1).Info("missed starting deadline for last run, sleeping till next")
		// TODO(directxman12): events
		return scheduledResult, nil
	}

	/*
		If we actually have to run a job, we'll need to either wait till existing ones finish,
		replace the existing ones, or just add new ones.  If our information is out of date due
		to cache delay, we'll get a requeue when we get up-to-date information.
	*/
	// figure out how to run this job -- concurrency policy might forbid us from running
	// multiple at the same time...
	if cronJob.Spec.ConcurrencyPolicy == batch.ForbidConcurrent && len(activeJobs) > 0 {
		log.V(1).Info("concurrency policy blocks concurrent runs, skipping", "num active", len(activeJobs))
		return scheduledResult, nil
	}

	// ...or instruct us to replace existing ones...
	if cronJob.Spec.ConcurrencyPolicy == batch.ReplaceConcurrent {
		for _, activeJob := range activeJobs {
			// we don't care if the job was already deleted
			if err := r.Delete(ctx, activeJob, client.PropagationPolicy(metav1.DeletePropagationBackground)); client.IgnoreNotFound(err) != nil {
				log.Error(err, "unable to delete active job", "job", activeJob)
				return ctrl.Result{}, err
			}
		}
	}

	/*
		Once we've figured out what to do with existing jobs, we'll actually create our desired job
	*/

	/*
		We need to construct a job based on our CronJob's template.  We'll copy over the spec
		from the template and copy some basic object meta.

		Then, we'll set the "scheduled time" annotation so that we can reconstitute our
		`LastScheduleTime` field each reconcile.

		Finally, we'll need to set an owner reference.  This allows the Kubernetes garbage collector
		to clean up jobs when we delete the CronJob, and allows controller-runtime to figure out
		which cronjob needs to be reconciled when a given job changes (is added, deleted, completes, etc).
	*/
	constructJobForCronJob := func(cronJob *batch.CronJob, scheduledTime time.Time) (*kbatch.Job, error) {
		// We want job names for a given nominal start time to have a deterministic name to avoid the same job being created twice
		name := fmt.Sprintf("%s-%d", cronJob.Name, scheduledTime.Unix())

		job := &kbatch.Job{
			ObjectMeta: metav1.ObjectMeta{
				Labels:      make(map[string]string),
				Annotations: make(map[string]string),
				Name:        name,
				Namespace:   cronJob.Namespace,
			},
			Spec: *cronJob.Spec.JobTemplate.Spec.DeepCopy(),
		}
		for k, v := range cronJob.Spec.JobTemplate.Annotations {
			job.Annotations[k] = v
		}
		job.Annotations[scheduledTimeAnnotation] = scheduledTime.Format(time.RFC3339)
		for k, v := range cronJob.Spec.JobTemplate.Labels {
			job.Labels[k] = v
		}
		if err := ctrl.SetControllerReference(cronJob, job, r.Scheme); err != nil {
			return nil, err
		}

		return job, nil
	}
	// +kubebuilder:docs-gen:collapse=constructJobForCronJob

	// actually make the job...
	job, err := constructJobForCronJob(&cronJob, missedRun)
	if err != nil {
		log.Error(err, "unable to construct job from template")
		// don't bother requeuing until we get a change to the spec
		return scheduledResult, nil
	}

	// ...and create it on the cluster
	if err := r.Create(ctx, job); err != nil {
		log.Error(err, "unable to create Job for CronJob", "job", job)
		return ctrl.Result{}, err
	}

	log.V(1).Info("created Job for CronJob run", "job", job)

	/*
		### 7: Requeue when we either see a running job or it's time for the next scheduled run

		Finally, we'll return the result that we prepped above, that says we want to requeue
		when our next run would need to occur.  This is taken as a maximum deadline -- if something
		else changes in between, like our job starts or finishes, we get modified, etc, we might
		reconcile again sooner.
	*/
	// we'll requeue once we see the running job, and update our status
	return scheduledResult, nil
}
```
