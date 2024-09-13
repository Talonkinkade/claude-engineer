
diff --git a/docker/Dockerfile b/docker/Dockerfile
index 9ce5e6e1..d2392e49 100644
--- a/docker/Dockerfile
+++ b/docker/Dockerfile
@@ -29,13 +29,4 @@ RUN playwright install --with-deps chromium

 ENTRYPOINT ["aider"]

-#########################
-FROM base AS aider
-
-COPY . /aider
-RUN pip install --upgrade pip \
-    && pip install --no-cache-dir /aider \
-       --extra-index-url https://download.pytorch.org/whl/cpu \
-    && rm -rf /aider
-
-ENTRYPOINT ["aider"]
+docker build -t aider-full --target aider-full .
diff --git a/scripts/jekyll_build.sh b/scripts/jekyll_build.sh
index bc41c66c..f22a1f12 100755
--- a/scripts/jekyll_build.sh
+++ b/scripts/jekyll_build.sh
@@ -1,4 +1,3 @@
 #!/bin/bash

-# Build the Docker image
-docker build -t my-jekyll-site -f scripts/Dockerfile.jekyll .
+docker build -t my-jekyll-site -d scripts/Dockerfile.jekyll 
\ No newline at end of file

