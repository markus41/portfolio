{{- define "brookside.name" -}}
{{ .Chart.Name }}
{{- end -}}

{{- define "brookside.fullname" -}}
{{ include "brookside.name" . }}
{{- end -}}

{{- define "brookside.labels" -}}
app.kubernetes.io/name: {{ include "brookside.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{- define "brookside.selectorLabels" -}}
app.kubernetes.io/name: {{ include "brookside.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}
