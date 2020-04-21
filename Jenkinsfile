pipeline {
  agent {
    kubernetes {
      cloud 'kubernetes'
      label 'ci'
      defaultContainer 'jnlp'
      yaml """
apiVersion: v1
kind: Pod
metadata:
labels:
  component: ci
spec:
  # Use service account that can deploy to all namespaces
  serviceAccountName: cd-jenkins
  containers:
  - name: helm
    image: alpine/helm:2.14.3
    command:
    - cat
    tty: true
  - name: gcloud
    image: gcr.io/cloud-builders/gcloud
    command:
    - cat
    tty: true
  - name: curl
    image: gcr.io/cloud-builders/curl
    command:
    - cat
    tty: true
  - name: git
    image: gcr.io/cloud-builders/git
    command:
    - cat
    tty: true
"""
}
  }
   stages {
     stage('Deploy') {
         steps {
             script {
               withCredentials([string(credentialsId: 'jenkins_token', variable: 'vault_token')]) {
                 gitorg = input message: 'What is your gitorg', ok: 'Submit', parameters: [choice(choices: ['dev1', 'dev2'], description: 'This is part of the pathing structure for Vault', name: 'input')], submitterParameter: 'merger'
                 dc = input message: 'What is your dc', ok: 'Submit', parameters: [choice(choices: ['dc1', 'dc2'], description: 'This is part of the pathing structure for Vault', name: 'input')], submitterParameter: 'merger'
                 appname = input message: 'What is your appname', ok: 'Submit', parameters: [choice(choices: ['pytestapp', 'javatestapp'], description: 'This is part of the pathing structure for Vault', name: 'input')], submitterParameter: 'merger'
                 role_id_path = ['auth', gitorg, appname, 'role', dc, 'role-id'].join('/')
		 vault_addr = 'http://34.69.161.191'
		 //secret_map = httpRequest customHeaders: [[maskValue: true, name: 'X-Vault-Token', : vault_token]], httpMode: 'POST', ignoreSslErrors: true, requestBody: '''{  "metadata": "{ "dc": ${dc.input},  "gitorg": ${gitorg.input}, "appname": ${appname.input}"}"}''', url: "http://34.69.161.191/v1/auth/${gitorg.input}/${appname.input}/role/${dc.input}/secret-id", wrapAsMultipart: false
		 secret_map = httpRequest contentType: 'APPLICATION_JSON', customHeaders: [[maskValue: false, name: 'X-Vault-Token', value: 'abc123']], httpMode: 'POST', ignoreSslErrors: true, requestBody: '''{ "metadata": " "dc": "${dc.input}",  "gitorg": "${gitorg.input}", "appname": "${appname.input}"}"}''', responseHandle: 'NONE', url: "http://34.69.161.191/v1/auth/${gitorg.input}/${appname.input}/role/${dc.input}/secret-id", wrapAsMultipart: false
                 // secret_map = sh label: '', returnStdout: true, script: 'curl --header "X-Vault-Token\\: ${vault_token}" --request POST --data \'{"metadata"\\: { \\"dc\\"\\: \\"$dc\\",  \\"gitorg\\"\\: \\"$gitorg\\", \\    "appname\\"\\: \\"$appname\\"}"}\' $vault_addr/v1/auth/$gitorg/$appname/role/$dc/secret-id'
		 //echo "${secret_map}"
                 }
		}
        container('helm') {
        withCredentials([file(credentialsId: 'kubeconfig', variable: 'kubeconfig')]) {
 //       script {
//                sh("cp \$kubeconfig /kconfig")
//                h("helm --kubeconfig /kconfig upgrade pytestapp ./helm_chart --install --set gitorg=${gitorg.input} --set appname=${appname.input} --set dc=${dc.input} --set role_id=${secret_map.role_id} secret_id=${secret_map.secret_id} --wait")
// 	  }
	  }
	}
     }
         }
     }
     }
