(base) wujingwei@LAPTOP-JHVV030O:~/foundry-cu/ragflow$ git remote -v
gitlab  git@125.122.154.130:wujingwei/ragflow.git (fetch)
gitlab  git@125.122.154.130:wujingwei/ragflow.git (push)
origin  ssh://git@github.com/infiniflow/ragflow.git (fetch)
origin  ssh://git@github.com/infiniflow/ragflow.git (push)
team_shu_lian   git@git.shu-lian.com:datainterconnect/ragflow (fetch)
team_shu_lian   git@git.shu-lian.com:datainterconnect/ragflow (push)




git add .




git commit  --no-verify -m "修改了全局样式 (web/src/global.less)
主要改进：
移除了 html 元素上的 overflow: hidden 设置
这允许页面正常滚动，特别是在登录页面" 




git fetch team_shu_lian

# 基于当前分支创建新开发分支
git checkout -b dev

# 推送新分支到远程（首次推送需用 -u 建立跟踪）
git push -u team_shu_lian dev

# 后续推送简化
git push


http://git.shu-lian.com:30080/users/sign_in
http://125.122.154.130:30080 wujingwei dfPvO1dYCpf2FRvD
git 地址和账号密码
