(base) wujingwei@LAPTOP-JHVV030O:~/foundry-cu/ragflow$ git remote -v
gitlab  git@125.122.154.130:wujingwei/ragflow.git (fetch)
gitlab  git@125.122.154.130:wujingwei/ragflow.git (push)
origin  ssh://git@github.com/infiniflow/ragflow.git (fetch)
origin  ssh://git@github.com/infiniflow/ragflow.git (push)
team_shu_lian   git@git.shu-lian.com:datainterconnect/ragflow (fetch)
team_shu_lian   git@git.shu-lian.com:datainterconnect/ragflow (push)




git add .
git commit  -m "增加11个行业场景Agent模板（图片+名称+简介）
港口航运预报
远洋渔情预报
海上风能评估
滨海旅游舒适度预报
蓝碳指数评估
共富农仓
数卫粮安
大黄鱼养殖
番茄🍅生长模型
美妆运营

通用场景Agent模板
通用场景智能体

Agent模板列表页面的白色背景板没有随着模板数量增长而增长，导致当模板数量较多时，背景板高度固定，影响用户体验。" --no-verify




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
