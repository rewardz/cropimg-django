pipeline {
  agent {
    kubernetes {
      yaml '''
apiVersion: v1
kind: Pod
spec:
  serviceAccountName: jenkins
  tolerations:
    - key: "cicd"
      operator: "Exists"
      effect: "NoSchedule"
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: app
            operator: In
            values: ['cicd']
  containers:
    - name: nerdctl
      image: 926080010171.dkr.ecr.ap-southeast-1.amazonaws.com/nerdctl:v2.1.6
      imagePullPolicy: Always
      command:
      - cat
      tty: true
      resources:
        requests:
          memory: "512Mi"
          cpu: "512m"
        limits:
          memory: "512Mi"
          cpu: "512m"
      volumeMounts:
      - name: containerd-socket
        mountPath: /run/containerd/containerd.sock
      - name: buildkit-socket
        mountPath: /run/buildkit
    - name: buildkitd
      image: moby/buildkit:v0.27.1
      imagePullPolicy: Always
      args:
        - --addr
        - unix:///run/buildkit/buildkitd.sock
      readinessProbe:
        exec:
          command:
            - buildctl
            - debug
            - workers
        initialDelaySeconds: 5
        periodSeconds: 5
      securityContext:
        privileged: true
      resources:
        requests:
          memory: "512Mi"
          cpu: "512m"
        limits:
          memory: "512Mi"
          cpu: "512m"
      volumeMounts:
        - name: buildkit-socket
          mountPath: /run/buildkit
  volumes:
    - name: containerd-socket
      hostPath:
        path: /run/containerd/containerd.sock
        type: Socket
    - name: buildkit-socket
      emptyDir: {}
''' }
  }
  options {
    ansiColor('xterm')
    skipDefaultCheckout true
    disableConcurrentBuilds(abortPrevious: true)
  }
  environment {
    ID_RSA = credentials('devops_id_rsa')
    ECR_REGISTRY = '926080010171.dkr.ecr.ap-southeast-1.amazonaws.com'
    FINAL_IMAGE = 'cropimg-django'
    PR_NUM = "${env.CHANGE_ID}"
    NAMESPACE = "pr-cropimg-django-${PR_NUM}"
    AWS_REGION = 'ap-southeast-1'
    SOURCE_BRANCH = "${env.CHANGE_BRANCH}"
    tags = setTags(SOURCE_BRANCH, PR_NUM)
    IMAGE_TAG_1_8 = "1-8-${tags.IMAGE_TAG}"
    IMAGE_TAG_1_11 = "1-11-${tags.IMAGE_TAG}"
    DOCKERFILE = 'Dockerfile'
  }
  stages {
    stage ('init') {
      steps {
        checkout([$class: 'GitSCM', branches: [[name: "${env.CHANGE_BRANCH}"]], extensions: [[$class: 'RelativeTargetDirectory', relativeTargetDir: 'cropimg-django']], userRemoteConfigs: [[credentialsId: 'github-app-rewardz', url: 'https://github.com/rewardz/cropimg-django.git']]])
        
        container('nerdctl') {
          script {
            sh '''
              mkdir ~/.ssh/
              touch ~/.ssh/id_rsa
              chmod 600 ~/.ssh/id_rsa
              chmod 666 /dev/tty
              cp $ID_RSA ~/.ssh/id_rsa
              touch ~/.ssh/known_hosts 
              ssh -T -o StrictHostKeyChecking=no git@github.com || true
              git config --global --add safe.directory '*'
            '''
          }
        }
      }
    }
    stage('Build Image & Setup Infra') {
      parallel {
        stage('Build docker image Django 1.8') {
          steps {
            container('nerdctl') {
              script {
                dockerLogin(ECR_REGISTRY, AWS_REGION)
                sh """
                  # Wait for buildkit to be ready
                  until buildctl --addr unix:///run/buildkit/buildkitd.sock debug workers; do
                    echo "Waiting for buildkit to be ready..."
                    sleep 5
                  done

                  cd cropimg-django
                  
                  ls -lah

                  # Set BUILDKIT_HOST for nerdctl
                  export BUILDKIT_HOST=unix:///run/buildkit/buildkitd.sock

                  echo Build Final Image
                  nerdctl build \
                    --file ${DOCKERFILE} \
                    --target cropimg \
                    --progress=plain -t ${ECR_REGISTRY}/${FINAL_IMAGE}:${IMAGE_TAG_1_8} .
                  nerdctl push ${ECR_REGISTRY}/${FINAL_IMAGE}:${IMAGE_TAG_1_8}
                  
                  echo "Cleaning up final image from local storage"
                  nerdctl rmi ${ECR_REGISTRY}/${FINAL_IMAGE}:${IMAGE_TAG_1_8} || echo "Final image already removed"
                """
              }
            }
          }
        }
        stage('Build docker image Django 1.11') {
          steps {
            container('nerdctl') {
              script {
                dockerLogin(ECR_REGISTRY, AWS_REGION)
                sh """
                  # Wait for buildkit to be ready
                  until buildctl --addr unix:///run/buildkit/buildkitd.sock debug workers; do
                    echo "Waiting for buildkit to be ready..."
                    sleep 5
                  done

                  cd cropimg-django
                  
                  ls -lah

                  # Set BUILDKIT_HOST for nerdctl
                  export BUILDKIT_HOST=unix:///run/buildkit/buildkitd.sock

                  echo Build Final Image
                  nerdctl build \
                    --file ${DOCKERFILE} \
                    --target cropimg \
                    --build-arg REQUIREMENTS_FILE=requirements/django111/test.txt \
                    --progress=plain -t ${ECR_REGISTRY}/${FINAL_IMAGE}:${IMAGE_TAG_1_11} .
                  nerdctl push ${ECR_REGISTRY}/${FINAL_IMAGE}:${IMAGE_TAG_1_11}
                  
                  echo "Cleaning up final image from local storage"
                  nerdctl rmi ${ECR_REGISTRY}/${FINAL_IMAGE}:${IMAGE_TAG_1_11} || echo "Final image already removed"
                """
              }
            }
          }
        }
        stage('Setup Infra') {
          steps {
            container('nerdctl') {
              script {
                sh """
                  echo "Avoiding race condition by waiting for the namespace to be removed from previous runs"
                  sleep 90

                  kubectl create ns ${NAMESPACE} || echo "Namespace ${NAMESPACE} already exists"
                """
              }
            }
          }
        }
      }
    }
    stage('Run Test') {
      parallel {
        stage('Run Test Django 1.8') {
          agent {
              kubernetes {
                  yaml """
              apiVersion: v1
              kind: Pod
              metadata:
                name: backend-1-8
                namespace: ${NAMESPACE}
              spec:
                tolerations:
                  - key: "cicd"
                    operator: "Exists"
                    effect: "NoSchedule"
                affinity:
                  nodeAffinity:
                    requiredDuringSchedulingIgnoredDuringExecution:
                      nodeSelectorTerms:
                      - matchExpressions:
                        - key: app
                          operator: In
                          values: ['cicd']
                containers:
                  - name: backend
                    image: ${ECR_REGISTRY}/${FINAL_IMAGE}:${IMAGE_TAG_1_8}
                    imagePullPolicy: Always
                    command:
                      - cat
                    tty: true
                    resources:
                      limits:
                          cpu: "256m"
                          memory: "256Mi"
                      requests:
                          cpu: "256m"
                          memory: "256Mi"
              """
              }
          }
          steps {
              container('backend') {
                  script {
                      try {
                          sh """
                            cd /code && python -m pytest --cov=cropimg --cov-report=term-missing
                          """
                      } catch (Exception e) {
                          echo "Tests failed"
                          throw e
                      }
                  }
              }
          }
        }
        stage('Run Test Django 1.11') {
          agent {
              kubernetes {
                  yaml """
              apiVersion: v1
              kind: Pod
              metadata:
                name: backend-1-11
                namespace: ${NAMESPACE}
              spec:
                tolerations:
                  - key: "cicd"
                    operator: "Exists"
                    effect: "NoSchedule"
                affinity:
                  nodeAffinity:
                    requiredDuringSchedulingIgnoredDuringExecution:
                      nodeSelectorTerms:
                      - matchExpressions:
                        - key: app
                          operator: In
                          values: ['cicd']
                containers:
                  - name: backend
                    image: ${ECR_REGISTRY}/${FINAL_IMAGE}:${IMAGE_TAG_1_11}
                    imagePullPolicy: Always
                    command:
                      - cat
                    tty: true
                    resources:
                      limits:
                          cpu: "256m"
                          memory: "256Mi"
                      requests:
                          cpu: "256m"
                          memory: "256Mi"
              """
              }
          }
          steps {
              container('backend') {
                  script {
                      try {
                          sh """
                            cd /code && python -m pytest --cov=cropimg --cov-report=term-missing
                          """
                      } catch (Exception e) {
                          echo "Tests failed"
                          throw e
                      }
                  }
              }
          }
        }
      }
    }
  }
  post {
    always {
      container('nerdctl') {
        script {
          sh """
            kubectl delete namespace ${NAMESPACE}
          """
        }
      }
    }
  }
}

def dockerLogin(ecrRegistry, awsRegion) {
    sh """
    aws ecr get-login-password --region ${awsRegion} | nerdctl login --username AWS --password-stdin ${ecrRegistry}
    """
}

def setTags(SOURCE_BRANCH, PR_NUM) {
    def IMAGE_TAG
    def CACHE_TAG

    if (SOURCE_BRANCH == 'dev' || SOURCE_BRANCH == 'master') {
        IMAGE_TAG = "${SOURCE_BRANCH}-${PR_NUM}"
        CACHE_TAG = "${SOURCE_BRANCH}-cache"
    } else {
        IMAGE_TAG = "pr-${PR_NUM}"
        CACHE_TAG = "pr-${PR_NUM}-cache"
    }

    return [IMAGE_TAG: IMAGE_TAG, CACHE_TAG: CACHE_TAG]
}
